import json
from typing import Any, Dict, List, Optional, cast

import requests

from apps.telegram.telegram_models import (
    AcceptedGiftTypes,
    BotAccessSettings,
    BotCommand,
    BotCommandList,
    BotCommandScope,
    BotDescription,
    BotName,
    BotShortDescription,
    BusinessConnection,
    ChatAdministratorRights,
    ChatFullInfo,
    ChatInviteLink,
    ChatMember,
    ChatMemberAdapter,
    ChatPermissions,
    File,
    ForumTopic,
    GameHighScore,
    Gift,
    InlineKeyboardMarkup,
    InlineQueryResult,
    InlineQueryResultsButton,
    InputChecklist,
    InputFile,
    InputMedia,
    InputPaidMedia,
    InputPollMedia,
    InputPollOption,
    InputProfilePhoto,
    InputRichMessage,
    InputSticker,
    InputStoryContent,
    KeyboardButton,
    LabeledPrice,
    LinkPreviewOptions,
    MenuButton,
    MenuButtonAdapter,
    Message,
    MessageEntity,
    MessageId,
    MessageIdList,
    MessageListAdapter,
    OwnedGift,
    OwnedGiftAdapter,
    PassportElementError,
    Poll,
    PreparedInlineMessage,
    PreparedKeyboardButton,
    ReactionType,
    ReplyMarkup,
    ReplyParameters,
    SentGuestMessage,
    SentWebAppMessage,
    ShippingOption,
    StarAmount,
    StarTransactions,
    Sticker,
    StickerList,
    StickerSet,
    Story,
    StoryArea,
    SuggestedPostParameters,
    User,
    UserChatBoosts,
    UserProfileAudios,
    UserProfilePhotos,
)
from utils.load_env import env
from utils.logger import logger


