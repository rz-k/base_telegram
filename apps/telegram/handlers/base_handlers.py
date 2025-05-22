from typing import Optional
from apps.telegram.telegram_models import Update, Chat, User
from apps.telegram.telegram import Telegram
from utils.logger import logger
from django.contrib.auth import get_user_model
UserDb = get_user_model()


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

    def create_user(self, **kwargs):
        """
        This method checks if the user object exists in the DB or not.
        If the user not exist, then add them to the DB.
        Sets the `user_qs` and `user_obj` as global variables.
        If the user is new, then call the `check_referral_user` method.
        """
        self.qs = UserDb.objects.filter(user_id=self.user_id)        
        if not self.qs:
            username = self.user.username
            dup_username = UserDb.objects.filter(username=username)
            if dup_username:
                username = self.user_id
            return UserDb.objects.create_user(
                username=username,
                password=str(self.user_id),
                first_name=self.user.first_name,
                last_name=self.user.last_name if self.user.last_name else self.user_id,
                user_id=self.user_id,
                **kwargs
            )

    @property
    def user_qs(self):  
        self.create_user  
        return UserDb.objects.filter(user_id=self.user_id)
    
    @property
    def user_obj(self):
        return self.user_qs.first()

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