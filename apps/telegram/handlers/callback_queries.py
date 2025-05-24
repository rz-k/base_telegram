from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram_models import Update
from apps.telegram.telegram import Telegram


class CallBackQueryHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)

        self.callback_handlers = {            
            "check_joined_channel_sponsor": self.handler_joined_channel_sponsor,            
        }

    def handler_joined_channel_sponsor(self):
        print("check_joined_channel_sponsor")

    def handle(self):
        print(f"CallBackQueryHandler Handlers")
        
        callback_data = self.update.callback_query.data or ""
        base_key = callback_data.split(":", 1)[0] # callback_data is "check_joined_channel_sponsor" or "check_joined_channel_sponsor:user_id"

        handler = self.callback_handlers.get(base_key)
        if handler:
            return handler()
