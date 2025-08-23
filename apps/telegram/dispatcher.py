from apps.telegram.handlers import CallBackQueryHandler, CommandHandler, MediaHandler, MessageHandler
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Update


class Dispatcher:
    """
    Dispatcher is responsible for routing incoming Telegram updates to the appropriate handler
    based on the type of content in the update.

    Attributes:
        update (Update): The incoming update object from Telegram.
        bot (Telegram): An instance of the Telegram bot interface used for interacting with the API.

    Methods:
        dispatch():
            Routes the update to the appropriate handler:
            - If it's a command (starts with '/'), it is handled by CommandHandler.
            - If it's a media message (photo, audio, video, voice, document, or sticker),
              it is handled by MediaHandler.
            - If it's a regular text message, it is handled by MessageHandler.
            - If it's a callback query (e.g., from inline buttons), it is handled by CallBackQueryHandler.
            - Any other unknown update is passed to MessageHandler by default.
    """

    def __init__(self, update: Update, bot: Telegram = None):
        self.update = update
        self.bot = bot or Telegram()

    def dispatch(self):

        if self.update.message:
            if self.update.message.text and self.update.message.text.startswith("/"):
                return CommandHandler(update=self.update, bot=self.bot).handle()

            elif any([
                self.update.message.photo,
                self.update.message.audio,
                self.update.message.video,
                self.update.message.voice,
                self.update.message.document,
                self.update.message.sticker
            ]):
                return MediaHandler(update=self.update, bot=self.bot).handle()

            return MessageHandler(update=self.update, bot=self.bot).handle()

        elif self.update.callback_query:
            return CallBackQueryHandler(update=self.update, bot=self.bot).handle()

        return MessageHandler(update=self.update, bot=self.bot).handle()
