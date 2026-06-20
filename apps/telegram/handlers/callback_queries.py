from apps.telegram.decorator import sponsor_required
from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Update
from utils.utils import update_object


class CallBackQueryHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)

        self.callback_handlers = {
            "joined_to_sponsor": self.joined_channel_sponsor_handler,
            "first_button": self.first_button_handler,
        }

    @sponsor_required
    def joined_channel_sponsor_handler(self):
        self.bot.answer_callback_query(callback_query_id=self.update.callback_query.id, text="⏳")
        self.bot.delete_message(chat_id=self.chat_id, message_id=self.update.callback_query.message.message_id)
        update_object(self.user_obj, step="home")
        return self.bot.send_message(
            chat_id=self.chat_id,
            text="Home"
        )

    def first_button_handler(self):
        return self.bot.answer_callback_query(callback_query_id=self.update.callback_query.id, text="first_button")

    def handle(self):
        print("CallBackQueryHandler Handlers")
        # check update bot
        if self.is_update_mode():return  # noqa: E701
        if self.is_user_block():return  # noqa: E701


        callback_data = self.update.callback_query.data or ""
        base_key = callback_data.split(":", 1)[0] # callback_data is "check_joined_channel_sponsor" or "check_joined_channel_sponsor:user_id"

        handler = self.callback_handlers.get(base_key)
        if handler:
            return handler()
