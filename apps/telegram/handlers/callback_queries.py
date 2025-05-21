from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram_models import Update
from apps.telegram.telegram import Telegram


class CallBackQueryHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)

    def handle(self):
        print(f"CallBackQueryHandler Handlers")