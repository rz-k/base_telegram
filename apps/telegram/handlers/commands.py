from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram_models import Update
from apps.telegram.telegram import Telegram


class CommandHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)
        self.bot = bot
        self.update = update

    
    def start_handler(self):
        self.create_user(step="home")
        return self.bot.send_message(chat_id=self.chat_id, text="Hello Start Command")

    def help_handler(self):
        return self.bot.send_message(chat_id=self.chat_id, text="Help Command")

    def handle(self):

        if self.update.message.text.startswith("/start"):
            self.start_handler()

        elif self.update.message.text.startswith("/help"):
            self.help_handler()

        print(f"Command Handlers")