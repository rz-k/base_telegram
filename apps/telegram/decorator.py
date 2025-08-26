from functools import wraps

from apps.bot.models import ChannelSponsor


def channel_sponsor(self):
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
            if self.bot.is_join_channel(channel.chat_id, self.chat_id):
                continue
            else:
                not_join_channel_chat_id.append(channel.chat_id)

        if not_join_channel_chat_id:
            channels = channels.filter(chat_id__in=not_join_channel_chat_id)
            self.bot.send_message(
                chat_id=self.chat_id,
                text=msg,
                parse_mode="html",
                reply_markup=self.inline_keyboard.sponsor_channel_keyboard(channels)
            )
            return True
    return False

def sponsor_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if channel_sponsor(self):
            return
        return func(self, *args, **kwargs)
    return wrapper
