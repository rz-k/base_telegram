import threading
from typing import Optional

from django.utils.functional import cached_property

from apps.account.models import User as UserDB
from apps.common._message import MessageManager
from apps.telegram.keyboard import InlineKeyboardMarkup, ReplyKeyboardMarkup
from apps.telegram.telegram import Telegram
from apps.telegram.telegram_models import Chat, Update, User


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
        self.reply_keyboard = ReplyKeyboardMarkup()
        self.inline_keyboard = InlineKeyboardMarkup()
        self.bot_messages = MessageManager()

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

    @cached_property
    def user_obj(self) -> Optional[UserDB]:
        if not self.user:
            return None
        if not self.is_private():
            return None
        user, _ = UserDB.objects.get_or_create(
            user_id=self.user_id,
            defaults={
                "username": self.user.username or str(self.user_id),
                "password": str(self.user_id),
                "first_name": self.user.first_name,
                "last_name": self.user.last_name or str(self.user_id),
            }
        )
        return user

    @property
    def user_step(self):
        """
        Returns the current user step from the database.
        """
        return self.user_obj.step if self.user_obj else None

    @property
    def user_id(self) -> Optional[int]:
        """
        Returns the Telegram user ID, if available.
        """
        return self.user.id if self.user else None

    @property
    def text(self) -> str:
        """
        Checks whether the update is a text message.
        """
        if self.update.message:
            return self.update.message.text
        if self.update.callback_query:
            return self.update.callback_query.message.text

        return None

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

    def is_private(self) -> bool:
        """
        Checks whether the message contains a private chat.
        """
        if self.chat:
            return self.chat.type == "private"
        return None

    def is_group(self) -> bool:
        """
        Checks whether the message contains a group chat.
        """
        if self.chat:
            return self.chat.type in ["supergroup", "group"]
        return None

    def run_function_in_thread(self, func, *args, **kwargs):
        """
            Run the given function in a separate thread.
        """
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    def is_update_mode(self):
        """Check if the application is currently in update mode."""
        from apps.bot.models import BotUpdateStatus
        update_obj = BotUpdateStatus.objects.first()
        if update_obj.is_update and not self.user_obj.is_superuser:
            return self.bot.send_message(
                self.chat_id,
                text=update_obj.update_msg,
                parse_mode="html"
            )
        return False

    def is_user_block(self):

        if self.user_obj and not self.user_obj.is_active:
            return self.bot.send_message(
                self.chat_id,
                text="شما در ربات بلاک شده اید",
                parse_mode="html"
            )
        return False
