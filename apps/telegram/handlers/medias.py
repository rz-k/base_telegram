from apps.telegram.handlers.base_handlers import BaseHandler
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Update


class MediaHandler(BaseHandler):

    def __init__(self, update: Update, bot: Telegram):
        super().__init__(update, bot)


    def handle(self):
        if self.is_update_mode():return  # noqa: E701
        if self.is_user_block():return  # noqa: E701

        print("Media Handlers")
