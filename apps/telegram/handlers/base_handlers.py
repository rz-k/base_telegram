from typing import Optional
from apps.telegram.telegram_models import Update, Chat, User
from apps.telegram.telegram import Telegram
from utils.logger import logger


class BaseHandler:
    def __init__(self, update: Update, bot: Telegram):
        self.update = update
        self.bot = bot

    @property
    def chat(self) -> Optional[Chat]:
        if self.update.message:
            return self.update.message.chat
        if self.update.callback_query:
            return self.update.callback_query.message.chat
        return None

    @property
    def user(self) -> Optional[User]:        
        if self.update.message:
            return self.update.message.from_user
        if self.update.callback_query:
            return self.update.callback_query.from_user
        if self.update.inline_query:
            return self.update.inline_query.from_user
        return None

    @property
    def chat_id(self) -> Optional[int]:
        return self.chat.id if self.chat else None

    @property
    def user_id(self) -> Optional[int]:
        return self.user.id if self.user else None

    def is_text(self) -> bool:
        return bool(self.update.message and self.update.message.text)

    def is_command(self) -> bool:
        return  self.update.message and self.update.message.startswith("/")        

    def is_photo(self) -> bool:
        return bool(self.update.message and self.update.message.photo)

    def send_message(self, text: str):
        logger.info(f"[SEND] To {self.chat_id}: {text}")

    def log(self):
        logger.info(f"[LOG] update from user={self.user_id}, chat={self.chat_id}")