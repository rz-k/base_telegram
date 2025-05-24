from typing import Optional
from apps.telegram.telegram_models import Update, Chat, User
from apps.telegram.telegram import Telegram
from utils.logger import logger
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
UserDb = get_user_model()

class BaseHandler:
    """
    Base handler class that provides common utilities for processing Telegram updates,
    such as accessing user, chat, and message details.
    """

    def __init__(self, update: Update, bot: Telegram):
        """
        Initializes the handler with the incoming update and bot instance.
        """
        self.update = update
        self.bot = bot

    @property
    def chat(self) -> Optional[Chat]:
        """
        Returns the chat object from the update, if available.
        """
        if self.update.message:
            return self.update.message.chat
        if self.update.callback_query:
            return self.update.callback_query.message.chat
        return None

    @property
    def user(self) -> Optional[User]:
        """
        Returns the user object who sent the update, if available.
        """
        if self.update.message:
            return self.update.message.from_user
        if self.update.callback_query:
            return self.update.callback_query.from_user
        if self.update.inline_query:
            return self.update.inline_query.from_user
        return None

    @property
    def chat_id(self) -> Optional[int]:
        """
        Returns the chat ID, if the chat exists.
        """
        return self.chat.id if self.chat else None

    def create_user(self, **kwargs):
        """
        Ensures the Telegram user is stored in the database.
        If the user does not exist, creates a new one.
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
    @cached_property
    def user_qs(self):
        """
        Returns the QuerySet for the current user from the database.
        """
        self.create_user()
        return UserDb.objects.filter(user_id=self.user_id)

    @cached_property
    def user_obj(self) -> UserDb:
        """
        Returns the first user object from the user QuerySet.
        """
        return self.user_qs.first()
    @property
    def user_step(self):
        """
        Returns the current user step from the database.
        """
        return self.user_obj.step

    @property
    def user_id(self) -> Optional[int]:
        """
        Returns the Telegram user ID, if available.
        """
        return self.user.id if self.user else None

    def is_text(self) -> bool:
        """
        Checks whether the update is a text message.
        """
        return bool(self.update.message and self.update.message.text)

    def is_command(self) -> bool:
        """
        Checks whether the message is a command (starts with "/").
        """
        return bool(self.update.message and self.update.message.text and self.update.message.text.startswith("/"))

    def is_photo(self) -> bool:
        """
        Checks whether the message contains a photo.
        """
        return bool(self.update.message and self.update.message.photo)