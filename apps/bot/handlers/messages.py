from apps.bot.handlers.base_handlers import BaseHandler
from apps.bot.telegram_models import Update


class MessageHandler(BaseHandler):

    def __init__(self, update: Update):
        super().__init__(update)


    def handle(self):
        print(f"Message Handlers")