class Telegram:
    """
    A fully typed and proxy-ready client for the Telegram Bot API (v9.2).
    Designed for clean, maintainable, and production-grade bot development.
    """

    HEADERS: Dict[str, str] = {"Cache-Control": "no-cache"}

    def __init__(self):
        self._validate_config()
        self.token = env.get("TOKEN")
        self.webhook = env.get("TM_WEBHOOK_URL")

        self.proxy = self._setup_proxy()
        self._session = requests.Session()
        self._session.headers.update(self.HEADERS)

    def _validate_config(self):
        """Ensure all required environment variables are present."""
        if not env.get("TOKEN"):
            raise ValueError("TOKEN is required in environment variables.")

        if not env.get("TM_WEBHOOK_URL"):
            raise ValueError("TM_WEBHOOK_URL is required in environment variables.")

    def _setup_proxy(self) -> Optional[Dict[str, str]]:
        """Configure SOCKS5 proxy if provided."""
        proxy_socks = env.get("PROXY_SOCKS")
        if proxy_socks:
            return {
                "http": f"socks5h://{proxy_socks}",
                "https": f"socks5h://{proxy_socks}",
            }
        return {}

    def _make_request(
        self,
        method_name: str,
        method: str = "POST",
        data: Optional[Dict[Any, Any]] = None,
        params: Optional[Dict[Any, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
    ) -> Dict[Any, Any]:
        """
        Send HTTP request to Telegram Bot API.
        """
        url = self.webhook + f"bot{self.token}/{method_name}"
        response = json.loads("{}")
        params = self._clean_dict(params)
        data = self._clean_dict(data)
        try:
            if method.upper() == "GET":
                response = self._session.get(
                    url, params=params, proxies=self.proxy, timeout=timeout
                )
            else:
                response = self._session.post(
                    url,
                    data=data,
                    params=params,
                    files=files,
                    timeout=100,
                    proxies=self.proxy,
                )

            json_data = response.json()

            if not json_data.get("ok", False):
                error_msg = json_data.get("description", "Unknown Telegram API error")
                logger.error(
                    f"Telegram API error | Method: {method_name} | Code: {json_data.get('error_code')} | Description: {error_msg}",
                )
                return {"ok": False, "error": error_msg}

            return json_data["result"]

        except Exception as e:
            logger.error(f"[Erro -> {method_name}]{response.json()}")
            return {"ok": False, "error": str(e)}

    def _clean_dict(self, data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Remove None values and convert nested dicts to JSON strings."""
        if data is None:
            return None

        cleaned = {}
        for key, value in data.items():
            if value is None:
                continue

            if hasattr(value, "model_dump"):
                value = value.model_dump(exclude_none=True)

            if isinstance(value, dict):
                cleaned[key] = json.dumps(value, ensure_ascii=False)
            else:
                cleaned[key] = value

        return cleaned

    def close(self):
        """Close the session."""
        self._session.close()

    def __enter__(self):
        response = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_me(self) -> User:
        response = self._make_request("getMe", method="GET")
        return User.model_validate(response)

    def send_message(
        self,
        chat_id: int | str,
        text: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        parse_mode: str | None = "html",
        entities: List[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a text message to a chat.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channel_username).
        :param text: Text of the message, 1-4096 characters after entities parsing.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier of the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic to send to (for direct messages chats).
        :param parse_mode: Mode for parsing entities in text ('HTML', 'MarkdownV2').
        :param entities: List of special entities (bold, links, etc.) in the message text.
        :param link_preview_options: Options for link preview generation.
        :param disable_notification: Send message silently (no notification sound).
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for a fee of 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (for private chats only).
        :param suggested_post_parameters: Parameters for a suggested post (monetized message).
        :param reply_parameters: Description of the message being replied to, with optional quoting.
        :param reply_markup: Inline or reply keyboard, or instructions to remove/force reply.
        :return: The sent Message object if successful, otherwise an error dictionary.
        """
        payload = {
            "chat_id": chat_id,
            "text": text,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "parse_mode": parse_mode,
            "entities": entities,
            "link_preview_options": link_preview_options,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        response = self._make_request("sendMessage", data=payload)
        message = Message.model_validate(response)
        return message

    def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        video_start_timestamp: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
    ) -> Message:
        """
        Forward a message of any kind.

        :param chat_id: Unique identifier for the target chat or username of the target channel (in format @channelusername).
        :param from_chat_id: Unique identifier for the source chat where the original message was sent.
        :param message_id: Identifier of the message to forward.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic to forward to; required if forwarding to a direct messages chat.
        :param video_start_timestamp: New start timestamp (in seconds) for the forwarded video.
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect the forwarded message from being forwarded or saved.
        :param suggested_post_parameters: Parameters for sending a suggested post; for direct messages chats only.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "video_start_timestamp": video_start_timestamp,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "suggested_post_parameters": suggested_post_parameters,
        }
        response = self._make_request("forwardMessage", data=payload)
        message = Message.model_validate(response)
        return message

    def forward_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: List[int],
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
    ) -> List[MessageId]:
        """
        Forward multiple messages of any kind at once.

        :param chat_id: Unique identifier for the target chat or username of the target channel (in format @channelusername).
        :param from_chat_id: Unique identifier for the source chat where the original messages were sent.
        :param message_ids: List of message IDs (1-100) to forward. Must be in strictly increasing order.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic to forward to; required if forwarding to a direct messages chat.
        :param disable_notification: Send messages silently without notification sound.
        :param protect_content: Protect the contents of the forwarded messages from forwarding and saving.
        :return: An array of MessageId objects for successfully sent messages.
        """
        payload = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_ids": json.dumps(message_ids),
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
        }
        response = self._make_request("forwardMessages", data=payload)
        return MessageIdList.validate_python(response or [])

    def copy_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        video_start_timestamp: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> MessageId:
        """
        Copy a message to another chat without a link to the original.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param from_chat_id: Unique identifier for the source chat where the original message was sent.
        :param message_id: Identifier of the message to copy.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic to send the message to; required if sending to a direct messages chat.
        :param video_start_timestamp: New start timestamp (in seconds) for the copied video.
        :param caption: New caption for media, 0–1024 characters. If not specified, the original caption is kept.
        :param parse_mode: Mode for parsing entities in the new caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the new caption (can be used instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the media.
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect the message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for a fee of 0.1 Stars per message.
        :param suggested_post_parameters: Parameters for sending a suggested post; for direct messages chats only.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Additional interface options (inline keyboard, reply keyboard, etc.).
        :return: A MessageId object on success.
        """
        payload = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "video_start_timestamp": video_start_timestamp,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("forwardMessage", data=payload)
        msg_id = MessageId.model_validate(response)
        return msg_id

    def copy_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: List[int],
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        remove_caption: bool | None = None,
    ) -> List[MessageId]:
        """
        Copy multiple messages to another chat without links to the originals.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param from_chat_id: Unique identifier for the source chat where the original messages were sent.
        :param message_ids: List of message IDs (1–100) to copy. Must be in strictly increasing order.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic to send messages to; required if sending to a direct messages chat.
        :param disable_notification: Send messages silently without notification sound.
        :param protect_content: Protect the contents of the sent messages from forwarding and saving.
        :param remove_caption: Pass True to copy messages without their captions.
        :return: An array of MessageId objects for successfully sent messages.
        """
        payload = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_ids": json.dumps(message_ids),
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "remove_caption": remove_caption,
        }
        response = self._make_request("copyMessages", data=payload)
        return MessageIdList.validate_python(response or [])

    def send_photo(
        self,
        chat_id: int | str,
        photo: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a photo to a chat. Uses GET for file_id/URL, POST for raw bytes.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param photo: Photo to send. Can be a file_id (str), URL (str), or raw bytes.
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param caption: Photo caption (0–1024 characters).
        :param parse_mode: Mode for parsing entities in caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption.
        :param show_caption_above_media: Show caption above the photo.
        :param has_spoiler: Cover photo with spoiler animation.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "has_spoiler": has_spoiler,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(photo, bytes):
            # Upload new photo → use POST + multipart/form-data
            files = {"photo": photo}
            payload["photo"] = None
            response = self._make_request(
                "sendPhoto", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["photo"] = photo
            response = self._make_request("sendPhoto", method="GET", params=payload)

        return Message.model_validate(response)

    def send_live_photo(
        self,
        chat_id: int | str,
        live_photo: InputFile | str,
        photo: InputFile | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Use this method to send live photos.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent.
        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        :param message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only.
        :param direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat.
        :param live_photo: Live photo video to send. The video must be no longer than 10 seconds and must not exceed 10 MB in size. Pass a file_id as String to send a video that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files ». Sending live photos by a URL is currently unsupported.
        :param photo: The static photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files ». Sending live photos by a URL is currently unsupported.
        :param caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing.
        :param parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
        :param caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode.
        :param show_caption_above_media: Pass True, if the caption must be shown above the message media.
        :param has_spoiler: Pass True if the video needs to be covered with a spoiler animation.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only.
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        :return: The sent Message object on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "live_photo": live_photo,
            "photo": photo,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "has_spoiler": has_spoiler,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(photo, bytes):
            # Upload new photo → use POST + multipart/form-data
            files = {"photo": photo}
            payload["photo"] = None
            response = self._make_request(
                "sendLivePhoto", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["photo"] = photo
            response = self._make_request("sendLivePhoto", method="GET", params=payload)

        return Message.model_validate(response)

    def send_audio(
        self,
        chat_id: int | str,
        audio: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        duration: int | None = None,
        performer: str | None = None,
        title: str | None = None,
        thumbnail: str | bytes | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send an audio file (e.g., music) to be displayed in the music player.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param audio: Audio file to send. Can be a file_id (str), URL (str), or raw bytes.
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param caption: Audio caption (0–1024 characters).
        :param parse_mode: Mode for parsing entities in caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption.
        :param duration: Duration of the audio in seconds.
        :param performer: Performer name.
        :param title: Track name.
        :param thumbnail: Thumbnail (JPEG <200KB, max 320x320). Use bytes or file_id.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "duration": duration,
            "performer": performer,
            "title": title,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(audio, bytes):
            # Upload new audio → use POST + multipart/form-data
            files = {"audio": audio}

            if isinstance(thumbnail, bytes):
                files["thumbnail"] = thumbnail
                payload["thumbnail"] = "attach://thumbnail"

            elif thumbnail:
                payload["thumbnail"] = thumbnail

            payload["audio"] = None
            response = self._make_request(
                "sendAudio", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["audio"] = audio
            if thumbnail:
                payload["thumbnail"] = thumbnail

            response = self._make_request("sendAudio", method="GET", params=payload)

        return Message.model_validate(response)

    def send_document(
        self,
        chat_id: int | str,
        document: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        thumbnail: str | bytes | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        disable_content_type_detection: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a general file to a chat. Uses GET for file_id/URL, POST for raw bytes.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param document: File to send. Can be a file_id (str), URL (str), or raw bytes.
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param thumbnail: Thumbnail of the file (JPEG <200KB, max 320x320). Use bytes or file_id.
        :param caption: Document caption (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption.
        :param disable_content_type_detection: Disable automatic content type detection for uploaded files.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "disable_content_type_detection": disable_content_type_detection,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(document, bytes):
            # Upload new document → use POST + multipart/form-data
            files = {"document": document}
            if isinstance(thumbnail, bytes):
                files["thumbnail"] = thumbnail
                payload["thumbnail"] = "attach://thumbnail"

            elif thumbnail:
                payload["thumbnail"] = thumbnail

            payload["document"] = None
            response = self._make_request(
                "sendDocument", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["document"] = document
            if thumbnail:
                payload["thumbnail"] = thumbnail

            response = self._make_request("sendDocument", method="GET", params=payload)

        return Message.model_validate(response)

    def send_video(
        self,
        chat_id: int | str,
        video: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: str | bytes | None = None,
        cover: str | bytes | None = None,
        start_timestamp: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        supports_streaming: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a video file to a chat. Uses GET for file_id/URL, POST for raw bytes.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param video: Video to send. Can be a file_id (str), URL (str), or raw bytes.
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param duration: Duration of the video in seconds.
        :param width: Video width.
        :param height: Video height.
        :param thumbnail: Thumbnail of the video (JPEG <200KB, max 320x320). Use bytes or file_id.
        :param cover: Cover image for the video in the message. Use file_id, URL, or attach://<name>.
        :param start_timestamp: Start timestamp for the video (in seconds).
        :param caption: Video caption (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption.
        :param show_caption_above_media: Show caption above the video.
        :param has_spoiler: Cover video with a spoiler animation.
        :param supports_streaming: Pass True if the video is suitable for streaming.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "duration": duration,
            "width": width,
            "height": height,
            "start_timestamp": start_timestamp,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "has_spoiler": has_spoiler,
            "supports_streaming": supports_streaming,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(video, bytes):
            # Upload new video → use POST + multipart/form-data
            files = {"video": video}
            if isinstance(thumbnail, bytes):
                files["thumbnail"] = thumbnail
                payload["thumbnail"] = "attach://thumbnail"

            elif thumbnail:
                payload["thumbnail"] = thumbnail

            if isinstance(cover, bytes):
                files["cover"] = cover
                payload["cover"] = "attach://cover"

            elif cover:
                payload["cover"] = cover

            payload["video"] = None
            response = self._make_request(
                "sendVideo", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["video"] = video
            if thumbnail:
                payload["thumbnail"] = thumbnail

            if cover:
                payload["cover"] = cover

            response = self._make_request("sendVideo", method="GET", params=payload)

        return Message.model_validate(response)

    def send_animation(
        self,
        chat_id: int | str,
        animation: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumbnail: str | bytes | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        has_spoiler: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send an animation file (GIF or H.264/MPEG-4 AVC video without sound).

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param animation: Animation to send. Can be a file_id (str), URL (str), or raw bytes.
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param duration: Duration of the animation in seconds.
        :param width: Animation width.
        :param height: Animation height.
        :param thumbnail: Thumbnail of the file (JPEG <200KB, max 320x320). Use bytes or file_id.
        :param caption: Animation caption (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption.
        :param show_caption_above_media: Show caption above the animation.
        :param has_spoiler: Cover animation with a spoiler animation.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "duration": duration,
            "width": width,
            "height": height,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "has_spoiler": has_spoiler,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(animation, bytes):
            # Upload new animation → use POST + multipart/form-data
            files = {"animation": animation}
            if isinstance(thumbnail, bytes):
                files["thumbnail"] = thumbnail
                payload["thumbnail"] = "attach://thumbnail"

            elif thumbnail:
                payload["thumbnail"] = thumbnail

            payload["animation"] = None
            response = self._make_request(
                "sendAnimation", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["animation"] = animation
            if thumbnail:
                payload["thumbnail"] = thumbnail

            response = self._make_request("sendAnimation", method="GET", params=payload)

        return Message.model_validate(response)

    def send_voice(
        self,
        chat_id: int | str,
        voice: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        duration: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a voice message (audio file displayed as voice message).

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param voice: Voice file to send. Can be a file_id (str), URL (str), or raw bytes (.OGG with OPUS, .MP3, .M4A).
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param caption: Voice message caption (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption.
        :param duration: Duration of the voice message in seconds.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "duration": duration,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(voice, bytes):
            # Upload new voice → use POST + multipart/form-data
            files = {"voice": voice}
            payload["voice"] = None
            response = self._make_request(
                "sendVoice", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use GET
            payload["voice"] = voice
            response = self._make_request("sendVoice", method="GET", params=payload)

        return Message.model_validate(response)

    def send_video_note(
        self,
        chat_id: int | str,
        video_note: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        duration: int | None = None,
        length: int | None = None,
        thumbnail: str | bytes | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a video note (round video message).

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param video_note: Video note to send. Can be a file_id (str) or raw bytes. Sending via URL is not supported.
        :param business_connection_id: Unique identifier of the business connection.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum.
        :param direct_messages_topic_id: Identifier of the direct messages topic.
        :param duration: Duration of the video in seconds.
        :param length: Diameter of the video message (width and height are equal).
        :param thumbnail: Thumbnail of the file (JPEG <200KB, max 320x320). Use bytes or file_id.
        :param disable_notification: Send silently.
        :param protect_content: Protect from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "duration": duration,
            "length": length,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        if isinstance(video_note, bytes):
            # Upload new video note → use POST + multipart/form-data
            files = {"video_note": video_note}
            if isinstance(thumbnail, bytes):
                files["thumbnail"] = thumbnail
                payload["thumbnail"] = "attach://thumbnail"

            elif thumbnail:
                payload["thumbnail"] = thumbnail

            payload["video_note"] = None
            response = self._make_request(
                "sendVideoNote", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id → use GET (URL not supported per API)
            payload["video_note"] = video_note
            if thumbnail:
                payload["thumbnail"] = thumbnail

            response = self._make_request("sendVideoNote", method="GET", params=payload)

        return Message.model_validate(response)

    def send_paid_media(
        self,
        chat_id: int | str,
        star_count: int,
        media: List[InputPaidMedia],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        payload: str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send paid media that requires Telegram Stars to access.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                    If the chat is a channel, proceeds go to the channel's balance; otherwise to the bot's balance.
        :param star_count: Number of Telegram Stars required to access the media (1–10000).
        :param media: A list of InputPaidMedia objects (e.g., photo, video) describing the media to send (up to 10 items).
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param payload: Bot-defined payload (0–128 bytes), not visible to user, for internal processing.
        :param caption: Caption for the media (0–1024 characters after entities parsing).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (can be used instead of parse_mode).
        :param show_caption_above_media: Show caption above the media.
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for a fee of 0.1 Stars per message.
        :param suggested_post_parameters: Parameters for sending a suggested post (for direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload_data = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "star_count": star_count,
            "media": json.dumps(media),
            "payload": payload,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendPaidMedia", method="POST", data=payload_data)
        return Message.model_validate(response)

    def send_media_group(
        self,
        chat_id: int | str,
        media: List[InputPaidMedia],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
    ) -> Message:
        """
        Send a group of photos, videos, documents, or audios as an album.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param media: A JSON-serialized array of InputMedia objects (photo, video, document, audio). Must contain 2–10 items.
                    All items must be of the same type if they are documents or audio.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the messages are sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param disable_notification: Send messages silently without notification sound.
        :param protect_content: Protect messages from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for a fee of 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (for private chats only).
        :param reply_parameters: Description of the message to reply to.
        :return: An array of sent Message objects on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "media": json.dumps(media),
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "reply_parameters": reply_parameters,
        }
        response = self._make_request("sendMediaGroup", method="POST", data=payload)
        return Message.model_validate(response)

    def send_location(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: int | None = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a point on the map.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param latitude: Latitude of the location.
        :param longitude: Longitude of the location.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param horizontal_accuracy: The radius of uncertainty for the location, in meters (0–1500).
        :param live_period: Period in seconds during which the location will be updated (60–86400 or 0x7FFFFFFF for indefinite).
        :param heading: Direction in which the user is moving, in degrees (1–360).
        :param proximity_alert_radius: Maximum distance for proximity alerts, in meters (1–100000).
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for a fee of 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (for private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post (for direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "latitude": latitude,
            "longitude": longitude,
            "horizontal_accuracy": horizontal_accuracy,
            "live_period": live_period,
            "heading": heading,
            "proximity_alert_radius": proximity_alert_radius,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendLocation", method="POST", data=payload)
        return Message.model_validate(response)

    def send_venue(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
        google_place_id: str | None = None,
        google_place_type: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send information about a venue.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param latitude: Latitude of the venue.
        :param longitude: Longitude of the venue.
        :param title: Name of the venue.
        :param address: Address of the venue.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param foursquare_id: Foursquare identifier of the venue.
        :param foursquare_type: Foursquare type of the venue (e.g., "arts_entertainment/aquarium").
        :param google_place_id: Google Places identifier of the venue.
        :param google_place_type: Google Places type of the venue.
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post (direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address,
            "foursquare_id": foursquare_id,
            "foursquare_type": foursquare_type,
            "google_place_id": google_place_id,
            "google_place_type": google_place_type,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendVenue", method="POST", data=payload)
        return Message.model_validate(response)

    def send_contact(
        self,
        chat_id: int | str,
        phone_number: str,
        first_name: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        last_name: str | None = None,
        vcard: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a phone contact.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param phone_number: Contact's phone number.
        :param first_name: Contact's first name.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param last_name: Contact's last name.
        :param vcard: Additional data about the contact in vCard format (0–2048 bytes).
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post (direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "vcard": vcard,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendContact", method="POST", data=payload)
        return Message.model_validate(response)

    def send_poll(
        self,
        chat_id: int | str,
        question: str,
        options: List[InputPollOption],
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        question_parse_mode: str | None = None,
        question_entities: List[MessageEntity] | None = None,
        is_anonymous: bool | None = None,
        poll_type: str | None = None,
        allows_revoting: bool | None = None,
        shuffle_options: bool | None = None,
        allows_multiple_answers: bool | None = None,
        allow_adding_options: bool | None = None,
        hide_results_until_closes: bool | None = None,
        members_only: bool | None = None,
        country_codes: List[str] | None = None,
        correct_option_ids: List[int] | None = None,
        explanation: str | None = None,
        explanation_parse_mode: str | None = None,
        explanation_entities: List[MessageEntity] | None = None,
        explanation_media: InputPollMedia | None = None,
        open_period: int | None = None,
        close_date: int | None = None,
        is_closed: bool | None = None,
        description: str | None = None,
        description_parse_mode: str | None = None,
        description_entities: List[MessageEntity] | None = None,
        media: InputPollMedia | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send a native poll.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                    Polls cannot be sent to channel direct messages chats.
        :param question: Poll question (1–300 characters).
        :param options: List of answer options (2–12 options, each 1–100 characters).
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param question_parse_mode: Mode for parsing entities in the question (only custom emoji allowed).
        :param question_entities: List of special entities in the question.
        :param is_anonymous: True if the poll is anonymous (default: True).
        :param poll_type: Poll type: "quiz" or "regular" (default: "regular").
        :param allows_revoting:Pass True, if the poll allows to change chosen answer options, defaults to False for quizzes and to True for regular polls.
        :param shuffle_options: Pass True, if the poll options must be shown in random order.
        :param allows_multiple_answers: True if multiple answers are allowed (ignored in quiz mode, default: False).
        :param allow_adding_options: Pass True, if answer options can be added to the poll after creation; not supported for anonymous polls and quizzes.
        :param hide_results_until_closes: Pass True, if poll results must be shown only after the poll closes.
        :param members_only: Pass True, if voting is limited to users who have been members of the chat where the poll is being sent for more than 24 hours; for channel chats only.
        :param country_codes: A JSON-serialized list of 0-12 two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which users can vote in the poll; for channel chats only. Use “FT” as a country code to allow users with anonymous numbers to vote. If omitted or empty, then users from any country can participate in the poll.
        :param correct_option_ids: Array of 0-based identifiers of the correct answer options. Available only for polls in quiz mode which are closed or were sent (not forwarded) by the bot or to the private chat with the bot.
        :param explanation: Text shown when an incorrect answer is chosen (0–200 characters).
        :param explanation_parse_mode: Mode for parsing entities in the explanation.
        :param explanation_entities: List of special entities in the explanation.
        :param explanation_media: Media added to the quiz explanation.
        :param open_period: Duration in seconds the poll will be active (5–600). Cannot be used with close_date.
        :param close_date: Unix timestamp when the poll will be automatically closed (5–600 seconds in future).
                        Cannot be used with open_period.
        :param is_closed: Pass True to immediately close the poll (useful for preview).
        :param description: Description of the poll to be sent, 0-1024 characters after entities parsing.
        :param description_parse_mode: Mode for parsing entities in the poll description. See formatting options for more details.
        :param description_entities: A JSON-serialized list of special entities that appear in the poll description, which can be specified instead of description_parse_mode.
        :param media: Media added to the poll description.
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "question": question,
            "options": json.dumps(options),
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "question_parse_mode": question_parse_mode,
            "question_entities": question_entities,
            "is_anonymous": is_anonymous,
            "poll_type": poll_type,
            "allows_revoting": allows_revoting,
            "shuffle_options": shuffle_options,
            "allows_multiple_answers": allows_multiple_answers,
            "allow_adding_options": allow_adding_options,
            "hide_results_until_closes": hide_results_until_closes,
            "members_only": members_only,
            "country_codes": country_codes,
            "correct_option_ids": correct_option_ids,
            "explanation": explanation,
            "explanation_parse_mode": explanation_parse_mode,
            "explanation_entities": explanation_entities,
            "explanation_media": explanation_media,
            "open_period": open_period,
            "close_date": close_date,
            "is_closed": is_closed,
            "description": description,
            "description_parse_mode": description_parse_mode,
            "description_entities": description_entities,
            "media": media,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendPoll", method="POST", data=payload)
        return Message.model_validate(response)

    def send_checklist(
        self,
        business_connection_id: str,
        chat_id: int,
        checklist: InputChecklist,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """
        Send a checklist on behalf of a connected business account.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent. Required.
        :param chat_id: Unique identifier for the target chat.
        :param checklist: A JSON-serialized object describing the checklist to send.
        :param disable_notification: Send message silently (no notification sound).
        :param protect_content: Protect message from forwarding and saving.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline keyboard markup.
        :return: The sent Message object on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "checklist": json.dumps(checklist),
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "message_effect_id": message_effect_id,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendChecklist", method="POST", data=payload)
        return Message.model_validate(response)

    def send_dice(
        self,
        chat_id: int | str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        emoji: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send an animated emoji that displays a random value (e.g., dice, target, slot machine).

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param emoji: Emoji for the animation. Must be one of: “🎲”, “🎯”, “🏀”, “⚽”, “🎳”, “🎰”. Defaults to “🎲”.
        :param disable_notification: Send message silently (no notification sound).
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post (direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "emoji": emoji,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendDice", method="POST", data=payload)
        return Message.model_validate(response)

    def send_message_draft(
        self,
        chat_id: int | str,
        draft_id: int,
        text: str,
        message_thread_id: int | None = None,
        parse_mode: str | None = "html",
        entities: List[MessageEntity] | None = None,
    ) -> bool:
        """
        Use this method to stream a partial message to a user while the message is being generated;
        supported only for bots with forum topic mode enabled.

        :param chat_id: Unique identifier for the target private chat.
        :param draft_id: Unique identifier of the message draft; must be non-zero. Changes of drafts with the same identifier are animated.
        :param text: Text of the message to be sent, 1-4096 characters after entities parsing.
        :param message_thread_id: Unique identifier for the target message thread.
        :param parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
        :param entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "draft_id": draft_id,
            "text": text,
            "message_thread_id": message_thread_id,
            "parse_mode": parse_mode,
            "entities": entities,
        }
        response = self._make_request("sendMessageDraft", method="POST", data=payload)
        return bool(response)

    def send_chat_action(
        self,
        chat_id: int | str,
        action: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
    ) -> bool:
        """
        Tell the user that something is happening on the bot's side (e.g., typing, uploading photo).

        :param chat_id: Unique identifier for the target chat or username of the target supergroup (e.g. @supergroupusername).
                        Channel chats and channel direct messages are not supported.
        :param action: Type of action to broadcast. Possible values:
                    'typing' - for text messages,
                    'upload_photo' - for photos,
                    'record_video', 'upload_video' - for videos,
                    'record_voice', 'upload_voice' - for voice notes,
                    'upload_document' - for general files,
                    'choose_sticker' - for stickers,
                    'find_location' - for location data,
                    'record_video_note', 'upload_video_note' - for video notes.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the action is sent.
        :param message_thread_id: Unique identifier for the target message thread; for supergroups only.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "action": action,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
        }
        response = self._make_request("sendChatAction", method="POST", data=payload)
        return bool(response)

    def set_message_reaction(
        self,
        chat_id: int | str,
        message_id: int,
        reaction: List[ReactionType] | None = None,
        is_big: bool | None = None,
    ) -> bool:
        """
        Change the chosen reactions on a message.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group.
        :param reaction: A JSON-serialized list of reaction types to set. Bots can set up to one reaction. Can be 'emoji' (e.g., "👍") or 'custom_emoji' with custom_emoji_id.
        :param is_big: Pass True to show the reaction with a big animation.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reaction": json.dumps(reaction) if reaction is not None else None,
            "is_big": is_big,
        }
        response = self._make_request("setMessageReaction", method="POST", data=payload)
        return bool(response)

    def get_user_profile_photos(
        self, user_id: int, offset: int | None = None, limit: int | None = None
    ) -> UserProfilePhotos:
        """
        Get a list of profile pictures for a user.

        :param user_id: Unique identifier of the target user.
        :param offset: Sequential number of the first photo to return. Defaults to 0 (all photos).
        :param limit: Limits the number of photos to retrieve (1–100). Defaults to 100.
        :return: A UserProfilePhotos object on success.
        """
        payload = {
            "user_id": user_id,
            "offset": offset,
            "limit": limit,
        }
        response = self._make_request(
            "getUserProfilePhotos", method="GET", params=payload
        )
        return UserProfilePhotos.model_validate(response)

    def get_user_profile_audios(
        self, user_id: int, offset: int | None = None, limit: int | None = None
    ) -> UserProfileAudios:
        """
        Use this method to get a list of profile audios for a user.

        :param user_id: Unique identifier of the target user.
        :param offset: Sequential number of the first photo to return. Defaults to 0 (all photos).
        :param limit: Limits the number of photos to retrieve (1–100). Defaults to 100.
        :return: A UserProfileAudios object.
        """
        payload = {
            "user_id": user_id,
            "offset": offset,
            "limit": limit,
        }
        response = self._make_request(
            "getUserProfileAudios", method="GET", params=payload
        )
        return UserProfileAudios.model_validate(response)

    def set_user_emoji_status(
        self,
        user_id: int,
        emoji_status_custom_emoji_id: str | None = None,
        emoji_status_expiration_date: int | None = None,
    ) -> bool:
        """
        Change the emoji status for a user who has granted the bot permission via requestEmojiStatusAccess.

        :param user_id: Unique identifier of the target user.
        :param emoji_status_custom_emoji_id: Custom emoji identifier for the status. Pass empty string to remove status.
        :param emoji_status_expiration_date: Unix timestamp when the emoji status should expire. Pass None for no expiration.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "emoji_status_custom_emoji_id": emoji_status_custom_emoji_id,
            "emoji_status_expiration_date": emoji_status_expiration_date,
        }
        response = self._make_request("setUserEmojiStatus", method="POST", data=payload)
        return bool(response)

    def get_file(self, file_id: str) -> File:
        """
        Get basic information about a file and prepare it for downloading.

        :param file_id: File identifier to get information about.
        :return: A File object on success. The file can be downloaded via https://api.telegram.org/file/bot<token>/<file_path>.
                The link is guaranteed to be valid for at least 1 hour.
        """
        payload = {"file_id": file_id}
        response = self._make_request("getFile", method="GET", params=payload)
        return File.model_validate(response)

    def set_chat_member_tag(self, chat_id: int | str, user_id: int, tag: str):
        """
        Use this method to set a tag for a regular member in a group or a supergroup.
        The bot must be an administrator in the chat for this to work and must
        have the can_manage_tags administrator right.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
        :param user_id: Unique identifier of the target user.
        :param tag: New tag for the member; 0-16 characters, emoji are not allowed.
        :return: True on success.
        """
        payload = {"chat_id": chat_id, "user_id": user_id, "tag": tag}
        response = self._make_request("setChatMemberTag", method="POST", data=payload)
        return bool(response)

    def ban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        until_date: int | None = None,
        revoke_messages: bool | None = None,
    ) -> bool:
        """
        Ban a user in a group, supergroup, or channel.
        In supergroups and channels, the user will not be able to return on their own unless unbanned.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param user_id: Unique identifier of the user to ban.
        :param until_date: Date when the user will be automatically unbanned (Unix timestamp).
                        If omitted or set to more than 366 days in the future, the ban is considered permanent.
                        Applied only to supergroups and channels.
        :param revoke_messages: Pass True to delete all messages from the chat for the user being removed.
                                If False, the user can still see messages sent before removal.
                                Always True for supergroups and channels.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "until_date": until_date,
            "revoke_messages": revoke_messages,
        }
        response = self._make_request("banChatMember", method="POST", data=payload)
        return bool(response)

    def unban_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        only_if_banned: bool | None = None,
    ) -> bool:
        """
        Unban a previously banned user in a supergroup or channel.
        The user won't rejoin automatically but can use invite links to join.
        If the user is currently a member, they will be removed from the chat unless only_if_banned is True.
        The bot must be an administrator.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param user_id: Unique identifier of the user to unban.
        :param only_if_banned: Do nothing if the user is not currently banned.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "only_if_banned": only_if_banned,
        }
        response = self._make_request("unbanChatMember", method="POST", data=payload)
        return bool(response)

    def restrict_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        permissions: Dict[str, Any],
        use_independent_chat_permissions: bool | None = None,
        until_date: int | None = None,
    ) -> bool:
        """
        Restrict a user in a supergroup.
        The bot must be an administrator with appropriate rights.
        Pass True for all permissions to lift restrictions.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param user_id: Unique identifier of the target user.
        :param permissions: A JSON-serialized ChatPermissions object specifying new permissions.
        :param use_independent_chat_permissions: Pass True if permissions should be applied independently.
                                                Otherwise, certain permissions imply others (e.g., can_send_polls implies can_send_messages).
        :param until_date: Date when restrictions will be lifted (Unix timestamp).
                        Permanent if more than 366 days in the future or less than 30 seconds from now.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": json.dumps(permissions),
            "use_independent_chat_permissions": use_independent_chat_permissions,
            "until_date": until_date,
        }
        response = self._make_request("restrictChatMember", method="POST", data=payload)
        return bool(response)

    def promote_chat_member(
        self,
        chat_id: int | str,
        user_id: int,
        is_anonymous: bool | None = None,
        can_manage_chat: bool | None = None,
        can_delete_messages: bool | None = None,
        can_manage_video_chats: bool | None = None,
        can_restrict_members: bool | None = None,
        can_promote_members: bool | None = None,
        can_change_info: bool | None = None,
        can_invite_users: bool | None = None,
        can_post_stories: bool | None = None,
        can_edit_stories: bool | None = None,
        can_delete_stories: bool | None = None,
        can_post_messages: bool | None = None,
        can_edit_messages: bool | None = None,
        can_pin_messages: bool | None = None,
        can_manage_topics: bool | None = None,
        can_manage_direct_messages: bool | None = None,
        can_manage_tags: bool | None = None,
    ) -> bool:
        """
        Promote or demote a user in a supergroup or channel.
        The bot must be an administrator with appropriate rights.
        Pass False for all parameters to demote the user.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param user_id: Unique identifier of the target user.
        :param is_anonymous: True if the administrator's presence is hidden.
        :param can_manage_chat: True if the admin can access chat event log, boost list, see hidden members, report spam, ignore slow mode, and send messages without Stars.
                                Implied by any other privilege.
        :param can_delete_messages: True if the admin can delete messages of other users.
        :param can_manage_video_chats: True if the admin can manage video chats.
        :param can_restrict_members: True if the admin can restrict, ban, or unban members, or access supergroup stats.
        :param can_promote_members: True if the admin can add new admins with subset of own privileges or demote those they promoted.
        :param can_change_info: True if the admin can change chat title, photo, and other settings.
        :param can_invite_users: True if the admin can invite new users.
        :param can_post_stories: True if the admin can post stories to the chat.
        :param can_edit_stories: True if the admin can edit others' stories, post stories to chat page, pin stories, and access archive.
        :param can_delete_stories: True if the admin can delete others' stories.
        :param can_post_messages: True if the admin can post messages in the channel, approve suggested posts, or access channel stats (channels only).
        :param can_edit_messages: True if the admin can edit messages of other users and pin messages (channels only).
        :param can_pin_messages: True if the admin can pin messages (supergroups only).
        :param can_manage_topics: True if the admin can create, rename, close, and reopen forum topics (supergroups only).
        :param can_manage_direct_messages: True if the admin can manage direct messages of the channel and decline suggested posts (channels only).
        :param can_manage_tags:Pass True if the administrator can edit the tags of regular members; for groups and supergroups only
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "is_anonymous": is_anonymous,
            "can_manage_chat": can_manage_chat,
            "can_delete_messages": can_delete_messages,
            "can_manage_video_chats": can_manage_video_chats,
            "can_restrict_members": can_restrict_members,
            "can_promote_members": can_promote_members,
            "can_change_info": can_change_info,
            "can_invite_users": can_invite_users,
            "can_post_stories": can_post_stories,
            "can_edit_stories": can_edit_stories,
            "can_delete_stories": can_delete_stories,
            "can_post_messages": can_post_messages,
            "can_edit_messages": can_edit_messages,
            "can_pin_messages": can_pin_messages,
            "can_manage_topics": can_manage_topics,
            "can_manage_direct_messages": can_manage_direct_messages,
            "can_manage_tags": can_manage_tags,
        }
        response = self._make_request("promoteChatMember", method="POST", data=payload)
        return bool(response)

    def set_chat_administrator_custom_title(
        self, chat_id: int | str, user_id: int, custom_title: str
    ) -> bool:
        """
        Set a custom title for an administrator in a supergroup promoted by the bot.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param user_id: Unique identifier of the target administrator.
        :param custom_title: New custom title for the administrator (0–16 characters, emoji not allowed).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "custom_title": custom_title,
        }
        response = self._make_request(
            "setChatAdministratorCustomTitle", method="POST", data=payload
        )
        return bool(response)

    def ban_chat_sender_chat(self, chat_id: int | str, sender_chat_id: int) -> bool:
        """
        Ban a channel chat in a supergroup or channel.
        After this, the channel's owner cannot post on behalf of that channel until it's unbanned.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param sender_chat_id: Unique identifier of the sender chat (i.e., the channel) to ban.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "sender_chat_id": sender_chat_id,
        }
        response = self._make_request("banChatSenderChat", method="POST", data=payload)
        return bool(response)

    def unban_chat_sender_chat(self, chat_id: int | str, sender_chat_id: int) -> bool:
        """
        Unban a previously banned channel chat in a supergroup or channel.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param sender_chat_id: Unique identifier of the sender chat (channel) to unban.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "sender_chat_id": sender_chat_id,
        }
        response = self._make_request(
            "unbanChatSenderChat", method="POST", data=payload
        )
        return bool(response)

    def set_chat_permissions(
        self,
        chat_id: int | str,
        permissions: ChatPermissions,
        use_independent_chat_permissions: bool | None = None,
    ) -> bool:
        """
        Set default chat permissions for all members in a group or supergroup.
        The bot must be an administrator with can_restrict_members right.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param permissions: A JSON-serialized ChatPermissions object defining default permissions.
        :param use_independent_chat_permissions: Whether permissions are applied independently.
                                                If False, some permissions imply others.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "permissions": json.dumps(permissions),
            "use_independent_chat_permissions": use_independent_chat_permissions,
        }
        response = self._make_request("setChatPermissions", method="POST", data=payload)
        return bool(response)

    def export_chat_invite_link(self, chat_id: int | str) -> str:
        """
        Generate a new primary invite link for a chat. Any previous primary link is revoked.
        The bot must be an administrator with appropriate rights.
        Each administrator (including bots) has their own invite links.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: The new invite link as a string on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "exportChatInviteLink", method="GET", params=payload
        )
        return str(response)

    def create_chat_invite_link(
        self,
        chat_id: int | str,
        name: str | None = None,
        expire_date: int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
    ) -> ChatInviteLink:
        """
        Create a new additional invite link for a chat.
        The link can be edited or revoked using editChatInviteLink or revokeChatInviteLink.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param name: Invite link name (0–32 characters).
        :param expire_date: Unix timestamp when the link will expire.
        :param member_limit: Maximum number of users that can join via this link (1–99999).
        :param creates_join_request: True if users must be approved by administrators to join.
                                    If True, member_limit cannot be specified.
        :return: The new ChatInviteLink object on success.
        """
        payload = {
            "chat_id": chat_id,
            "name": name,
            "expire_date": expire_date,
            "member_limit": member_limit,
            "creates_join_request": creates_join_request,
        }
        response = self._make_request(
            "createChatInviteLink", method="POST", data=payload
        )
        return ChatInviteLink.model_validate(response)

    def edit_chat_invite_link(
        self,
        chat_id: int | str,
        invite_link: str,
        name: str | None = None,
        expire_date: int | None = None,
        member_limit: int | None = None,
        creates_join_request: bool | None = None,
    ) -> ChatInviteLink:
        """
        Edit a non-primary invite link created by the bot.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param invite_link: The invite link to edit.
        :param name: New invite link name (0–32 characters).
        :param expire_date: New Unix timestamp when the link will expire.
        :param member_limit: New maximum number of users that can join via this link (1–99999).
        :param creates_join_request: True if users must be approved by administrators to join.
                                    If True, member_limit cannot be specified.
        :return: The edited ChatInviteLink object on success.
        """
        payload = {
            "chat_id": chat_id,
            "invite_link": invite_link,
            "name": name,
            "expire_date": expire_date,
            "member_limit": member_limit,
            "creates_join_request": creates_join_request,
        }
        response = self._make_request("editChatInviteLink", method="POST", data=payload)
        return ChatInviteLink.model_validate(response)

    def create_chat_subscription_invite_link(
        self,
        chat_id: int | str,
        subscription_period: int,
        subscription_price: int,
        name: str | None = None,
    ) -> ChatInviteLink:
        """
        Create a subscription invite link for a channel.
        Users must pay Telegram Stars to join via this link.
        The bot must have the 'can_invite_users' administrator right.

        :param chat_id: Unique identifier for the target channel or username (e.g. @channelusername).
        :param subscription_period: Duration of the subscription in seconds. Must be 2592000 (30 days).
        :param subscription_price: Amount of Telegram Stars required (1–10000).
        :param name: Invite link name (0–32 characters).
        :return: The new ChatInviteLink object on success.
        """
        payload = {
            "chat_id": chat_id,
            "name": name,
            "subscription_period": subscription_period,
            "subscription_price": subscription_price,
        }
        response = self._make_request(
            "createChatSubscriptionInviteLink", method="POST", data=payload
        )
        return ChatInviteLink.model_validate(response)

    def edit_chat_subscription_invite_link(
        self, chat_id: int | str, invite_link: str, name: str | None = None
    ) -> ChatInviteLink:
        """
        Edit a subscription invite link created by the bot.
        The bot must have the 'can_invite_users' administrator right.

        :param chat_id: Unique identifier for the target channel or username (e.g. @channelusername).
        :param invite_link: The subscription invite link to edit.
        :param name: New invite link name (0–32 characters).
        :return: The edited ChatInviteLink object on success.
        """
        payload = {
            "chat_id": chat_id,
            "invite_link": invite_link,
            "name": name,
        }
        response = self._make_request(
            "editChatSubscriptionInviteLink", method="POST", data=payload
        )
        return ChatInviteLink.model_validate(response)

    def revoke_chat_invite_link(
        self, chat_id: int | str, invite_link: str
    ) -> ChatInviteLink:
        """
        Revoke an invite link created by the bot.
        If the primary link is revoked, a new one is automatically generated.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param invite_link: The invite link to revoke.
        :return: The revoked ChatInviteLink object on success.
        """
        payload = {
            "chat_id": chat_id,
            "invite_link": invite_link,
        }
        response = self._make_request(
            "revokeChatInviteLink", method="POST", data=payload
        )
        return ChatInviteLink.model_validate(response)

    def approve_chat_join_request(self, chat_id: int | str, user_id: int) -> bool:
        """
        Approve a user's request to join a chat.
        The bot must be an administrator with the 'can_invite_users' right.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param user_id: Unique identifier of the user whose join request is approved.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        response = self._make_request(
            "approveChatJoinRequest", method="POST", data=payload
        )
        return bool(response)

    def decline_chat_join_request(self, chat_id: int | str, user_id: int) -> bool:
        """
        Decline a user's request to join a chat.
        The bot must be an administrator with the 'can_invite_users' right.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param user_id: Unique identifier of the user whose join request is declined.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        response = self._make_request(
            "declineChatJoinRequest", method="POST", data=payload
        )
        return bool(response)

    def answer_chat_join_request_query(
        self, chat_join_request_query_id: str, result: str
    ) -> bool:
        """
        Use this method to process a received chat join request query.

        :param chat_join_request_query_id: Unique identifier of the join request query.
        :param result: Result of the query. Must be either “approve” to allow the user to join the chat, “decline” to disallow the user to join the chat, or “queue” to leave the decision to other administrators.
        :return: True on success.
        """
        payload = {
            "chat_join_request_query_id": chat_join_request_query_id,
            "result": result,
        }
        response = self._make_request(
            "answerChatJoinRequestQuery", method="POST", data=payload
        )
        return bool(response)

    def send_chat_join_request_web_app(
        self, chat_join_request_query_id: str, web_app_url: str
    ) -> bool:
        """
        Use this method to process a received chat join request query by
        showing a Mini App to the user before deciding the outcome.

        :param chat_join_request_query_id: Unique identifier of the join request query.
        :param web_app_url: The URL of the Mini App to be opened.
        :return: True on success.
        """
        payload = {
            "chat_join_request_query_id": chat_join_request_query_id,
            "web_app_url": web_app_url,
        }
        response = self._make_request(
            "sendChatJoinRequestWebApp", method="POST", data=payload
        )
        return bool(response)

    def set_chat_photo(self, chat_id: int | str, photo: bytes) -> bool:
        """
        Set a new profile photo for the chat.
        Not available for private chats.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param photo: New chat photo, uploaded as bytes using multipart/form-data.
        :return: True on success.
        """
        files = {"photo": photo}
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "setChatPhoto", method="POST", data=payload, files=files
        )
        return bool(response)

    def delete_chat_photo(self, chat_id: int | str) -> bool:
        """
        Delete the current profile photo of the chat.
        Not available for private chats.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request("deleteChatPhoto", method="POST", data=payload)
        return bool(response)

    def set_chat_title(self, chat_id: int | str, title: str) -> bool:
        """
        Change the title of a chat.
        Not available for private chats.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param title: New chat title (1–128 characters).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "title": title,
        }
        response = self._make_request("setChatTitle", method="POST", data=payload)
        return bool(response)

    def set_chat_description(
        self, chat_id: int | str, description: str | None = None
    ) -> bool:
        """
        Change the description of a group, supergroup, or channel.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param description: New chat description (0–255 characters). Pass empty string to remove.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "description": description,
        }

        response = self._make_request("setChatDescription", method="POST", data=payload)
        return bool(response)

    def pin_chat_message(
        self,
        chat_id: int | str,
        message_id: int,
        business_connection_id: str | None = None,
        disable_notification: bool | None = None,
    ) -> bool:
        """
        Pin a message in a chat.
        In groups and channels, the bot must have 'can_pin_messages' or 'can_edit_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param message_id: Identifier of the message to pin.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is pinned.
        :param disable_notification: Pass True to disable notification for all members about the new pinned message.
                                    Always disabled in channels and private chats.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "business_connection_id": business_connection_id,
            "disable_notification": disable_notification,
        }
        response = self._make_request("pinChatMessage", method="POST", data=payload)
        return bool(response)

    def unpin_chat_message(
        self,
        chat_id: int | str,
        message_id: int | None = None,
        business_connection_id: str | None = None,
    ) -> bool:
        """
        Unpin a specific message in a chat.
        If message_id is not specified, the most recent pinned message is unpinned.
        The bot must have appropriate rights in groups and channels.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param message_id: Identifier of the message to unpin. Required if business_connection_id is used.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is unpinned.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "business_connection_id": business_connection_id,
        }
        response = self._make_request("unpinChatMessage", method="POST", data=payload)
        return bool(response)

    def unpin_all_chat_messages(self, chat_id: int | str) -> bool:
        """
        Clear all pinned messages in a chat.
        No special rights needed in private chats or channel direct messages.
        In groups and channels, the bot must have 'can_pin_messages' or 'can_edit_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "unpinAllChatMessages", method="POST", data=payload
        )
        return bool(response)

    def leave_chat(self, chat_id: int | str) -> bool:
        """
        Make the bot leave a group, supergroup, or channel.
        Channel direct messages chats are not supported; leave the corresponding channel instead.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request("leaveChat", method="POST", data=payload)
        return bool(response)

    def get_chat(self, chat_id: int | str) -> ChatFullInfo:
        """
        Get up-to-date information about a chat (group, supergroup, channel, or private chat).
        Returns a ChatFullInfo object.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: A ChatFullInfo object on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request("getChat", method="GET", params=payload)
        return ChatFullInfo.model_validate(response)

    def get_chat_administrators(
        self, chat_id: int | str, return_bots: bool = False
    ) -> ChatMember:
        """
        Use this method to get a list of administrators in a chat.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param return_bots: Pass True to additionally receive all bots that are administrators of the chat. By default, bots other than the current bot are omitted.
        :return: Array of ChatMember objects on success.
        """
        payload = {"chat_id": chat_id, "return_bots": return_bots}
        response = self._make_request(
            "getChatAdministrators", method="GET", params=payload
        )
        return ChatMemberAdapter.validate_python(response)

    def get_chat_member_count(self, chat_id: int | str) -> int:
        """
        Get the number of members in a chat.
        Returns an integer on success.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: Number of members in the chat.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "getChatMemberCount", method="GET", params=payload
        )
        return cast(int, response)

    def get_user_personal_chat_messages(
        self, user_id: int, limit: int
    ) -> List[Message]:
        """
        Use this method to get the last messages from the personal chat
        (i.e., the chat currently added to their profile) of a given user

        :param user_id: Unique identifier for the target user.
        :param limit: The maximum number of messages to return; 1-20.
        :return: Aarray of Message objects is returned.
        """
        payload = {"user_id": user_id, "limit": limit}
        response = self._make_request(
            "getUserPersonalChatMessages", method="GET", params=payload
        )
        return MessageListAdapter.validate_python(response)

    def get_chat_member(self, chat_id: int | str, user_id: int) -> ChatMember:
        """
        Get information about a specific member of a chat.
        Guaranteed to work for other users only if the bot is an administrator.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param user_id: Unique identifier of the target user.
        :return: A ChatMember object on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        response = self._make_request("getChatMember", method="GET", params=payload)
        return ChatMemberAdapter.validate_python(response)

    def set_chat_sticker_set(self, chat_id: int | str, sticker_set_name: str) -> bool:
        """
        Set a new group sticker set for a supergroup.
        The bot must be an administrator with appropriate rights.
        Use getChat to check if the bot can_set_sticker_set.

        :param chat_id: Unique identifier for the target supergroup or username (e.g. @supergroupusername).
        :param sticker_set_name: Name of the sticker set to set as the group sticker set.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "sticker_set_name": sticker_set_name,
        }
        response = self._make_request("setChatStickerSet", method="POST", data=payload)
        return bool(response)

    def delete_chat_sticker_set(self, chat_id: int | str) -> bool:
        """
        Delete the group sticker set from a supergroup.
        The bot must be an administrator with appropriate rights.
        Use getChat to check if the bot can_set_sticker_set.

        :param chat_id: Unique identifier for the target supergroup or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "deleteChatStickerSet", method="POST", data=payload
        )
        return bool(response)

    def get_forum_topic_icon_stickers(self) -> List[Sticker]:
        """
        Get custom emoji stickers that can be used as forum topic icons by any user.
        This method requires no parameters.

        :return: An Array of Sticker objects on success.
        """
        response = self._make_request("getForumTopicIconStickers", method="GET")
        return StickerList.validate_python(response)

    def create_forum_topic(
        self,
        chat_id: int | str,
        name: str,
        icon_color: int | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> ForumTopic:
        """
        Create a new topic in a forum supergroup chat.
        The bot must be an administrator with 'can_manage_topics' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param name: Name of the new topic (1–128 characters).
        :param icon_color: Color of the topic icon in RGB format. Must be one of:
                        7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB),
                        9367192 (0x8EEE98), 16749490 (0xFF93B2), 16478047 (0xFB6F5F).
        :param icon_custom_emoji_id: Unique identifier of a custom emoji to use as the topic icon.
                                    Use get_forum_topic_icon_stickers() to get allowed identifiers.
        :return: A ForumTopic object containing information about the created topic.
        """
        payload = {
            "chat_id": chat_id,
            "name": name,
            "icon_color": icon_color,
            "icon_custom_emoji_id": icon_custom_emoji_id,
        }
        response = self._make_request("createForumTopic", method="POST", data=payload)
        return ForumTopic.model_validate(response)

    def edit_forum_topic(
        self,
        chat_id: int | str,
        message_thread_id: int,
        name: str | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> bool:
        """
        Edit the name and/or icon of a forum topic.
        The bot must be an administrator with 'can_manage_topics' rights, unless it's the topic creator.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param message_thread_id: Unique identifier for the target message thread (topic).
        :param name: New name for the topic (0–128 characters). If empty, name remains unchanged.
        :param icon_custom_emoji_id: New custom emoji identifier for the icon.
                                    Pass empty string to remove the icon.
                                    If not specified, icon remains unchanged.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "name": name,
            "icon_custom_emoji_id": icon_custom_emoji_id,
        }
        response = self._make_request("editForumTopic", method="POST", data=payload)
        return bool(response)

    def close_forum_topic(self, chat_id: int | str, message_thread_id: int) -> bool:
        """
        Close an open forum topic.
        The bot must be an administrator with 'can_manage_topics' rights, unless it's the topic creator.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param message_thread_id: Unique identifier for the target message thread (topic).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
        }
        response = self._make_request("closeForumTopic", method="POST", data=payload)
        return bool(response)

    def reopen_forum_topic(self, chat_id: int | str, message_thread_id: int) -> bool:
        """
        Reopen a closed forum topic.
        The bot must be an administrator with 'can_manage_topics' rights, unless it's the topic creator.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param message_thread_id: Unique identifier for the target message thread (topic).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
        }
        response = self._make_request("reopenForumTopic", method="POST", data=payload)
        return bool(response)

    def delete_forum_topic(self, chat_id: int | str, message_thread_id: int) -> bool:
        """
        Delete a forum topic along with all its messages.
        The bot must be an administrator with 'can_delete_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param message_thread_id: Unique identifier for the target message thread (topic).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
        }
        response = self._make_request("deleteForumTopic", method="POST", data=payload)
        return bool(response)

    def unpin_all_forum_topic_messages(
        self, chat_id: int | str, message_thread_id: int
    ) -> bool:
        """
        Clear the list of pinned messages in a specific forum topic.
        The bot must be an administrator with 'can_pin_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param message_thread_id: Unique identifier for the target message thread (topic).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
        }
        response = self._make_request(
            "unpinAllForumTopicMessages", method="POST", data=payload
        )
        return bool(response)

    def edit_general_forum_topic(self, chat_id: int | str, name: str) -> bool:
        """
        Edit the name of the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :param name: New name for the 'General' topic (1–128 characters).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "name": name,
        }
        response = self._make_request(
            "editGeneralForumTopic", method="POST", data=payload
        )
        return bool(response)

    def close_general_forum_topic(self, chat_id: int | str) -> bool:
        """
        Close the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "closeGeneralForumTopic", method="POST", data=payload
        )
        return bool(response)

    def reopen_general_forum_topic(self, chat_id: int | str) -> bool:
        """
        Reopen a closed 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.
        If the topic was hidden, it will be automatically unhidden.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "reopenGeneralForumTopic", method="POST", data=payload
        )
        return bool(response)

    def hide_general_forum_topic(self, chat_id: int | str) -> bool:
        """
        Hide the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.
        The topic will be automatically closed if it was open.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "hideGeneralForumTopic", method="POST", data=payload
        )
        return bool(response)

    def unhide_general_forum_topic(self, chat_id: int | str) -> bool:
        """
        Unhide the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "unhideGeneralForumTopic", method="POST", data=payload
        )
        return bool(response)

    def unpin_all_general_forum_topic_messages(self, chat_id: int | str) -> bool:
        """
        Clear the list of pinned messages in the 'General' forum topic.
        The bot must be an administrator with 'can_pin_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "unpinAllGeneralForumTopicMessages", method="POST", data=payload
        )
        return bool(response)

    def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> bool:
        """
        Send an answer to a callback query sent from an inline keyboard.
        The answer will be displayed to the user as a notification or an alert.

        :param callback_query_id: Unique identifier for the query to be answered.
        :param text: Text of the notification. If not specified, nothing is shown to the user (0–200 characters).
        :param show_alert: If True, an alert is shown instead of a notification at the top of the chat screen. Defaults to False.
        :param url: URL to be opened by the user's client. Use for games (created via @BotFather) or deep linking (e.g., t.me/your_bot?start=XXXX).
        :param cache_time: Maximum amount of time in seconds that the result may be cached client-side. Defaults to 0.
        :return: True on success.
        """
        payload = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert,
            "url": url,
            "cache_time": cache_time,
        }

        response = self._make_request(
            "answerCallbackQuery", method="POST", data=payload
        )
        return bool(response)

    def answer_guest_query(
        self, guest_query_id: str, result: InlineQueryResult
    ) -> SentGuestMessage:
        """
        Use this method to reply to a received guest message.

        :param guest_query_id: Unique identifier for the query to be answered.
        :param result: A JSON-serialized object describing the message to be sent.
        :return: SentGuestMessage object on success.
        """
        payload = {"guest_query_id": guest_query_id, "result": result}

        response = self._make_request("answerGuestQuery", method="POST", data=payload)
        return SentGuestMessage.model_validate(response)

    def get_user_chat_boosts(self, chat_id: int | str, user_id: int) -> UserChatBoosts:
        """
        Get the list of boosts added to a chat by a user.
        The bot must have administrator rights in the chat.

        :param chat_id: Unique identifier for the chat or username of the channel (e.g. @channelusername).
        :param user_id: Unique identifier of the target user.
        :return: A UserChatBoosts object on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        response = self._make_request("getUserChatBoosts", method="GET", params=payload)
        return UserChatBoosts.model_validate(response)

    def get_business_connection(
        self, business_connection_id: str
    ) -> BusinessConnection:
        """
        Get information about the connection of the bot with a business account.

        :param business_connection_id: Unique identifier of the business connection.
        :return: A BusinessConnection object on success.
        """
        payload = {"business_connection_id": business_connection_id}
        response = self._make_request(
            "getBusinessConnection", method="GET", params=payload
        )
        return BusinessConnection.model_validate(response)

    def get_managed_bot_token(self, user_id: int) -> str:
        """
        Use this method to get the token of a managed bot.

        :param user_id: User identifier of the managed bot whose token will be returned.
        :return: The token as String on success.
        """
        payload = {"user_id": user_id}
        response = self._make_request(
            "getManagedBotToken", method="GET", params=payload
        )
        return str(response)

    def replace_managed_bot_token(self, user_id: int) -> str:
        """
        Use this method to revoke the current token of a managed bot and generate a new one.

        :param user_id: User identifier of the managed bot whose token will be replaced.
        :return: New token as String on success.
        """
        payload = {"user_id": user_id}
        response = self._make_request(
            "replaceManagedBotToken", method="POST", data=payload
        )
        return str(response)

    def get_managed_bot_access_settings(self, user_id: int) -> BotAccessSettings:
        """
        Use this method to get the access settings of a managed bot.

        :param user_id: User identifier of the managed bot whose access settings will be returned.
        :return: BotAccessSettings object on success.
        """
        payload = {"user_id": user_id}
        response = self._make_request(
            "getManagedBotAccessSettings", method="GET", params=payload
        )
        return BotAccessSettings.model_validate(response)

    def set_managed_bot_access_settings(
        self, user_id: int, is_access_restricted: bool, added_user_ids: List[int]
    ) -> bool:
        """
        Use this method to change the access settings of a managed bot.

        :param user_id: User identifier of the managed bot whose access settings will be changed.
        :param is_access_restricted: Pass True, if only selected users can access the bot. The bot's owner can always access it.
        :param added_user_ids: A JSON-serialized list of up to 10 identifiers of users who will have access to the bot in addition to its owner. Ignored if is_access_restricted is false.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "is_access_restricted": is_access_restricted,
            "added_user_ids": added_user_ids,
        }
        response = self._make_request(
            "setManagedBotAccessSettings", method="POST", data=payload
        )
        return bool(response)

    def set_my_commands(
        self,
        commands: BotCommand,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> bool:
        """
        Change the list of the bot's commands.

        :param commands: A list of BotCommand objects (JSON-serialized), at most 100.
        :param scope: A JSON-serialized BotCommandScope object. Defaults to BotCommandScopeDefault.
        :param language_code: A two-letter ISO 639-1 language code. If empty, commands apply to all users in the scope without a dedicated language command.
        :return: True on success.
        """
        payload = {
            "commands": json.dumps(commands),
            "scope": json.dumps(scope) if scope is not None else None,
            "language_code": language_code,
        }
        response = self._make_request("setMyCommands", method="POST", data=payload)
        return bool(response)

    def delete_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> bool:
        """
        Delete the list of the bot's commands for the given scope and language.
        After deletion, higher-level commands will be used.

        :param scope: A JSON-serialized BotCommandScope object. Defaults to BotCommandScopeDefault.
        :param language_code: A two-letter ISO 639-1 language code. If empty, applies to all users in the scope without a dedicated command.
        :return: True on success.
        """
        payload = {
            "scope": json.dumps(scope) if scope is not None else None,
            "language_code": language_code,
        }
        response = self._make_request("deleteMyCommands", method="POST", data=payload)
        return bool(response)

    def get_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> List[BotCommand]:
        """
        Get the current list of the bot's commands for the given scope and language.

        :param scope: A JSON-serialized BotCommandScope object. Defaults to BotCommandScopeDefault.
        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: An array of BotCommand objects. Empty if no commands are set.
        """
        payload = {
            "scope": json.dumps(scope) if scope is not None else None,
            "language_code": language_code,
        }

        response = self._make_request("getMyCommands", method="GET", params=payload)
        return BotCommandList.validate_python(response)

    def set_my_name(
        self, name: str | None = None, language_code: str | None = None
    ) -> bool:
        """
        Change the bot's name.

        :param name: New bot name (0–64 characters). Pass empty string to remove the name for the given language.
        :param language_code: A two-letter ISO 639-1 language code. If empty, name applies to all users without a dedicated name.
        :return: True on success.
        """
        payload = {
            "name": name,
            "language_code": language_code,
        }
        response = self._make_request("setMyName", method="POST", data=payload)
        return bool(response)

    def get_my_name(self, language_code: str | None = None) -> BotName:
        """
        Get the current bot name for the given user language.

        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: A BotName object on success.
        """
        payload = {"language_code": language_code}
        response = self._make_request("getMyName", method="GET", params=payload)
        return BotName.model_validate(response)

    def set_my_description(
        self, description: str | None = None, language_code: str | None = None
    ) -> bool:
        """
        Change the bot's description shown in the chat when it's empty.

        :param description: New bot description (0–512 characters). Pass empty string to remove for the given language.
        :param language_code: A two-letter ISO 639-1 language code. If empty, applies to all users without a dedicated description.
        :return: True on success.
        """
        payload = {
            "description": description,
            "language_code": language_code,
        }

        response = self._make_request("setMyDescription", method="POST", data=payload)
        return bool(response)

    def get_my_description(self, language_code: str | None = None) -> BotDescription:
        """
        Get the current bot description for the given user language.

        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: A BotDescription object on success.
        """
        payload = {"language_code": language_code}
        response = self._make_request("getMyDescription", method="GET", params=payload)
        return BotDescription.model_validate(response)

    def set_my_short_description(
        self,
        short_description: str | None = None,
        language_code: str | None = None,
    ) -> bool:
        """
        Change the bot's short description shown on the profile and when shared.

        :param short_description: New short description (0–120 characters). Pass empty string to remove for the given language.
        :param language_code: A two-letter ISO 639-1 language code. If empty, applies to all users without a dedicated short description.
        :return: True on success.
        """
        payload = {
            "short_description": short_description,
            "language_code": language_code,
        }
        response = self._make_request(
            "setMyShortDescription", method="POST", data=payload
        )
        return bool(response)

    def get_my_short_description(
        self, language_code: str | None = None
    ) -> BotShortDescription:
        """
        Get the current bot short description for the given user language.

        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: A BotShortDescription object on success.
        """
        payload = {"language_code": language_code}

        response = self._make_request(
            "getMyShortDescription", method="GET", params=payload
        )
        return BotShortDescription.model_validate(response)

    def set_my_profile_photo(self, photo: InputProfilePhoto) -> bool:
        """
        Changes the profile photo of the bot.

        :param photo: The new profile photo to set.
        :return: True on success.
        """
        payload = {"photo": photo}
        response = self._make_request("setMyProfilePhoto", method="POST", data=payload)
        return bool(response)

    def remove_my_profile_photo(self) -> bool:
        """
        Removes the profile photo of the bot. Requires no parameters.

        :return: True on success.
        """
        response = self._make_request("removeMyProfilePhoto", method="POST")
        return bool(response)

    def set_chat_menu_button(
        self,
        chat_id: int | None = None,
        menu_button: MenuButton | None = None,
    ) -> bool:
        """
        Change the bot's menu button in a private chat or the default menu button.

        :param chat_id: Unique identifier for the target private chat. If not specified, changes the default menu button.
        :param menu_button: A JSON-serialized MenuButton object. Defaults to MenuButtonDefault.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "menu_button": menu_button,
        }
        response = self._make_request("setChatMenuButton", method="POST", data=payload)
        return bool(response)

    def get_chat_menu_button(self, chat_id: int | None = None) -> MenuButton:
        """
        Get the current value of the bot's menu button in a private chat or the default.

        :param chat_id: Unique identifier for the target private chat. If not specified, returns the default menu button.
        :return: A MenuButton object on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request("getChatMenuButton", method="GET", params=payload)
        return MenuButtonAdapter.validate_python(response)

    def set_my_default_administrator_rights(
        self,
        rights: ChatAdministratorRights | None = None,
        for_channels: bool | None = None,
    ) -> bool:
        """
        Change the default administrator rights requested when the bot is added to groups or channels.

        :param rights: A JSON-serialized ChatAdministratorRights object. If not specified, rights are cleared.
        :param for_channels: Pass True to change rights for channels. Otherwise, for groups/supergroups.
        :return: True on success.
        """
        payload = {
            "rights": json.dumps(rights) if rights is not None else None,
            "for_channels": for_channels,
        }
        response = self._make_request(
            "setMyDefaultAdministratorRights", method="POST", data=payload
        )
        return bool(response)

    def get_my_default_administrator_rights(
        self, for_channels: bool | None = None
    ) -> ChatAdministratorRights:
        """
        Get the current default administrator rights of the bot.

        :param for_channels: Pass True to get rights for channels. Otherwise, for groups/supergroups.
        :return: A ChatAdministratorRights object on success.
        """
        payload = {"for_channels": for_channels}
        response = self._make_request(
            "getMyDefaultAdministratorRights", method="GET", params=payload
        )
        return ChatAdministratorRights.model_validate(response)

    def get_available_gifts(self) -> Gift:
        """
        Get the list of gifts that can be sent by the bot to users and channel chats.

        :return: A Gifts object on success.
        """
        response = self._make_request("getAvailableGifts", method="GET")
        return Gift.model_validate(response)

    def send_gift(
        self,
        gift_id: str,
        user_id: int | None = None,
        chat_id: int | str | None = None,
        pay_for_upgrade: bool | None = None,
        text: str | None = None,
        text_parse_mode: str | None = None,
        text_entities: List[MessageEntity] | None = None,
    ) -> bool:
        """
        Send a gift to a user or channel chat. The gift cannot be converted to Telegram Stars.

        :param gift_id: Identifier of the gift to send.
        :param user_id: Unique identifier of the target user. Required if chat_id is not specified.
        :param chat_id: Unique identifier or username of the target channel. Required if user_id is not specified.
        :param pay_for_upgrade: Pass True to pay for the gift upgrade from the bot's balance (free for receiver).
        :param text: Text to show with the gift (0–128 characters).
        :param text_parse_mode: Mode for parsing entities in the text (e.g., 'HTML', 'MarkdownV2').
        :param text_entities: List of special entities in the text (can be used instead of parse_mode).
                            Only bold, italic, underline, strikethrough, spoiler, and custom_emoji are allowed.
        :return: True on success.
        """
        if not (user_id or chat_id):
            raise ValueError("Either user_id or chat_id must be provided.")

        payload = {
            "user_id": user_id,
            "chat_id": chat_id,
            "gift_id": gift_id,
            "pay_for_upgrade": pay_for_upgrade,
            "text": text,
            "text_parse_mode": text_parse_mode,
            "text_entities": text_entities,
        }
        response = self._make_request("sendGift", method="POST", data=payload)
        return bool(response)

    def gift_premium_subscription(
        self,
        user_id: int,
        month_count: int,
        star_count: int,
        text: str | None = None,
        text_parse_mode: str | None = None,
        text_entities: List[MessageEntity] | None = None,
    ) -> bool:
        """
        Gift a Telegram Premium subscription to a user.

        :param user_id: Unique identifier of the target user who will receive the subscription.
        :param month_count: Number of months the subscription will be active. Must be one of: 3, 6, or 12.
        :param star_count: Number of Telegram Stars to pay. Must be 1000 (3 months), 1500 (6 months), or 2500 (12 months).
        :param text: Text to show with the service message (0–128 characters).
        :param text_parse_mode: Mode for parsing entities in the text ('HTML', 'MarkdownV2').
                                Only bold, italic, underline, strikethrough, spoiler, and custom_emoji are allowed.
        :param text_entities: List of special entities in the text (can be used instead of parse_mode).
                            Same restrictions apply as with text_parse_mode.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "month_count": month_count,
            "star_count": star_count,
            "text": text,
            "text_parse_mode": text_parse_mode,
            "text_entities": text_entities,
        }
        response = self._make_request(
            "giftPremiumSubscription", method="POST", data=payload
        )
        return bool(response)

    def verify_user(self, user_id: int, custom_description: str | None = None) -> bool:
        """
        Verify a user on behalf of the organization represented by the bot.

        :param user_id: Unique identifier of the target user.
        :param custom_description: Custom description for the verification (0–70 characters).
                                Must be empty if the organization isn't allowed to set a custom description.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "custom_description": custom_description,
        }
        response = self._make_request("verifyUser", method="POST", data=payload)
        return bool(response)

    def verify_chat(
        self, chat_id: int | str, custom_description: str | None = None
    ) -> bool:
        """
        Verify a chat (e.g., channel) on behalf of the organization represented by the bot.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :param custom_description: Custom description for the verification (0–70 characters).
                                Must be empty if the organization isn't allowed to set a custom description.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "custom_description": custom_description,
        }
        response = self._make_request("verifyChat", method="POST", data=payload)
        return bool(response)

    def remove_user_verification(self, user_id: int) -> bool:
        """
        Remove verification from a user who is currently verified on behalf of the organization.

        :param user_id: Unique identifier of the target user.
        :return: True on success.
        """
        payload = {"user_id": user_id}
        response = self._make_request(
            "removeUserVerification", method="POST", data=payload
        )
        return bool(response)

    def remove_chat_verification(self, chat_id: int | str) -> bool:
        """
        Remove verification from a chat that is currently verified on behalf of the organization.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
                        Channel direct messages chats cannot be verified.
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        response = self._make_request(
            "removeChatVerification", method="POST", data=payload
        )
        return bool(response)

    def read_business_message(
        self, business_connection_id: str, chat_id: int, message_id: int
    ) -> bool:
        """
        Mark an incoming message as read on behalf of a connected business account.
        Requires the 'can_read_messages' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param chat_id: Unique identifier of the chat where the message was received.
                        The chat must have been active in the last 24 hours.
        :param message_id: Unique identifier of the message to mark as read.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
        }
        response = self._make_request(
            "readBusinessMessage", method="POST", data=payload
        )
        return bool(response)

    def delete_business_messages(
        self, business_connection_id: str, message_ids: List[int]
    ) -> bool:
        """
        Delete messages on behalf of a business account.
        Requires 'can_delete_sent_messages' to delete own messages, or 'can_delete_all_messages' to delete any message.

        :param business_connection_id: Unique identifier of the business connection.
        :param message_ids: A list of 1–100 message identifiers to delete.
                            All messages must be from the same chat.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "message_ids": json.dumps(message_ids),
        }
        response = self._make_request(
            "deleteBusinessMessages", method="POST", data=payload
        )
        return bool(response)

    def set_business_account_name(
        self,
        business_connection_id: str,
        first_name: str,
        last_name: str | None = None,
    ) -> bool:
        """
        Change the first and last name of a managed business account.
        Requires the 'can_change_name' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param first_name: New first name for the business account (1–64 characters).
        :param last_name: New last name for the business account (0–64 characters).
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "first_name": first_name,
            "last_name": last_name,
        }
        response = self._make_request(
            "setBusinessAccountName", method="POST", data=payload
        )
        return bool(response)

    def set_business_account_username(
        self, business_connection_id: str, username: str | None = None
    ) -> bool:
        """
        Change the username of a managed business account.
        Requires the 'can_change_username' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param username: New username for the business account (0–32 characters). Pass empty string to remove.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "username": username,
        }
        response = self._make_request(
            "setBusinessAccountUsername", method="POST", data=payload
        )
        return bool(response)

    def set_business_account_bio(
        self, business_connection_id: str, bio: str | None = None
    ) -> bool:
        """
        Change the bio (description) of a managed business account.
        Requires the 'can_change_bio' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param bio: New bio for the business account (0–140 characters). Pass empty string to remove.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "bio": bio,
        }
        response = self._make_request(
            "setBusinessAccountBio", method="POST", data=payload
        )
        return bool(response)

    def set_business_account_profile_photo(
        self,
        business_connection_id: str,
        photo: bytes,
        is_public: bool | None = None,
    ) -> bool:
        """
        Change the profile photo of a managed business account.
        Requires the 'can_edit_profile_photo' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param photo: New profile photo, uploaded as bytes using multipart/form-data.
        :param is_public: Pass True to set the photo as public (visible even if main photo is hidden by privacy settings).
                        An account can have only one public photo.
        :return: True on success.
        """
        files = {"photo": photo}
        payload = {
            "business_connection_id": business_connection_id,
            "is_public": is_public,
        }
        response = self._make_request(
            "setBusinessAccountProfilePhoto",
            method="POST",
            data=payload,
            files=files,
        )
        return bool(response)

    def remove_business_account_profile_photo(
        self, business_connection_id: str, is_public: bool | None = None
    ) -> bool:
        """
        Remove the current profile photo of a managed business account.
        Requires the 'can_edit_profile_photo' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param is_public: Pass True to remove the public photo (visible even if main photo is hidden).
                        After removing the main photo, the previous photo (if any) becomes the main one.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "is_public": is_public,
        }
        response = self._make_request(
            "removeBusinessAccountProfilePhoto", method="POST", data=payload
        )
        return bool(response)

    def set_business_account_gift_settings(
        self,
        business_connection_id: str,
        show_gift_button: bool,
        accepted_gift_types: Dict[str, Any],
    ) -> bool:
        """
        Change the privacy settings for incoming gifts in a managed business account.
        Requires the 'can_change_gift_settings' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param show_gift_button: Pass True if the gift button should always be shown in the input field.
        :param accepted_gift_types: A JSON-serialized AcceptedGiftTypes object specifying which types of gifts are accepted.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "show_gift_button": show_gift_button,
            "accepted_gift_types": json.dumps(accepted_gift_types),
        }
        response = self._make_request(
            "setBusinessAccountGiftSettings", method="POST", data=payload
        )
        return bool(response)

    def get_business_account_star_balance(
        self, business_connection_id: str
    ) -> AcceptedGiftTypes:
        """
        Get the amount of Telegram Stars owned by a managed business account.
        Requires the 'can_view_gifts_and_stars' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :return: A StarAmount object on success.
        """
        payload = {"business_connection_id": business_connection_id}
        response = self._make_request(
            "getBusinessAccountStarBalance", method="GET", params=payload
        )
        return AcceptedGiftTypes.model_validate(response)

    def transfer_business_account_stars(
        self, business_connection_id: str, star_count: int
    ) -> bool:
        """
        Transfer Telegram Stars from the business account balance to the bot's balance.
        Requires the 'can_transfer_stars' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param star_count: Number of Telegram Stars to transfer (1–10000).
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "star_count": star_count,
        }
        response = self._make_request(
            "transferBusinessAccountStars", method="POST", data=payload
        )
        return bool(response)

    def get_business_account_gifts(
        self,
        business_connection_id: str,
        exclude_unsaved: bool | None = None,
        exclude_saved: bool | None = None,
        exclude_unlimited: bool | None = None,
        exclude_limited: bool | None = None,
        exclude_unique: bool | None = None,
        sort_by_price: bool | None = None,
        offset: str | None = None,
        limit: int | None = None,
    ) -> OwnedGift:
        """
        Get the list of gifts received and owned by a managed business account.
        Requires the 'can_view_gifts_and_stars' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param exclude_unsaved: Pass True to exclude gifts not saved to the profile page.
        :param exclude_saved: Pass True to exclude gifts saved to the profile page.
        :param exclude_unlimited: Pass True to exclude gifts that can be purchased unlimited times.
        :param exclude_limited: Pass True to exclude limited-purchase gifts.
        :param exclude_unique: Pass True to exclude unique gifts.
        :param sort_by_price: Pass True to sort results by price instead of send date.
        :param offset: Offset for pagination (from previous response); use empty string for first page.
        :param limit: Maximum number of gifts to return (1–100, default: 100).
        :return: An OwnedGifts object on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "exclude_unsaved": exclude_unsaved,
            "exclude_saved": exclude_saved,
            "exclude_unlimited": exclude_unlimited,
            "exclude_limited": exclude_limited,
            "exclude_unique": exclude_unique,
            "sort_by_price": sort_by_price,
            "offset": offset,
            "limit": limit,
        }
        response = self._make_request(
            "getBusinessAccountGifts", method="GET", params=payload
        )
        return OwnedGiftAdapter.validate_python(response)

    def convert_gift_to_stars(
        self, business_connection_id: str, owned_gift_id: str
    ) -> bool:
        """
        Convert a regular gift to Telegram Stars.
        Requires the 'can_convert_gifts_to_stars' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param owned_gift_id: Unique identifier of the regular gift to convert.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "owned_gift_id": owned_gift_id,
        }
        response = self._make_request("convertGiftToStars", method="POST", data=payload)
        return bool(response)

    def upgrade_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        keep_original_details: bool | None = None,
        star_count: int | None = None,
    ) -> bool:
        """
        Upgrade a regular gift to a unique gift.
        Requires the 'can_transfer_and_upgrade_gifts' business bot right.
        If the upgrade is paid, the 'can_transfer_stars' right is also required.

        :param business_connection_id: Unique identifier of the business connection.
        :param owned_gift_id: Unique identifier of the regular gift to upgrade.
        :param keep_original_details: Pass True to keep original sender, receiver, and text in the upgraded gift.
        :param star_count: Amount of Telegram Stars to pay for the upgrade.
                        If the gift has a prepaid upgrade, pass 0. Otherwise, this value must match the gift's upgrade cost.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "owned_gift_id": owned_gift_id,
            "keep_original_details": keep_original_details,
            "star_count": star_count,
        }
        response = self._make_request("upgradeGift", method="POST", data=payload)
        return bool(response)

    def transfer_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        new_owner_chat_id: int,
        star_count: int | None = None,
    ) -> bool:
        """
        Transfer an owned unique gift to another user.
        Requires the 'can_transfer_and_upgrade_gifts' business bot right.
        If the transfer is paid, the 'can_transfer_stars' right is required.

        :param business_connection_id: Unique identifier of the business connection.
        :param owned_gift_id: Unique identifier of the gift to transfer.
        :param new_owner_chat_id: Unique identifier of the chat that will receive the gift. Must be active in the last 24 hours.
        :param star_count: Amount of Telegram Stars to pay for the transfer. If 0 or omitted, transfer is free.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "owned_gift_id": owned_gift_id,
            "new_owner_chat_id": new_owner_chat_id,
            "star_count": star_count,
        }
        response = self._make_request("transferGift", method="POST", data=payload)
        return bool(response)

    def post_story(
        self,
        business_connection_id: str,
        content: InputStoryContent,
        active_period: int,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        areas: List[StoryArea] | None = None,
        post_to_chat_page: bool | None = None,
        protect_content: bool | None = None,
    ) -> Story:
        """
        Post a story on behalf of a managed business account.
        Requires the 'can_manage_stories' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param content: A JSON-serialized InputStoryContent object (e.g., photo, video).
        :param active_period: Duration in seconds after which the story expires. Must be one of: 21600 (6h), 43200 (12h), 86400 (1d), or 172800 (2d).
        :param caption: Story caption (0–2048 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (can be used instead of parse_mode).
        :param areas: List of clickable StoryArea objects (e.g., locations, links, quiz).
        :param post_to_chat_page: Pass True to keep the story accessible after expiration.
        :param protect_content: Pass True to protect the story from forwarding and screenshots.
        :return: A Story object on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "content": json.dumps(content),
            "active_period": active_period,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "areas": json.dumps(areas) if areas is not None else None,
            "post_to_chat_page": post_to_chat_page,
            "protect_content": protect_content,
        }
        response = self._make_request("postStory", method="POST", data=payload)
        return Story.model_validate(response)

    def edit_story(
        self,
        business_connection_id: str,
        story_id: int,
        content: InputStoryContent,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        areas: List[StoryArea] | None = None,
    ) -> Story:
        """
        Edit a story previously posted by the bot on behalf of a managed business account.
        Requires the 'can_manage_stories' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param story_id: Unique identifier of the story to edit.
        :param content: A JSON-serialized InputStoryContent object with new content.
        :param caption: New caption for the story (0–2048 characters).
        :param parse_mode: Mode for parsing entities in the caption.
        :param caption_entities: List of special entities in the caption.
        :param areas: List of clickable StoryArea objects to replace existing ones.
        :return: The updated Story object on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "story_id": story_id,
            "content": json.dumps(content),
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "areas": json.dumps(areas) if areas is not None else None,
        }
        response = self._make_request("editStory", method="POST", data=payload)
        return Story.model_validate(response)

    def delete_story(self, business_connection_id: str, story_id: int) -> bool:
        """
        Delete a story previously posted by the bot on behalf of a managed business account.
        Requires the 'can_manage_stories' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :param story_id: Unique identifier of the story to delete.
        :return: True on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "story_id": story_id,
        }
        response = self._make_request("deleteStory", method="POST", data=payload)
        return bool(response)

    def edit_message_text(
        self,
        text: str,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        parse_mode: str | None = None,
        entities: List[MessageEntity] | None = None,
        link_preview_options: LinkPreviewOptions | None = None,
        rich_message: InputRichMessage | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Edit the text and game messages.

        :param text: New text of the message (1–4096 characters after entities parsing).
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited.
        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                        Required if inline_message_id is not specified.
        :param message_id: Identifier of the message to edit. Required if inline_message_id is not specified.
        :param inline_message_id: Identifier of the inline message. Required if chat_id and message_id are not specified.
        :param parse_mode: Mode for parsing entities in the message text ('HTML', 'MarkdownV2').
        :param entities: List of special entities in the message text (can be used instead of parse_mode).
        :param link_preview_options: Options for link preview generation.
        :param: rich_message: New rich content of the message; required if text isn't specified.
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "text": text,
            "parse_mode": parse_mode,
            "entities": entities,
            "link_preview_options": link_preview_options,
            "rich_message": rich_message,
            "reply_markup": reply_markup,
        }
        response = self._make_request("editMessageText", method="POST", data=payload)
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def edit_message_caption(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: List[MessageEntity] | None = None,
        show_caption_above_media: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Edit the caption of messages.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited.
        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                        Required if inline_message_id is not specified.
        :param message_id: Identifier of the message to edit. Required if inline_message_id is not specified.
        :param inline_message_id: Identifier of the inline message. Required if chat_id and message_id are not specified.
        :param caption: New caption of the message (0–1024 characters after entities parsing).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (can be used instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the media (supported only for animation, photo, video).
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "reply_markup": reply_markup,
        }
        response = self._make_request("editMessageCaption", method="POST", data=payload)
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def edit_message_media(
        self,
        media: InputMedia,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Edit the media content of a message (animation, audio, document, photo, video) or add media to a text message.

        When editing inline messages, a new file cannot be uploaded; use existing file_id or URL.

        :param media: A JSON-serialized object representing the new media content (InputMediaPhoto, InputMediaVideo, etc.).
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited.
        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                        Required if inline_message_id is not specified.
        :param message_id: Identifier of the message to edit. Required if inline_message_id is not specified.
        :param inline_message_id: Identifier of the inline message. Required if chat_id and message_id are not specified.
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "media": json.dumps(media),
            "reply_markup": reply_markup,
        }
        response = self._make_request("editMessageMedia", method="POST", data=payload)
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        live_period: int | None = None,
        horizontal_accuracy: Optional[float] = None,
        heading: int | None = None,
        proximity_alert_radius: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Edit live location messages.

        Location can be edited until live_period expires or until stopMessageLiveLocation is called.

        :param latitude: New latitude of the location.
        :param longitude: New longitude of the location.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited.
        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                        Required if inline_message_id is not specified.
        :param message_id: Identifier of the message to edit. Required if inline_message_id is not specified.
        :param inline_message_id: Identifier of the inline message. Required if chat_id and message_id are not specified.
        :param live_period: New period in seconds during which the location can be updated.
                            If 0x7FFFFFFF, location can be updated forever. Must not extend current period by more than 1 day.
        :param horizontal_accuracy: Radius of uncertainty for the location (0–1500 meters).
        :param heading: Direction of user movement in degrees (1–360).
        :param proximity_alert_radius: Maximum distance for proximity alerts (1–100000 meters).
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "latitude": latitude,
            "longitude": longitude,
            "live_period": live_period,
            "horizontal_accuracy": horizontal_accuracy,
            "heading": heading,
            "proximity_alert_radius": proximity_alert_radius,
            "reply_markup": reply_markup,
        }

        response = self._make_request(
            "editMessageLiveLocation", method="POST", data=payload
        )
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def stop_message_live_location(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Stop updating a live location message before live_period expires.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited.
        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                        Required if inline_message_id is not specified.
        :param message_id: Identifier of the live location message to stop. Required if inline_message_id is not specified.
        :param inline_message_id: Identifier of the inline message. Required if chat_id and message_id are not specified.
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
        }
        response = self._make_request(
            "stopMessageLiveLocation", method="POST", data=payload
        )
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def edit_message_checklist(
        self,
        business_connection_id: str,
        chat_id: int,
        message_id: int,
        checklist: Dict[str, Any],
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Edit a checklist on behalf of a connected business account.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited. Required.
        :param chat_id: Unique identifier for the target chat.
        :param message_id: Unique identifier for the target message.
        :param checklist: A JSON-serialized InputChecklist object for the new checklist.
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object on success.
        """
        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "checklist": json.dumps(checklist),
            "reply_markup": reply_markup,
        }
        response = self._make_request(
            "editMessageChecklist", method="POST", data=payload
        )
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def edit_message_reply_markup(
        self,
        business_connection_id: str | None = None,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """
        Edit only the reply markup (inline keyboard) of a message.

        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is edited.
        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
                        Required if inline_message_id is not specified.
        :param message_id: Identifier of the message to edit. Required if inline_message_id is not specified.
        :param inline_message_id: Identifier of the inline message. Required if chat_id and message_id are not specified.
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
        }
        response = self._make_request(
            "editMessageReplyMarkup", method="POST", data=payload
        )
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def stop_poll(
        self,
        chat_id: int | str,
        message_id: int,
        business_connection_id: str | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Poll:
        """
        Stop a poll that was sent by the bot.
        On success, the stopped Poll object is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param message_id: Identifier of the original message with the poll.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the poll is stopped.
        :param reply_markup: A JSON-serialized object for a new inline keyboard attached to the message.
        :return: The stopped Poll object on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "business_connection_id": business_connection_id,
            "reply_markup": reply_markup,
        }
        response = self._make_request("stopPoll", method="POST", data=payload)
        return Poll.model_validate(response)

    def approve_suggested_post(
        self, chat_id: int, message_id: int, send_date: int | None = None
    ) -> bool:
        """
        Approve a suggested post in a direct messages chat.
        The bot must have the 'can_post_messages' administrator right in the corresponding channel chat.

        :param chat_id: Unique identifier for the target direct messages chat.
        :param message_id: Identifier of the suggested post message to approve.
        :param send_date: Unix timestamp when the post should be published.
                        Must be within 30 days (2678400 seconds) in the future.
                        Omit if already specified during creation.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "send_date": send_date,
        }
        response = self._make_request(
            "approveSuggestedPost", method="POST", data=payload
        )
        return bool(response)

    def decline_suggested_post(
        self, chat_id: int, message_id: int, comment: str | None = None
    ) -> bool:
        """
        Decline a suggested post in a direct messages chat.
        The bot must have the 'can_manage_direct_messages' administrator right in the corresponding channel chat.

        :param chat_id: Unique identifier for the target direct messages chat.
        :param message_id: Identifier of the suggested post message to decline.
        :param comment: Comment for the creator of the suggested post (0–128 characters).
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "comment": comment,
        }
        response = self._make_request(
            "declineSuggestedPost", method="POST", data=payload
        )
        return bool(response)

    def delete_message(self, chat_id: int | str, message_id: int) -> bool:
        """
        Delete a message, including service messages, with the following limitations:
        - The message must have been sent less than 48 hours ago.
        - Service messages about supergroup/channel/forum topic creation cannot be deleted.
        - A dice message in a private chat can only be deleted if sent more than 24 hours ago.
        - Bots can delete outgoing messages in private chats, groups, and supergroups.
        - Bots can delete incoming messages in private chats.
        - Bots with 'can_post_messages' can delete outgoing messages in channels.
        - Administrators can delete any message in groups.
        - Bots with 'can_delete_messages' right can delete any message in supergroups and channels.
        - Bots with 'can_manage_direct_messages' right can delete any message in direct messages chats.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param message_id: Identifier of the message to delete.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        response = self._make_request("deleteMessage", method="POST", data=payload)
        return bool(response)

    def delete_messages(self, chat_id: int | str, message_ids: List[int]) -> bool:
        """
        Delete multiple messages simultaneously.
        If some messages can't be found or deleted, they are simply skipped.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param message_ids: A list of 1–100 message identifiers to delete.
                            See delete_message() for limitations on deletable messages.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_ids": json.dumps(message_ids),
        }
        response = self._make_request("deleteMessages", method="POST", data=payload)
        return bool(response)

    def delete_message_reaction(
        self, chat_id: int | str, message_id: int, user_id: int, actor_chat_id: int
    ) -> bool:
        """
        Use this method to remove a reaction from a message in a group or a supergroup chat.
        The bot must have the 'can_delete_messages' administrator right in the chat.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param message_id: A list of 1–100 message identifiers to delete. See delete_message() for limitations on deletable messages.
        :param user_id: Identifier of the user whose reaction will be removed, if the reaction was added by a user.
        :param actor_chat_id: Identifier of the chat whose reaction will be removed, if the reaction was added by a chat.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "user_id": user_id,
            "actor_chat_id": actor_chat_id,
        }
        response = self._make_request(
            "deleteMessageReaction", method="POST", data=payload
        )
        return bool(response)

    def delete_message_reactions(
        self, chat_id: int | str, user_id: int, actor_chat_id: int
    ) -> bool:
        """
        Use this method to remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat.
        The bot must have the 'can_delete_messages' administrator right in the chat.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username.
        :param user_id: Identifier of the user whose reactions will be removed, if the reactions were added by a user.
        :param actor_chat_id: Identifier of the chat whose reactions will be removed, if the reactions were added by a chat.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "user_id": user_id,
            "actor_chat_id": actor_chat_id,
        }
        response = self._make_request(
            "deleteAllMessageReactions", method="POST", data=payload
        )
        return bool(response)

    def send_sticker(
        self,
        chat_id: int | str,
        sticker: str | bytes,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        emoji: str | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Send static .WEBP, animated .TGS, or video .WEBM stickers.
        On success, the sent Message is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param sticker: Sticker to send. Can be a file_id (str), URL (str), or raw bytes.
                        - For static stickers: .WEBP or .PNG
                        - For animated stickers: .TGS
                        - For video stickers: .WEBM
                        Note: Video and animated stickers cannot be sent via HTTP URL.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param emoji: Emoji associated with the sticker (only for newly uploaded stickers).
        :param disable_notification: Send message silently without notification sound.
        :param protect_content: Protect message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post (direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline or reply keyboard.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "emoji": emoji,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        if isinstance(sticker, bytes):
            # Upload new sticker → use POST + multipart/form-data
            files = {"sticker": sticker}
            payload["sticker"] = None
            response = self._make_request(
                "sendSticker", method="POST", data=payload, files=files
            )
        else:
            # Reuse existing file_id or URL → use POST (GET not supported for stickers)
            payload["sticker"] = sticker
            response = self._make_request("sendSticker", method="POST", data=payload)

        return Message.model_validate(response)

    def get_sticker_set(self, name: str) -> StickerSet:
        """
        Get information about a sticker set.

        :param name: Name of the sticker set (e.g., 'my_stickers_by_botname').
        :return: A StickerSet object on success.
        """
        payload = {"name": name}
        response = self._make_request("getStickerSet", method="GET", params=payload)
        return StickerSet.model_validate(response)

    def get_custom_emoji_stickers(self, custom_emoji_ids: List[str]) -> Sticker:
        """
        Get information about custom emoji stickers by their identifiers.

        :param custom_emoji_ids: A list of up to 200 unique identifiers of custom emoji stickers.
        :return: An Array of Sticker objects on success.
        """
        payload = {"custom_emoji_ids": json.dumps(custom_emoji_ids)}
        response = self._make_request(
            "getCustomEmojiStickers", method="POST", data=payload
        )
        return Sticker.model_validate(response)

    def upload_sticker_file(
        self, user_id: int, sticker: bytes, sticker_format: str
    ) -> File:
        """
        Upload a sticker file for later use in creating or editing sticker sets.
        The file can be reused multiple times.

        :param user_id: User identifier of the sticker file owner.
        :param sticker: File with the sticker in .WEBP (static), .PNG (static), .TGS (animated), or .WEBM (video) format.
                        See https://core.telegram.org/stickers for technical requirements.
        :param sticker_format: Format of the sticker: 'static', 'animated', or 'video'.
        :return: The uploaded File object on success.
        """
        files = {"sticker": sticker}
        payload = {
            "user_id": user_id,
            "sticker_format": sticker_format,
        }
        response = self._make_request(
            "uploadStickerFile", method="POST", data=payload, files=files
        )
        return File.model_validate(response)

    def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: List[InputSticker],
        sticker_type: str | None = None,
        needs_repainting: bool | None = None,
    ) -> bool:
        """
        Create a new sticker set owned by a user. The bot will be able to edit this set.

        :param user_id: User identifier of the sticker set owner.
        :param name: Short name of the sticker set (1–64 characters). Must end with '_by_<bot_username>'.
        :param title: Sticker set title (1–64 characters).
        :param stickers: A list of InputSticker objects (1–50 stickers).
        :param sticker_type: Type of stickers: 'regular', 'mask', or 'custom_emoji'. Default: 'regular'.
        :param needs_repainting: For custom emoji sets: True if stickers should adapt to context color (text, status, etc.).
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "name": name,
            "title": title,
            "stickers": json.dumps(stickers),
            "sticker_type": sticker_type,
            "needs_repainting": needs_repainting,
        }
        response = self._make_request(
            "createNewStickerSet", method="POST", data=payload
        )
        return bool(response)

    def add_sticker_to_set(
        self, user_id: int, name: str, sticker: InputSticker
    ) -> bool:
        """
        Add a new sticker to a set created by the bot.
        - Regular/mask sets: up to 120 stickers.
        - Custom emoji sets: up to 200 stickers.

        :param user_id: User identifier of the sticker set owner.
        :param name: Name of the sticker set.
        :param sticker: An InputSticker object describing the sticker to add.
                        If the same sticker exists, the set is not changed.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "name": name,
            "sticker": json.dumps(sticker),
        }
        response = self._make_request("addStickerToSet", method="POST", data=payload)
        return bool(response)

    def set_sticker_position_in_set(self, sticker: str, position: int) -> bool:
        """
        Move a sticker in a bot-created set to a specific position (zero-based index).

        :param sticker: File identifier of the sticker.
        :param position: New position of the sticker in the set.
        :return: True on success.
        """
        payload = {
            "sticker": sticker,
            "position": position,
        }
        response = self._make_request(
            "setStickerPositionInSet", method="POST", data=payload
        )
        return bool(response)

    def delete_sticker_from_set(self, sticker: str) -> bool:
        """
        Delete a sticker from a set created by the bot.

        :param sticker: File identifier of the sticker to delete.
        :return: True on success.
        """
        payload = {"sticker": sticker}
        response = self._make_request(
            "deleteStickerFromSet", method="POST", data=payload
        )
        return bool(response)

    def replace_sticker_in_set(
        self, user_id: int, name: str, old_sticker: str, sticker: InputSticker
    ) -> bool:
        """
        Replace an existing sticker in a set with a new one.
        Equivalent to: delete → add → set position.

        :param user_id: User identifier of the sticker set owner.
        :param name: Name of the sticker set.
        :param old_sticker: File identifier of the sticker to replace.
        :param sticker: An InputSticker object with the new sticker data.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "name": name,
            "old_sticker": old_sticker,
            "sticker": sticker.to_dict(),
        }
        response = self._make_request(
            "replaceStickerInSet", method="POST", data=payload
        )
        return bool(response)

    def set_sticker_emoji_list(self, sticker: str, emoji_list: List[str]) -> bool:
        """
        Change the list of emoji associated with a regular or custom emoji sticker.
        The sticker must belong to a bot-created set.

        :param sticker: File identifier of the sticker.
        :param emoji_list: List of 1–20 emoji to associate with the sticker.
        :return: True on success.
        """
        payload = {
            "sticker": sticker,
            "emoji_list": json.dumps(emoji_list),
        }
        response = self._make_request(
            "setStickerEmojiList", method="POST", data=payload
        )
        return bool(response)

    def set_sticker_keywords(
        self, sticker: str, keywords: Optional[List[str]] = None
    ) -> bool:
        """
        Change search keywords for a regular or custom emoji sticker.
        Total length of all keywords must not exceed 64 characters.
        The sticker must belong to a bot-created set.

        :param sticker: File identifier of the sticker.
        :param keywords: List of 0–20 search keywords. Pass empty list or omit to remove.
        :return: True on success.
        """
        payload = {
            "sticker": sticker,
            "keywords": json.dumps(keywords) if keywords is not None else None,
        }
        response = self._make_request("setStickerKeywords", method="POST", data=payload)
        return bool(response)

    def set_sticker_mask_position(
        self, sticker: str, mask_position: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Change the mask position of a mask sticker.
        The sticker must belong to a sticker set created by the bot.
        Omit the mask_position parameter to remove the current mask position.

        :param sticker: File identifier of the mask sticker.
        :param mask_position: A JSON-serialized MaskPosition object describing the new position
                            where the mask should be placed on the face. Pass None to remove.
        :return: True on success.
        """
        payload = {
            "sticker": sticker,
            "mask_position": json.dumps(mask_position)
            if mask_position is not None
            else None,
        }
        response = self._make_request(
            "setStickerMaskPosition", method="POST", data=payload
        )
        return bool(response)

    def set_sticker_set_title(self, name: str, title: str) -> bool:
        """
        Set the title of a sticker set created by the bot.

        :param name: Name of the sticker set.
        :param title: New title for the sticker set (1–64 characters).
        :return: True on success.
        """
        payload = {
            "name": name,
            "title": title,
        }
        response = self._make_request("setStickerSetTitle", method="POST", data=payload)
        return bool(response)

    def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        thumbnail: InputFile | str | None = None,
        format: str = "static",
    ) -> bool:
        """
        Set the thumbnail of a regular or mask sticker set.
        The format of the thumbnail must match the format of the stickers in the set.

        - For 'static' sets: a .WEBP or .PNG image, exactly 100x100px, up to 128 KB.
        - For 'animated' sets: a .TGS animation, up to 32 KB.
        - For 'video' sets: a .WEBM video, up to 32 KB.

        Animated and video thumbnails cannot be uploaded via HTTP URL.

        If thumbnail is omitted, the thumbnail is removed and the first sticker becomes the thumbnail.

        :param name: Name of the sticker set.
        :param user_id: User identifier of the sticker set owner.
        :param thumbnail: Thumbnail file to upload (bytes), file_id (str), or HTTP URL (str).
                        If None, removes the current thumbnail.
        :param format: Format of the thumbnail: 'static', 'animated', or 'video'.
        :return: True on success.
        """
        payload = {
            "name": name,
            "user_id": user_id,
            "format": format,
        }
        files = None
        if isinstance(thumbnail, bytes):
            files = {"thumbnail": thumbnail}
            payload["thumbnail"] = None

        elif thumbnail is not None:
            payload["thumbnail"] = thumbnail

        # else: omit thumbnail to drop it
        response = self._make_request(
            "setStickerSetThumbnail", method="POST", data=payload, files=files
        )
        return bool(response)

    def set_custom_emoji_sticker_set_thumbnail(
        self, name: str, custom_emoji_id: str | None = ""
    ) -> bool:
        """
        Set the thumbnail of a custom emoji sticker set.

        :param name: Name of the custom emoji sticker set.
        :param custom_emoji_id: Custom emoji identifier of a sticker in the set to use as the thumbnail.
                                Pass an empty string or None to remove the thumbnail and use the first sticker instead.
        :return: True on success.
        """
        payload = {
            "name": name,
            "custom_emoji_id": custom_emoji_id,
        }
        # We include custom_emoji_id even if None (to allow empty string for removal)
        response = self._make_request(
            "setCustomEmojiStickerSetThumbnail", method="POST", data=payload
        )
        return bool(response)

    def delete_sticker_set(self, name: str) -> bool:
        """
        Delete a sticker set that was created by the bot.

        :param name: Name of the sticker set to delete.
        :return: True on success.
        """
        payload = {"name": name}
        response = self._make_request("deleteStickerSet", method="POST", data=payload)
        return bool(response)

    def send_rich_message(
        self,
        chat_id: int | str,
        rich_message: InputRichMessage,
        message_thread_id: int | None = None,
        business_connection_id: str | None = None,
        direct_messages_topic_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: ReplyMarkup | None = None,
    ) -> Message:
        """
        Use this method to send rich messages. If the message contains a block with a media element,
        then the bot must have the right to send the media to the chat.

        :param chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
        :param rich_message: The message to be sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent.
        :param direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat.
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param protect_content: Protects the contents of the sent message from forwarding and saving.
        :param allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
        :param message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only.
        :param suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "rich_message": rich_message,
            "message_thread_id": message_thread_id,
            "business_connection_id": business_connection_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendRichMessage", method="POST", data=payload)
        return Message.model_validate(response)

    def send_rich_message_draft(
        self,
        chat_id: int,
        draft_id: int,
        rich_message: InputRichMessage,
        message_thread_id: int | None = None,
    ):
        """
        Use this method to stream a partial rich message to a user while the message is being generated.
        Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized,
        you must call sendRichMessage with the complete message to persist it in the user's chat.

        :param chat_id: Unique identifier for the target private chat.
        :param draft_id: Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated.
        :param rich_message: The partial message to be streamed.
        :param message_thread_id: Unique identifier for the target message thread.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "draft_id": draft_id,
            "rich_message": rich_message,
            "message_thread_id": message_thread_id,
        }
        response = self._make_request(
            "sendRichMessageDraft", method="POST", data=payload
        )
        return bool(response)

    def answer_inline_query(
        self,
        inline_query_id: str,
        results: List[InlineQueryResult],
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        button: InlineQueryResultsButton | None = None,
    ) -> bool:
        """
        Send answers to an incoming inline query.
        On success, True is returned.
        No more than 50 results per query are allowed.

        :param inline_query_id: Unique identifier for the answered query.
        :param results: A JSON-serialized array of results for the inline query.
        :param cache_time: The maximum amount of time in seconds that the result of the query may be cached on the server. Defaults to 300.
        :param is_personal: Pass True if results are meant only for the user that sent the query. Otherwise, results may be cached for all users.
        :param next_offset: Pass the offset that clients should send in the next query to receive more results. Pass empty string if no more results.
        :param button: A JSON-serialized object describing a button to be shown above the results.
        :return: True on success.
        """
        payload = {
            "inline_query_id": inline_query_id,
            "results": json.dumps([result.to_dict() for result in results]),
            "cache_time": cache_time,
            "is_personal": is_personal,
            "next_offset": next_offset,
            "button": button.to_dict() if button else None,
        }
        response = self._make_request("answerInlineQuery", method="POST", data=payload)
        return bool(response)

    def answer_web_app_query(
        self, web_app_query_id: str, result: InlineQueryResult
    ) -> SentWebAppMessage:
        """
        Set the result of an interaction with a Web App and send a corresponding message on behalf of the user
        to the chat from which the query originated.

        On success, a SentWebAppMessage object is returned.

        :param web_app_query_id: Unique identifier for the query to be answered.
        :param result: A JSON-serialized InlineQueryResult object describing the message to be sent.
                    Must be one of the supported result types (e.g., article, photo, video, etc.).
        :return: A SentWebAppMessage object on success.
        """
        payload = {
            "web_app_query_id": web_app_query_id,
            "result": json.dumps(result),
        }
        response = self._make_request("answerWebAppQuery", method="POST", data=payload)
        return SentWebAppMessage.model_validate(response)

    def create_sent_web_app_message(
        self,
        inline_message_id: str | None = None,
    ) -> SentWebAppMessage:
        """
        Create a SentWebAppMessage object (typically returned by answerWebAppQuery).

        Describes an inline message sent by a Web App on behalf of a user.

        :param inline_message_id: Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached.
        :return: A dictionary representing a SentWebAppMessage object.
        """
        result = {
            "inline_message_id": inline_message_id,
        }
        return SentWebAppMessage.model_validate(result)

    def save_prepared_inline_message(
        self,
        user_id: int,
        result: Dict[str, Any],
        allow_user_chats: bool | None = None,
        allow_bot_chats: bool | None = None,
        allow_group_chats: bool | None = None,
        allow_channel_chats: bool | None = None,
    ) -> PreparedInlineMessage:
        """
        Store a message that can be sent by a user of a Mini App.
        This allows the Mini App to prepare a message in advance, which the user can send later with a single tap.

        Returns a PreparedInlineMessage object on success.

        :param user_id: Unique identifier of the target user that can use the prepared message.
        :param result: A JSON-serialized InlineQueryResult object describing the message to be sent.
        :param allow_user_chats: Pass True if the message can be sent to private chats with users.
        :param allow_bot_chats: Pass True if the message can be sent to private chats with bots.
        :param allow_group_chats: Pass True if the message can be sent to group and supergroup chats.
        :param allow_channel_chats: Pass True if the message can be sent to channel chats.
        :return: A PreparedInlineMessage object on success.
        """
        payload = {
            "user_id": user_id,
            "result": json.dumps(result),
            "allow_user_chats": allow_user_chats,
            "allow_bot_chats": allow_bot_chats,
            "allow_group_chats": allow_group_chats,
            "allow_channel_chats": allow_channel_chats,
        }
        response = self._make_request(
            "savePreparedInlineMessage", method="POST", data=payload
        )
        return PreparedInlineMessage.model_validate(response)

    def save_prepared_keyboard_button(
        self, user_id: int, button: KeyboardButton
    ) -> PreparedKeyboardButton:
        """
        Stores a keyboard button that can be used by a user within a Mini App.

        :param user_id: Unique identifier of the target user that can use the prepared message.
        :param button: A JSON-serialized object describing the button to be saved. The button must be of the type request_users, request_chat, or request_managed_bot.
        :return: PreparedKeyboardButton object
        """
        payload = {"user_id": user_id, "button": button}
        response = self._make_request(
            "savePreparedKeyboardButton", method="POST", data=payload
        )
        return PreparedKeyboardButton.model_validate(response)

    def create_prepared_inline_message(
        self, _id: str, expiration_date: int
    ) -> PreparedInlineMessage:
        """
        Create a PreparedInlineMessage object (returned by savePreparedInlineMessage).

        Describes an inline message that can be sent by a user of a Mini App.

        :param id: Unique identifier of the prepared message.
        :param expiration_date: Expiration date of the prepared message, in Unix time. Expired messages cannot be used.
        :return: A dictionary representing a PreparedInlineMessage object.
        """
        result = {
            "id": _id,
            "expiration_date": expiration_date,
        }
        return PreparedInlineMessage.model_validate(result)

    def send_invoice(
        self,
        chat_id: int | str,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        message_thread_id: int | None = None,
        direct_messages_topic_id: int | None = None,
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: List[int] | None = None,
        start_parameter: str | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        suggested_post_parameters: SuggestedPostParameters | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """
        Send an invoice for payment.

        On success, the sent Message is returned.

        :param chat_id: Unique identifier for the target chat or username of the target channel (e.g. @channelusername).
        :param title: Product name (1–32 characters).
        :param description: Product description (1–255 characters).
        :param payload: Bot-defined payload (1–128 bytes). Not shown to the user. Use for internal tracking.
        :param currency: Three-letter ISO 4217 currency code (e.g., 'USD', 'EUR') or 'XTR' for Telegram Stars.
                        For payments in Telegram Stars, provider_token must be empty.
        :param prices: A JSON-serialized list of LabeledPrice objects representing the price breakdown.
                    Must contain exactly one item if currency is 'XTR'.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param direct_messages_topic_id: Identifier of the direct messages topic; required if sending to a direct messages chat.
        :param provider_token: Payment provider token (from @BotFather). Pass empty string for payments in Telegram Stars.
        :param max_tip_amount: Maximum tip amount in the smallest currency units (e.g., 145 for $1.45). Defaults to 0.
        :param suggested_tip_amounts: List of suggested tip amounts (positive, increasing, <= max_tip_amount). Max 4 items.
        :param start_parameter: Unique deep-linking parameter. If empty, forwarded messages have a Pay button.
                                If non-empty, forwarded messages have a URL button with a deep link to the bot.
        :param provider_data: JSON-serialized data about the invoice to share with the payment provider.
        :param photo_url: URL of the product photo for the invoice (recommended).
        :param photo_size: Photo size in bytes.
        :param photo_width: Photo width.
        :param photo_height: Photo height.
        :param need_name: Pass True if user's full name is required to complete the order.
        :param need_phone_number: Pass True if user's phone number is required.
        :param need_email: Pass True if user's email address is required.
        :param need_shipping_address: Pass True if shipping address is required (for physical goods).
        :param send_phone_number_to_provider: Pass True to send user's phone number to the provider.
        :param send_email_to_provider: Pass True to send user's email address to the provider.
        :param is_flexible: Pass True if the final price depends on the shipping method (e.g., delivery cost varies).
        :param disable_notification: Send the message silently (no notification sound).
        :param protect_content: Protect the message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param suggested_post_parameters: Parameters for sending a suggested post (direct messages chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline keyboard. If empty, a default 'Pay total price' button is shown.
                            The first button must be a Pay button if reply_markup is provided.
        :return: The sent Message object on success.
        """
        if currency == "XTR" and (provider_token is not None and provider_token != ""):
            raise ValueError(
                "For payments in Telegram Stars (XTR), provider_token must be an empty string."
            )

        payload_data = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "direct_messages_topic_id": direct_messages_topic_id,
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": provider_token,
            "currency": currency,
            "prices": json.dumps(prices),
            "max_tip_amount": max_tip_amount,
            "suggested_tip_amounts": suggested_tip_amounts,
            "start_parameter": start_parameter,
            "provider_data": provider_data,
            "photo_url": photo_url,
            "photo_size": photo_size,
            "photo_width": photo_width,
            "photo_height": photo_height,
            "need_name": need_name,
            "need_phone_number": need_phone_number,
            "need_email": need_email,
            "need_shipping_address": need_shipping_address,
            "send_phone_number_to_provider": send_phone_number_to_provider,
            "send_email_to_provider": send_email_to_provider,
            "is_flexible": is_flexible,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "suggested_post_parameters": suggested_post_parameters,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendInvoice", method="POST", data=payload_data)
        return Message.model_validate(response)

    def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[LabeledPrice],
        business_connection_id: str | None = None,
        provider_token: str | None = None,
        subscription_period: int | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: List[int] | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
    ) -> str:
        """
        Create a direct link for an invoice. This link can be used to open the payment interface directly.

        On success, returns the created invoice link as a string.

        :param title: Product name (1–32 characters).
        :param description: Product description (1–255 characters).
        :param payload: Bot-defined payload (1–128 bytes). Not shown to the user. Use for internal tracking.
        :param currency: Three-letter ISO 4217 currency code (e.g., 'USD', 'EUR') or 'XTR' for Telegram Stars.
        :param prices: A JSON-serialized list of LabeledPrice objects representing the price breakdown.
                    Must contain exactly one item if currency is 'XTR'.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the link is created.
                                    Required only for payments in Telegram Stars.
        :param provider_token: Payment provider token (from @BotFather). Pass empty string for payments in Telegram Stars.
        :param subscription_period: Number of seconds the subscription will be active before the next payment.
                                    Must be 2592000 (30 days) if specified. Only valid if currency is 'XTR'.
        :param max_tip_amount: Maximum tip amount in the smallest currency units (e.g., 145 for $1.45). Defaults to 0.
        :param suggested_tip_amounts: List of suggested tip amounts (positive, increasing, <= max_tip_amount). Max 4 items.
        :param provider_data: JSON-serialized data about the invoice to share with the payment provider.
        :param photo_url: URL of the product photo for the invoice (recommended).
        :param photo_size: Photo size in bytes.
        :param photo_width: Photo width.
        :param photo_height: Photo height.
        :param need_name: Pass True if user's full name is required to complete the order.
        :param need_phone_number: Pass True if user's phone number is required.
        :param need_email: Pass True if user's email address is required.
        :param need_shipping_address: Pass True if shipping address is required (for physical goods).
        :param send_phone_number_to_provider: Pass True to send user's phone number to the provider.
        :param send_email_to_provider: Pass True to send user's email address to the provider.
        :param is_flexible: Pass True if the final price depends on the shipping method (e.g., delivery cost varies).
        :return: The created invoice link as a string on success.
        """
        # Validate currency and provider_token for Stars
        if currency == "XTR":
            if provider_token not in (None, ""):
                raise ValueError(
                    "For payments in Telegram Stars (XTR), provider_token must be an empty string."
                )
            if subscription_period is not None and subscription_period != 2592000:
                raise ValueError(
                    "For Telegram Stars subscriptions, subscription_period must be 2592000 (30 days)."
                )

        payload_data = {
            "business_connection_id": business_connection_id,
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": provider_token,
            "currency": currency,
            "prices": json.dumps(prices),
            "subscription_period": subscription_period,
            "max_tip_amount": max_tip_amount,
            "suggested_tip_amounts": json.dumps(suggested_tip_amounts)
            if suggested_tip_amounts is not None
            else None,
            "provider_data": provider_data,
            "photo_url": photo_url,
            "photo_size": photo_size,
            "photo_width": photo_width,
            "photo_height": photo_height,
            "need_name": need_name,
            "need_phone_number": need_phone_number,
            "need_email": need_email,
            "need_shipping_address": need_shipping_address,
            "send_phone_number_to_provider": send_phone_number_to_provider,
            "send_email_to_provider": send_email_to_provider,
            "is_flexible": is_flexible,
        }
        response = self._make_request(
            "createInvoiceLink", method="POST", data=payload_data
        )
        return str(response)

    def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: Optional[ShippingOption] = None,
        error_message: str | None = None,
    ) -> bool:
        """
        Reply to a shipping query.

        If an invoice was sent with `is_flexible=True` and requested a shipping address, the Bot API will send an Update
        with a `shipping_query` field. Use this method to respond.

        On success, True is returned.

        :param shipping_query_id: Unique identifier for the shipping query to be answered.
        :param ok: Pass True if delivery to the specified address is possible, False otherwise.
        :param shipping_options: Required if `ok` is True. A list of available shipping options (ShippingOption objects).
        :param error_message: Required if `ok` is False. Error message to show to the user explaining why delivery is impossible.
        :return: True on success.
        """
        if ok and not shipping_options:
            raise ValueError("shipping_options are required when ok is True.")

        if not ok and not error_message:
            raise ValueError("error_message is required when ok is False.")

        payload = {
            "shipping_query_id": shipping_query_id,
            "ok": ok,
            "shipping_options": json.dumps(shipping_options)
            if shipping_options is not None
            else None,
            "error_message": error_message,
        }
        response = self._make_request(
            "answerShippingQuery", method="POST", data=payload
        )
        return bool(response)

    def answer_pre_checkout_query(
        self, pre_checkout_query_id: str, ok: bool, error_message: str | None = None
    ) -> bool:
        """
        Respond to a pre-checkout query.

        After the user confirms payment and shipping details, the Bot API sends a `pre_checkout_query`.
        You must respond within 10 seconds.

        On success, True is returned.

        :param pre_checkout_query_id: Unique identifier for the pre-checkout query to be answered.
        :param ok: Pass True if the bot is ready to proceed with the order (e.g., goods are available). Use False if there are problems.
        :param error_message: Required if `ok` is False. Human-readable explanation for why the checkout cannot proceed.
                            Telegram will display this message to the user.
        :return: True on success.
        """
        if not ok and not error_message:
            raise ValueError("error_message is required when ok is False.")

        payload = {
            "pre_checkout_query_id": pre_checkout_query_id,
            "ok": ok,
            "error_message": error_message,
        }
        response = self._make_request(
            "answerPreCheckoutQuery", method="POST", data=payload
        )
        return bool(response)

    def get_my_star_balance(self) -> StarAmount:
        """
        Get the current Telegram Stars balance of the bot.

        Requires no parameters.

        On success, returns a StarAmount object.

        :return: A StarAmount object containing the bot's current Telegram Stars balance.
        """
        response = self._make_request("getMyStarBalance", method="GET")
        return StarAmount.model_validate(response)

    def get_star_transactions(
        self, offset: int | None = None, limit: int | None = None
    ) -> StarTransactions:
        """
        Get the bot's Telegram Star transactions in chronological order.

        On success, returns a StarTransactions object.

        :param offset: Number of transactions to skip in the response.
        :param limit: Maximum number of transactions to retrieve (1–100). Defaults to 100.
        :return: A StarTransactions object on success.
        """
        payload = {"offset": offset, "limit": limit}
        response = self._make_request(
            "getStarTransactions", method="GET", params=payload
        )
        return StarTransactions.model_validate(response)

    def refund_star_payment(
        self, user_id: int, telegram_payment_charge_id: str
    ) -> bool:
        """
        Refund a successful payment made in Telegram Stars.

        Returns True on success.

        :param user_id: Identifier of the user whose payment will be refunded.
        :param telegram_payment_charge_id: Telegram payment identifier (from SuccessfulPayment.telegram_payment_charge_id).
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "telegram_payment_charge_id": telegram_payment_charge_id,
        }
        response = self._make_request("refundStarPayment", method="POST", data=payload)
        return bool(response)

    def edit_user_star_subscription(
        self, user_id: int, telegram_payment_charge_id: str, is_canceled: bool
    ) -> bool:
        """
        Cancel or re-enable the extension of a subscription paid in Telegram Stars.

        Returns True on success.

        :param user_id: Identifier of the user whose subscription will be edited.
        :param telegram_payment_charge_id: Telegram payment identifier for the subscription.
        :param is_canceled: Pass True to cancel the extension of the user's subscription.
                            The subscription must be active up to the end of the current period.
                            Pass False to allow the user to re-enable a subscription previously canceled by the bot.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "telegram_payment_charge_id": telegram_payment_charge_id,
            "is_canceled": is_canceled,
        }
        response = self._make_request(
            "editUserStarSubscription", method="POST", data=payload
        )
        return bool(response)

    def set_passport_data_errors(
        self, user_id: int, errors: List[PassportElementError]
    ) -> bool:
        """
        Inform a user that some of the data they provided in Telegram Passport contains errors.
        The user will not be able to re-submit until the errors are fixed.

        Use this method if the submitted data doesn't meet your service's requirements
        (e.g., invalid date, blurry document, evidence of tampering).

        Returns True on success.

        :param user_id: Unique identifier of the target user.
        :param errors: A list of PassportElementError objects describing the errors.
        :return: True on success.
        """
        payload = {
            "user_id": user_id,
            "errors": json.dumps(errors),
        }
        response = self._make_request(
            "setPassportDataErrors", method="POST", data=payload
        )
        return bool(response)

    def send_game(
        self,
        chat_id: int,
        game_short_name: str,
        business_connection_id: str | None = None,
        message_thread_id: int | None = None,
        disable_notification: bool | None = None,
        protect_content: bool | None = None,
        allow_paid_broadcast: bool | None = None,
        message_effect_id: str | None = None,
        reply_parameters: ReplyParameters | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message:
        """
        Send a game to a user.

        On success, the sent Message is returned.

        :param chat_id: Unique identifier for the target chat.
                        Games cannot be sent to channel direct messages or channel chats.
        :param game_short_name: Short name of the game, serves as the unique identifier.
                                Games must be created and configured via @BotFather.
        :param business_connection_id: Unique identifier of the business connection on behalf of which the message is sent.
        :param message_thread_id: Unique identifier for the target message thread (topic) in a forum; for forum supergroups only.
        :param disable_notification: Send the message silently (no notification sound).
        :param protect_content: Protect the message from forwarding and saving.
        :param allow_paid_broadcast: Allow up to 1000 messages/sec for 0.1 Stars per message.
        :param message_effect_id: Unique identifier of a message effect to be added (private chats only).
        :param reply_parameters: Description of the message to reply to.
        :param reply_markup: Inline keyboard. If empty, a default 'Play [game_title]' button is shown.
                            The first button must be a game launch button if reply_markup is provided.
        :return: The sent Message object on success.
        """
        payload = {
            "chat_id": chat_id,
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "game_short_name": game_short_name,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }
        response = self._make_request("sendGame", method="POST", data=payload)
        return Message.model_validate(response)

    def set_game_score(
        self,
        user_id: int,
        score: int,
        force: bool | None = None,
        disable_edit_message: bool | None = None,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
    ) -> Message | bool:
        """
        Set the score of a specified user in a game message.

        On success, if the message is not an inline message, the Message is returned; otherwise, True is returned.

        Returns an error if the new score is not greater than the user's current score in the chat and `force` is False.

        :param user_id: User identifier.
        :param score: New score for the user. Must be non-negative.
        :param force: Pass True if the high score is allowed to decrease.
                    Useful for fixing mistakes or banning cheaters.
        :param disable_edit_message: Pass True if the game message should not be automatically edited to include the current scoreboard.
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param message_id: Required if inline_message_id is not specified. Identifier of the sent message.
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "user_id": user_id,
            "score": score,
            "force": force,
            "disable_edit_message": disable_edit_message,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
        }
        response = self._make_request("setGameScore", method="POST", data=payload)
        if isinstance(response, bool):
            return bool(response)

        return Message.model_validate(response)

    def get_game_high_scores(
        self,
        user_id: int,
        chat_id: int | None = None,
        message_id: int | None = None,
        inline_message_id: str | None = None,
    ) -> List[GameHighScore]:
        """
        Get data for high score tables.

        Returns an array of GameHighScore objects.

        This method returns the score of the specified user and several of their neighbors in the game.
        Currently, it returns the target user's score plus two closest neighbors on each side.
        It also returns the top three users if the user and their neighbors are not among them.
        Note: This behavior is subject to change.

        :param user_id: Target user's unique identifier.
        :param chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
        :param message_id: Required if inline_message_id is not specified. Identifier of the sent message.
        :param inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
        :return: An Array of GameHighScore objects on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError(
                "Either (chat_id and message_id) or inline_message_id must be provided."
            )

        payload = {
            "user_id": user_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
        }
        response = self._make_request("getGameHighScores", method="GET", params=payload)
        return [GameHighScore.model_validate(game) for game in response]

    def is_join_channel(self, chat_id, user_id, **kwargs):
        if chat_id.isnumeric():
            chat_id = chat_id if "@" in chat_id else "@" + str(chat_id)

        rsp = self.get_chat_member(chat_id, user_id)
        return rsp.status != "left"
