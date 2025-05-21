from apps.bot.telegram_models import Update
from apps.bot.handlers import (
    CommandHandler,
    MessageHandler,
    CallBackQueryHandler,
    MediaHandler
)


class Dispatcher:
    def __init__(self, update: Update):
        self.update = update

    def dispatch(self):

        if self.update.message:
            if self.update.message.text and self.update.message.text.startswith("/"):
                return CommandHandler(update=self.update).handle()

        elif self.update.message.text:
            return MessageHandler(update=self.update).handle()
            
        elif self.update.message.photo or self.update.message.audio or self.update.message.video or self.update.message.voice or self.update.message.document or self.update.message.sticker:
            return MediaHandler(update=self.update).handle()
        
        elif self.update.callback_query:
            return CallBackQueryHandler(update=self.update).handle()
            
        else:
            return MessageHandler(update=self.update).handle()
            