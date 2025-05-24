from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram_models import Update
from apps.telegram.telegram import Telegram


class MessageHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)

        self.steps = {
            "home": self.home
        }
    
    def home(self):
        print("Home")

    def handle(self):

        if callback := self.steps.get(self.user_step): # step : "home"
            return callback()

        if callback := self.steps.get(self.user_step.split(":")[0]): # step : "home:info"
            return callback()