from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Update
from utils.utils import update_object


class CommandHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)
        self.bot = bot
        self.update = update


    def start_handler(self):
        """
        Handles the /start command or entry point of the bot.

        - If the user does not exist, a new user will be created with the step set to "home".
        - If the user already exists, their current step will be updated to "home".
        - Finally, sends a "Home" message with the corresponding reply keyboard.

        This function serves as the main entry point of the bot and represents the home screen.
        """

        self.create_user(step="home")
        update_object(self.user_obj, step="home")

        return self.bot.send_message(
            chat_id=self.chat_id,
            text="Home",
            reply_markup=self.reply_keyboard.home_keyboard(),
        )

    def help_handler(self):
        return self.bot.send_message(chat_id=self.chat_id, text="Help Command")

    def handle(self):

        if self.update.message.text.startswith("/start"):
            self.start_handler()

        elif self.update.message.text.startswith("/help"):
            self.help_handler()

        print("Command Handlers")
