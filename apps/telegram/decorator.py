import json
from functools import wraps

from django.core.cache import cache

from apps.bot.models import ChannelSponsor
from apps.telegram.handlers.base_handlers import BaseHandler
from utils.load_env import env


class SponsorCacheHandler:

    @staticmethod
    def set_cache(key: str, value, expire: int = 3600):
        """
        Store value in Django cache. Value will be serialized to JSON.
        """
        serialized = json.dumps(value)
        cache.set(key, serialized, expire)

    @staticmethod
    def get_cache(key: str):
        """
        Get value from cache. If not exists, return None.
        Automatically deserializes JSON.
        """
        data = cache.get(key)
        return bool(data)

def channel_sponsor(self: BaseHandler):

    sponsor_cache = SponsorCacheHandler()
    cache_key = f"{env.BOT_USERNAME}:sponsor:{self.user_id}"
    cached = sponsor_cache.get_cache(cache_key)
    if cached:
        return True

    channels = ChannelSponsor.objects.all()
    try:
        msg = self.bot_messages.get_message("sponsor_channels_message")
    except Exception:
        msg = "please join in the sponsor channel"
    if channels:
        not_join_channel_chat_id = []
        for channel in channels:
            if channel.other:
                continue
            if self.bot.is_join_channel(channel.chat_id, self.user_id):
                continue
            else:
                not_join_channel_chat_id.append(channel.chat_id)

        if not_join_channel_chat_id:
            channels = channels.filter(chat_id__in=not_join_channel_chat_id)
            self.bot.send_message(
                chat_id=self.user_id,
                text=msg,
                parse_mode="html",
                reply_markup=self.inline_keyboard.sponsor_channel_keyboard(channels)
            )
            return False
    sponsor_cache.set_cache(cache_key, True, expire=60)
    return True

def sponsor_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not channel_sponsor(self):
            return
        return func(self, *args, **kwargs)
    return wrapper
