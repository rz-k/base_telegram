from apps.telegram.decorator import sponsor_required
from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Update
from utils.utils import update_object


class MessageHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)
        self.update = update
        self.bot = bot

        self.steps = {
            "home": self.home,
            "second_button": self.second_button
        }

    @sponsor_required
    def home(self):
        """
        Handles user interactions when the user is at the "home" step.

        - If the user presses "دکمه اول", a message is sent along with an inline keyboard.
        - If the user presses "دکمه دوم", the user's step is updated to "second_button"
        and a message is sent with a back button (reply keyboard).

        This method routes the user based on their selected option from the home screen.
        """

        if self.update.message.text == "دکمه اول":
            return self.bot.send_message(
                chat_id=self.chat_id,
                text="دکمه اول",
                reply_markup=self.inline_keyboard.first_keyboard()

            )
        elif self.update.message.text == "دکمه دوم":
            update_object(self.user_obj, step="second_button")
            return self.bot.send_message(
                chat_id=self.chat_id,
                text="دکمه دوم",
                reply_markup=self.reply_keyboard.back_keyboard()
            )

    def second_button(self):
        """
        Handles user interactions when the user is at the "second_button" step.

        - If the user presses "بازگشت", their step is updated to "home"
        and the home screen message is sent with the main reply keyboard.

        This method allows the user to navigate back to the home screen.
        """

        if self.update.message.text == "بازگشت":
            # update user step
            update_object(self.user_obj, step="home")

            return self.bot.send_message(
                chat_id=self.chat_id,
                text="Home",
                reply_markup=self.reply_keyboard.home_keyboard(),
            )

    def handle(self):
        if self.is_update_mode():return  # noqa: E701
        if self.is_user_block():return  # noqa: E701

        if self.user_step:
            if callback := self.steps.get(self.user_step): # step : "home"
                return callback()

            if callback := self.steps.get(self.user_step.split(":")[0]): # step : "home:info"
                return callback()
