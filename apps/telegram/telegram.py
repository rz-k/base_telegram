import json
from typing import Any, Dict, List, Optional, Union

import requests

from apps.telegram._types import (
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    MessageEntity,
    ReplyMarkup,
    ReplyParameters,
    SuggestedPostParameters,
    WebAppInfo,
)
from utils.load_env import env


class Telegram:
    """
    A fully typed and proxy-ready client for the Telegram Bot API (v9.2).
    Designed for clean, maintainable, and production-grade bot development.
    """

    BASE_URL: str = "https://api.telegram.org/bot{}/{}"
    HEADERS: Dict[str, str] = {"Cache-Control": "no-cache"}

    def __init__(self):
        self.token = env.get("TOKEN")
        if not self.token:
            raise ValueError("TOKEN is required in environment variables.")

        self.proxy = self._setup_proxy()
        self._session = requests.Session()
        self._session.headers.update(self.HEADERS)

    def _setup_proxy(self) -> Optional[Dict[str, str]]:
        """Configure SOCKS5 proxy if provided."""
        proxy_socks = env.get("PROXY_SOCKS")
        if proxy_socks:
            return {
                "http": f"socks5h://{proxy_socks}",
                "https": f"socks5h://{proxy_socks}"
            }
        return {}

    def _make_request(
        self,
        method_name: str,
        method: str = "POST",
        data: Optional[Dict[Any, Any]] = None,
        params: Optional[Dict[Any, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[Any, Any]:
        """
        Send HTTP request to Telegram Bot API.
        """
        url = self.BASE_URL.format(self.token, method_name)
        if data:
            for k, v in data.items():
                if isinstance(v, dict):
                    data[k] = json.dumps(v)
        if params:
            for k, v in data.items():
                if isinstance(v, dict):
                    data[k] = json.dumps(v)
        try:
            if method.upper() == "GET":
                response = self._session.get(
                    url, params=params, proxies=self.proxy, timeout=timeout
                )
            else:
                response = self._session.post(
                    url, data=data, params=params, files=files,
                    proxies=self.proxy, timeout=timeout
                )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[Telegram API Error] {method_name}: {e}")
            return {"ok": False, "error": str(e)}

    def close(self):
        """Close the session."""
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # =============================
    # === SEND MESSAGE METHOD ===
    # =============================

    def send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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

        # Remove None values before sending
        filtered_payload = {k: v for k, v in payload.items() if v is not None}

        return self._make_request("sendMessage", data=filtered_payload)

    def forward_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None
    ) -> Dict[Any, Any]:
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
        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("forwardMessage", data=filtered_payload)

    def forward_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: List[int],
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Dict[Any, Any]:
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
        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("forwardMessages", data=filtered_payload)

    def copy_message(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        video_start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("copyMessage", data=filtered_payload)

    def copy_messages(
        self,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: List[int],
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        remove_caption: Optional[bool] = None
    ) -> Dict[Any, Any]:
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
        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("copyMessages", data=filtered_payload)

    def send_photo(
        self,
        chat_id: Union[int, str],
        photo: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendPhoto", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use GET
            payload["photo"] = photo
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendPhoto", method="GET", params=filtered_params)

    def send_audio(
        self,
        chat_id: Union[int, str],
        audio: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        performer: Optional[str] = None,
        title: Optional[str] = None,
        thumbnail: Optional[Union[str, bytes]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendAudio", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use GET
            payload["audio"] = audio
            if thumbnail:
                payload["thumbnail"] = thumbnail
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendAudio", method="GET", params=filtered_params)

    def send_document(
        self,
        chat_id: Union[int, str],
        document: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        thumbnail: Optional[Union[str, bytes]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        disable_content_type_detection: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendDocument", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use GET
            payload["document"] = document
            if thumbnail:
                payload["thumbnail"] = thumbnail
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendDocument", method="GET", params=filtered_params)

    def send_video(
        self,
        chat_id: Union[int, str],
        video: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[str, bytes]] = None,
        cover: Optional[Union[str, bytes]] = None,
        start_timestamp: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        supports_streaming: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendVideo", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use GET
            payload["video"] = video
            if thumbnail:
                payload["thumbnail"] = thumbnail
            if cover:
                payload["cover"] = cover
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendVideo", method="GET", params=filtered_params)

    def send_animation(
        self,
        chat_id: Union[int, str],
        animation: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        duration: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        thumbnail: Optional[Union[str, bytes]] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        has_spoiler: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendAnimation", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use GET
            payload["animation"] = animation
            if thumbnail:
                payload["thumbnail"] = thumbnail
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendAnimation", method="GET", params=filtered_params)

    def send_voice(
        self,
        chat_id: Union[int, str],
        voice: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        duration: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendVoice", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use GET
            payload["voice"] = voice
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendVoice", method="GET", params=filtered_params)

    def send_video_note(
        self,
        chat_id: Union[int, str],
        video_note: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        duration: Optional[int] = None,
        length: Optional[int] = None,
        thumbnail: Optional[Union[str, bytes]] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendVideoNote", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id → use GET (URL not supported per API)
            payload["video_note"] = video_note
            if thumbnail:
                payload["thumbnail"] = thumbnail
            filtered_params = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendVideoNote", method="GET", params=filtered_params)

    def send_paid_media(
        self,
        chat_id: Union[int, str],
        star_count: int,
        media: List[Dict[str, Any]],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        payload: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload_data.items() if v is not None}
        return self._make_request("sendPaidMedia", method="POST", data=filtered_payload)

    def send_media_group(
        self,
        chat_id: Union[int, str],
        media: List[Dict[str, Any]],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendMediaGroup", method="POST", data=filtered_payload)

    def send_location(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendLocation", method="POST", data=filtered_payload)

    def send_venue(
        self,
        chat_id: Union[int, str],
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendVenue", method="POST", data=filtered_payload)

    def send_contact(
        self,
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendContact", method="POST", data=filtered_payload)

    def send_poll(
        self,
        chat_id: Union[int, str],
        question: str,
        options: List[str],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        question_parse_mode: Optional[str] = None,
        question_entities: Optional[List[MessageEntity]] = None,
        is_anonymous: Optional[bool] = None,
        poll_type: Optional[str] = None,
        allows_multiple_answers: Optional[bool] = None,
        correct_option_id: Optional[int] = None,
        explanation: Optional[str] = None,
        explanation_parse_mode: Optional[str] = None,
        explanation_entities: Optional[List[MessageEntity]] = None,
        open_period: Optional[int] = None,
        close_date: Optional[int] = None,
        is_closed: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
        :param allows_multiple_answers: True if multiple answers are allowed (ignored in quiz mode, default: False).
        :param correct_option_id: 0-based index of the correct answer option (required for quiz mode).
        :param explanation: Text shown when an incorrect answer is chosen (0–200 characters).
        :param explanation_parse_mode: Mode for parsing entities in the explanation.
        :param explanation_entities: List of special entities in the explanation.
        :param open_period: Duration in seconds the poll will be active (5–600). Cannot be used with close_date.
        :param close_date: Unix timestamp when the poll will be automatically closed (5–600 seconds in future).
                        Cannot be used with open_period.
        :param is_closed: Pass True to immediately close the poll (useful for preview).
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
            "business_connection_id": business_connection_id,
            "message_thread_id": message_thread_id,
            "question": question,
            "question_parse_mode": question_parse_mode,
            "question_entities": question_entities,
            "options": json.dumps(options),
            "is_anonymous": is_anonymous,
            "type": poll_type,
            "allows_multiple_answers": allows_multiple_answers,
            "correct_option_id": correct_option_id,
            "explanation": explanation,
            "explanation_parse_mode": explanation_parse_mode,
            "explanation_entities": explanation_entities,
            "open_period": open_period,
            "close_date": close_date,
            "is_closed": is_closed,
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "allow_paid_broadcast": allow_paid_broadcast,
            "message_effect_id": message_effect_id,
            "reply_parameters": reply_parameters,
            "reply_markup": reply_markup,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendPoll", method="POST", data=filtered_payload)

    def send_checklist(
        self,
        business_connection_id: str,
        chat_id: int,
        checklist: Dict[str, Any],
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendChecklist", method="POST", data=filtered_payload)

    def send_dice(
        self,
        chat_id: Union[int, str],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendDice", method="POST", data=filtered_payload)

    def send_chat_action(
        self,
        chat_id: Union[int, str],
        action: str,
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendChatAction", method="POST", data=filtered_payload)

    def set_message_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        reaction: Optional[List[Dict[str, Any]]] = None,
        is_big: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setMessageReaction", method="POST", data=filtered_payload)

    def get_user_profile_photos(
        self,
        user_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getUserProfilePhotos", method="GET", params=filtered_params)

    def set_user_emoji_status(
        self,
        user_id: int,
        emoji_status_custom_emoji_id: Optional[str] = None,
        emoji_status_expiration_date: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setUserEmojiStatus", method="POST", data=filtered_payload)

    def get_file(
        self,
        file_id: str
    ) -> Dict[Any, Any]:
        """
        Get basic information about a file and prepare it for downloading.

        :param file_id: File identifier to get information about.
        :return: A File object on success. The file can be downloaded via https://api.telegram.org/file/bot<token>/<file_path>.
                The link is guaranteed to be valid for at least 1 hour.
        """
        payload = {"file_id": file_id}
        return self._make_request("getFile", method="GET", params=payload)

    def ban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        until_date: Optional[int] = None,
        revoke_messages: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("banChatMember", method="POST", data=filtered_payload)

    def unban_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        only_if_banned: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("unbanChatMember", method="POST", data=filtered_payload)

    def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        permissions: Dict[str, Any],
        use_independent_chat_permissions: Optional[bool] = None,
        until_date: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("restrictChatMember", method="POST", data=filtered_payload)

    def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int,
        is_anonymous: Optional[bool] = None,
        can_manage_chat: Optional[bool] = None,
        can_delete_messages: Optional[bool] = None,
        can_manage_video_chats: Optional[bool] = None,
        can_restrict_members: Optional[bool] = None,
        can_promote_members: Optional[bool] = None,
        can_change_info: Optional[bool] = None,
        can_invite_users: Optional[bool] = None,
        can_post_stories: Optional[bool] = None,
        can_edit_stories: Optional[bool] = None,
        can_delete_stories: Optional[bool] = None,
        can_post_messages: Optional[bool] = None,
        can_edit_messages: Optional[bool] = None,
        can_pin_messages: Optional[bool] = None,
        can_manage_topics: Optional[bool] = None,
        can_manage_direct_messages: Optional[bool] = None
    ) -> Dict[Any, Any]:
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
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("promoteChatMember", method="POST", data=filtered_payload)

    def set_chat_administrator_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: int,
        custom_title: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("setChatAdministratorCustomTitle", method="POST", data=payload)

    def ban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("banChatSenderChat", method="POST", data=payload)

    def unban_chat_sender_chat(
        self,
        chat_id: Union[int, str],
        sender_chat_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("unbanChatSenderChat", method="POST", data=payload)

    def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: Dict[str, Any],
        use_independent_chat_permissions: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setChatPermissions", method="POST", data=filtered_payload)

    def export_chat_invite_link(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Generate a new primary invite link for a chat. Any previous primary link is revoked.
        The bot must be an administrator with appropriate rights.
        Each administrator (including bots) has their own invite links.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: The new invite link as a string on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("exportChatInviteLink", method="GET", params=payload)

    def create_chat_invite_link(
        self,
        chat_id: Union[int, str],
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("createChatInviteLink", method="POST", data=filtered_payload)

    def edit_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        name: Optional[str] = None,
        expire_date: Optional[int] = None,
        member_limit: Optional[int] = None,
        creates_join_request: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editChatInviteLink", method="POST", data=filtered_payload)

    def create_chat_subscription_invite_link(
        self,
        chat_id: Union[int, str],
        subscription_period: int,
        subscription_price: int,
        name: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("createChatSubscriptionInviteLink", method="POST", data=filtered_payload)

    def edit_chat_subscription_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str,
        name: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editChatSubscriptionInviteLink", method="POST", data=filtered_payload)

    def revoke_chat_invite_link(
        self,
        chat_id: Union[int, str],
        invite_link: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("revokeChatInviteLink", method="POST", data=payload)

    def approve_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("approveChatJoinRequest", method="POST", data=payload)

    def decline_chat_join_request(
        self,
        chat_id: Union[int, str],
        user_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("declineChatJoinRequest", method="POST", data=payload)

    def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: bytes
    ) -> Dict[Any, Any]:
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
        return self._make_request("setChatPhoto", method="POST", data=payload, files=files)

    def delete_chat_photo(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Delete the current profile photo of the chat.
        Not available for private chats.
        The bot must be an administrator with appropriate rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("deleteChatPhoto", method="POST", data=payload)

    def set_chat_title(
        self,
        chat_id: Union[int, str],
        title: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("setChatTitle", method="POST", data=payload)

    def set_chat_description(
        self,
        chat_id: Union[int, str],
        description: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setChatDescription", method="POST", data=filtered_payload)

    def pin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
        business_connection_id: Optional[str] = None,
        disable_notification: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("pinChatMessage", method="POST", data=filtered_payload)

    def unpin_chat_message(
        self,
        chat_id: Union[int, str],
        message_id: Optional[int] = None,
        business_connection_id: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("unpinChatMessage", method="POST", data=filtered_payload)

    def unpin_all_chat_messages(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Clear all pinned messages in a chat.
        No special rights needed in private chats or channel direct messages.
        In groups and channels, the bot must have 'can_pin_messages' or 'can_edit_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("unpinAllChatMessages", method="POST", data=payload)

    def leave_chat(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Make the bot leave a group, supergroup, or channel.
        Channel direct messages chats are not supported; leave the corresponding channel instead.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("leaveChat", method="POST", data=payload)

    def get_chat(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Get up-to-date information about a chat (group, supergroup, channel, or private chat).
        Returns a ChatFullInfo object.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: A ChatFullInfo object on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("getChat", method="GET", params=payload)

    def get_chat_administrators(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Get a list of administrators in a chat (excluding bots).
        Returns an array of ChatMember objects.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: Array of ChatMember objects on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("getChatAdministrators", method="GET", params=payload)

    def get_chat_member_count(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Get the number of members in a chat.
        Returns an integer on success.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
        :return: Number of members in the chat.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("getChatMemberCount", method="GET", params=payload)

    def get_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("getChatMember", method="GET", params=payload)

    def set_chat_sticker_set(
        self,
        chat_id: Union[int, str],
        sticker_set_name: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("setChatStickerSet", method="POST", data=payload)

    def delete_chat_sticker_set(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Delete the group sticker set from a supergroup.
        The bot must be an administrator with appropriate rights.
        Use getChat to check if the bot can_set_sticker_set.

        :param chat_id: Unique identifier for the target supergroup or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("deleteChatStickerSet", method="POST", data=payload)

    def get_forum_topic_icon_stickers(self) -> Dict[Any, Any]:
        """
        Get custom emoji stickers that can be used as forum topic icons by any user.
        This method requires no parameters.

        :return: An Array of Sticker objects on success.
        """
        return self._make_request("getForumTopicIconStickers", method="GET")

    def create_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str,
        icon_color: Optional[int] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("createForumTopic", method="POST", data=filtered_payload)

    def edit_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int,
        name: Optional[str] = None,
        icon_custom_emoji_id: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editForumTopic", method="POST", data=filtered_payload)

    def close_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("closeForumTopic", method="POST", data=payload)

    def reopen_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("reopenForumTopic", method="POST", data=payload)

    def delete_forum_topic(
        self,
        chat_id: Union[int, str],
        message_thread_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("deleteForumTopic", method="POST", data=payload)

    def unpin_all_forum_topic_messages(
        self,
        chat_id: Union[int, str],
        message_thread_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("unpinAllForumTopicMessages", method="POST", data=payload)

    def edit_general_forum_topic(
        self,
        chat_id: Union[int, str],
        name: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("editGeneralForumTopic", method="POST", data=payload)

    def close_general_forum_topic(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Close the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("closeGeneralForumTopic", method="POST", data=payload)

    def reopen_general_forum_topic(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Reopen a closed 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.
        If the topic was hidden, it will be automatically unhidden.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("reopenGeneralForumTopic", method="POST", data=payload)

    def hide_general_forum_topic(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Hide the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.
        The topic will be automatically closed if it was open.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("hideGeneralForumTopic", method="POST", data=payload)

    def unhide_general_forum_topic(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Unhide the 'General' topic in a forum supergroup.
        The bot must be an administrator with 'can_manage_topics' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("unhideGeneralForumTopic", method="POST", data=payload)

    def unpin_all_general_forum_topic_messages(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Clear the list of pinned messages in the 'General' forum topic.
        The bot must be an administrator with 'can_pin_messages' rights.

        :param chat_id: Unique identifier for the target chat or username (e.g. @supergroupusername).
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("unpinAllGeneralForumTopicMessages", method="POST", data=payload)

    def answer_callback_query(
        self,
        callback_query_id: str,
        text: Optional[str] = None,
        show_alert: Optional[bool] = None,
        url: Optional[str] = None,
        cache_time: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("answerCallbackQuery", method="POST", data=filtered_payload)

    def get_user_chat_boosts(
        self,
        chat_id: Union[int, str],
        user_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("getUserChatBoosts", method="GET", params=payload)

    def get_business_connection(
        self,
        business_connection_id: str
    ) -> Dict[Any, Any]:
        """
        Get information about the connection of the bot with a business account.

        :param business_connection_id: Unique identifier of the business connection.
        :return: A BusinessConnection object on success.
        """
        payload = {"business_connection_id": business_connection_id}
        return self._make_request("getBusinessConnection", method="GET", params=payload)

    def set_my_commands(
        self,
        commands: List[Dict[str, Any]],
        scope: Optional[Dict[str, Any]] = None,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setMyCommands", method="POST", data=filtered_payload)

    def delete_my_commands(
        self,
        scope: Optional[Dict[str, Any]] = None,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("deleteMyCommands", method="POST", data=filtered_payload)

    def get_my_commands(
        self,
        scope: Optional[Dict[str, Any]] = None,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getMyCommands", method="GET", params=filtered_params)

    def set_my_name(
        self,
        name: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setMyName", method="POST", data=filtered_payload)

    def get_my_name(
        self,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Get the current bot name for the given user language.

        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: A BotName object on success.
        """
        payload = {"language_code": language_code}
        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getMyName", method="GET", params=filtered_params)

    def set_my_description(
        self,
        description: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setMyDescription", method="POST", data=filtered_payload)

    def get_my_description(
        self,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Get the current bot description for the given user language.

        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: A BotDescription object on success.
        """
        payload = {"language_code": language_code}
        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getMyDescription", method="GET", params=filtered_params)

    def set_my_short_description(
        self,
        short_description: Optional[str] = None,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setMyShortDescription", method="POST", data=filtered_payload)

    def get_my_short_description(
        self,
        language_code: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Get the current bot short description for the given user language.

        :param language_code: A two-letter ISO 639-1 language code or empty string.
        :return: A BotShortDescription object on success.
        """
        payload = {"language_code": language_code}
        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getMyShortDescription", method="GET", params=filtered_params)

    def set_chat_menu_button(
        self,
        chat_id: Optional[int] = None,
        menu_button: Optional[Dict[str, Any]] = None
    ) -> Dict[Any, Any]:
        """
        Change the bot's menu button in a private chat or the default menu button.

        :param chat_id: Unique identifier for the target private chat. If not specified, changes the default menu button.
        :param menu_button: A JSON-serialized MenuButton object. Defaults to MenuButtonDefault.
        :return: True on success.
        """
        payload = {
            "chat_id": chat_id,
            "menu_button": json.dumps(menu_button) if menu_button is not None else None,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setChatMenuButton", method="POST", data=filtered_payload)

    def get_chat_menu_button(
        self,
        chat_id: Optional[int] = None
    ) -> Dict[Any, Any]:
        """
        Get the current value of the bot's menu button in a private chat or the default.

        :param chat_id: Unique identifier for the target private chat. If not specified, returns the default menu button.
        :return: A MenuButton object on success.
        """
        payload = {"chat_id": chat_id}
        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getChatMenuButton", method="GET", params=filtered_params)

    def set_my_default_administrator_rights(
        self,
        rights: Optional[Dict[str, Any]] = None,
        for_channels: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setMyDefaultAdministratorRights", method="POST", data=filtered_payload)

    def get_my_default_administrator_rights(
        self,
        for_channels: Optional[bool] = None
    ) -> Dict[Any, Any]:
        """
        Get the current default administrator rights of the bot.

        :param for_channels: Pass True to get rights for channels. Otherwise, for groups/supergroups.
        :return: A ChatAdministratorRights object on success.
        """
        payload = {"for_channels": for_channels}
        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getMyDefaultAdministratorRights", method="GET", params=filtered_params)

    def get_available_gifts(self) -> Dict[Any, Any]:
        """
        Get the list of gifts that can be sent by the bot to users and channel chats.

        :return: A Gifts object on success.
        """
        return self._make_request("getAvailableGifts", method="GET")

    def send_gift(
        self,
        gift_id: str,
        user_id: Optional[int] = None,
        chat_id: Optional[Union[int, str]] = None,
        pay_for_upgrade: Optional[bool] = None,
        text: Optional[str] = None,
        text_parse_mode: Optional[str] = None,
        text_entities: Optional[List[MessageEntity]] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendGift", method="POST", data=filtered_payload)

    def gift_premium_subscription(
        self,
        user_id: int,
        month_count: int,
        star_count: int,
        text: Optional[str] = None,
        text_parse_mode: Optional[str] = None,
        text_entities: Optional[List[MessageEntity]] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("giftPremiumSubscription", method="POST", data=filtered_payload)

    def verify_user(
        self,
        user_id: int,
        custom_description: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("verifyUser", method="POST", data=filtered_payload)

    def verify_chat(
        self,
        chat_id: Union[int, str],
        custom_description: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("verifyChat", method="POST", data=filtered_payload)

    def remove_user_verification(
        self,
        user_id: int
    ) -> Dict[Any, Any]:
        """
        Remove verification from a user who is currently verified on behalf of the organization.

        :param user_id: Unique identifier of the target user.
        :return: True on success.
        """
        payload = {"user_id": user_id}
        return self._make_request("removeUserVerification", method="POST", data=payload)

    def remove_chat_verification(
        self,
        chat_id: Union[int, str]
    ) -> Dict[Any, Any]:
        """
        Remove verification from a chat that is currently verified on behalf of the organization.

        :param chat_id: Unique identifier for the target chat or username (e.g. @channelusername).
                        Channel direct messages chats cannot be verified.
        :return: True on success.
        """
        payload = {"chat_id": chat_id}
        return self._make_request("removeChatVerification", method="POST", data=payload)

    def read_business_message(
        self,
        business_connection_id: str,
        chat_id: int,
        message_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("readBusinessMessage", method="POST", data=payload)

    def delete_business_messages(
        self,
        business_connection_id: str,
        message_ids: List[int]
    ) -> Dict[Any, Any]:
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
        return self._make_request("deleteBusinessMessages", method="POST", data=payload)

    def set_business_account_name(
        self,
        business_connection_id: str,
        first_name: str,
        last_name: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setBusinessAccountName", method="POST", data=filtered_payload)

    def set_business_account_username(
        self,
        business_connection_id: str,
        username: Optional[str] = None
    ) -> Dict[Any, Any]:
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
        return self._make_request("setBusinessAccountUsername", method="POST", data=payload)

    def set_business_account_bio(
        self,
        business_connection_id: str,
        bio: Optional[str] = None
    ) -> Dict[Any, Any]:
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
        return self._make_request("setBusinessAccountBio", method="POST", data=payload)

    def set_business_account_profile_photo(
        self,
        business_connection_id: str,
        photo: bytes,
        is_public: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setBusinessAccountProfilePhoto", method="POST", data=filtered_payload, files=files)

    def remove_business_account_profile_photo(
        self,
        business_connection_id: str,
        is_public: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("removeBusinessAccountProfilePhoto", method="POST", data=filtered_payload)

    def set_business_account_gift_settings(
        self,
        business_connection_id: str,
        show_gift_button: bool,
        accepted_gift_types: Dict[str, Any]
    ) -> Dict[Any, Any]:
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
        return self._make_request("setBusinessAccountGiftSettings", method="POST", data=payload)

    def get_business_account_star_balance(
        self,
        business_connection_id: str
    ) -> Dict[Any, Any]:
        """
        Get the amount of Telegram Stars owned by a managed business account.
        Requires the 'can_view_gifts_and_stars' business bot right.

        :param business_connection_id: Unique identifier of the business connection.
        :return: A StarAmount object on success.
        """
        payload = {"business_connection_id": business_connection_id}
        return self._make_request("getBusinessAccountStarBalance", method="GET", params=payload)

    def transfer_business_account_stars(
        self,
        business_connection_id: str,
        star_count: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("transferBusinessAccountStars", method="POST", data=payload)

    def get_business_account_gifts(
        self,
        business_connection_id: str,
        exclude_unsaved: Optional[bool] = None,
        exclude_saved: Optional[bool] = None,
        exclude_unlimited: Optional[bool] = None,
        exclude_limited: Optional[bool] = None,
        exclude_unique: Optional[bool] = None,
        sort_by_price: Optional[bool] = None,
        offset: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getBusinessAccountGifts", method="GET", params=filtered_params)

    def convert_gift_to_stars(
        self,
        business_connection_id: str,
        owned_gift_id: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("convertGiftToStars", method="POST", data=payload)

    def upgrade_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        keep_original_details: Optional[bool] = None,
        star_count: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("upgradeGift", method="POST", data=filtered_payload)

    def transfer_gift(
        self,
        business_connection_id: str,
        owned_gift_id: str,
        new_owner_chat_id: int,
        star_count: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("transferGift", method="POST", data=filtered_payload)

    def post_story(
        self,
        business_connection_id: str,
        content: Dict[str, Any],
        active_period: int,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        areas: Optional[List[Dict[str, Any]]] = None,
        post_to_chat_page: Optional[bool] = None,
        protect_content: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("postStory", method="POST", data=filtered_payload)

    def edit_story(
        self,
        business_connection_id: str,
        story_id: int,
        content: Dict[str, Any],
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        areas: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editStory", method="POST", data=filtered_payload)

    def delete_story(
        self,
        business_connection_id: str,
        story_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("deleteStory", method="POST", data=payload)

    def edit_message_text(
        self,
        text: str,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
        :param reply_markup: A JSON-serialized object for a new inline keyboard.
        :return: The edited Message object if not an inline message, otherwise True on success.
        """
        if not (chat_id and message_id) and not inline_message_id:
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "text": text,
            "parse_mode": parse_mode,
            "entities": entities,
            "link_preview_options": link_preview_options,
            "reply_markup": reply_markup,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editMessageText", method="POST", data=filtered_payload)

    def edit_message_caption(
        self,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editMessageCaption", method="POST", data=filtered_payload)

    def edit_message_media(
        self,
        media: Dict[str, Any],
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "media": json.dumps(media),
            "reply_markup": reply_markup,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editMessageMedia", method="POST", data=filtered_payload)

    def edit_message_live_location(
        self,
        latitude: float,
        longitude: float,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        live_period: Optional[int] = None,
        horizontal_accuracy: Optional[float] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editMessageLiveLocation", method="POST", data=filtered_payload)

    def stop_message_live_location(
        self,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("stopMessageLiveLocation", method="POST", data=filtered_payload)

    def edit_message_checklist(
        self,
        business_connection_id: str,
        chat_id: int,
        message_id: int,
        checklist: Dict[str, Any],
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editMessageChecklist", method="POST", data=filtered_payload)

    def edit_message_reply_markup(
        self,
        business_connection_id: Optional[str] = None,
        chat_id: Optional[Union[int, str]] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
            raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

        payload = {
            "business_connection_id": business_connection_id,
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("editMessageReplyMarkup", method="POST", data=filtered_payload)

    def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        business_connection_id: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("stopPoll", method="POST", data=filtered_payload)

    def approve_suggested_post(
        self,
        chat_id: int,
        message_id: int,
        send_date: Optional[int] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("approveSuggestedPost", method="POST", data=filtered_payload)

    def decline_suggested_post(
        self,
        chat_id: int,
        message_id: int,
        comment: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("declineSuggestedPost", method="POST", data=filtered_payload)

    def delete_message(
        self,
        chat_id: Union[int, str],
        message_id: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("deleteMessage", method="POST", data=payload)

    def delete_messages(
        self,
        chat_id: Union[int, str],
        message_ids: List[int]
    ) -> Dict[Any, Any]:
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
        return self._make_request("deleteMessages", method="POST", data=payload)

    def send_sticker(
        self,
        chat_id: Union[int, str],
        sticker: Union[str, bytes],
        business_connection_id: Optional[str] = None,
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        emoji: Optional[str] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[ReplyMarkup] = None
    ) -> Dict[Any, Any]:
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
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendSticker", method="POST", data=filtered_payload, files=files)
        else:
            # Reuse existing file_id or URL → use POST (GET not supported for stickers)
            payload["sticker"] = sticker
            filtered_payload = {k: v for k, v in payload.items() if v is not None}
            return self._make_request("sendSticker", method="POST", data=filtered_payload)

    def get_sticker_set(
        self,
        name: str
    ) -> Dict[Any, Any]:
        """
        Get information about a sticker set.

        :param name: Name of the sticker set (e.g., 'my_stickers_by_botname').
        :return: A StickerSet object on success.
        """
        payload = {"name": name}
        return self._make_request("getStickerSet", method="GET", params=payload)

    def get_custom_emoji_stickers(
        self,
        custom_emoji_ids: List[str]
    ) -> Dict[Any, Any]:
        """
        Get information about custom emoji stickers by their identifiers.

        :param custom_emoji_ids: A list of up to 200 unique identifiers of custom emoji stickers.
        :return: An Array of Sticker objects on success.
        """
        payload = {"custom_emoji_ids": json.dumps(custom_emoji_ids)}
        return self._make_request("getCustomEmojiStickers", method="POST", data=payload)

    def upload_sticker_file(
        self,
        user_id: int,
        sticker: bytes,
        sticker_format: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("uploadStickerFile", method="POST", data=payload, files=files)

    def create_new_sticker_set(
        self,
        user_id: int,
        name: str,
        title: str,
        stickers: List[Dict[str, Any]],
        sticker_type: Optional[str] = None,
        needs_repainting: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("createNewStickerSet", method="POST", data=filtered_payload)

    def add_sticker_to_set(
        self,
        user_id: int,
        name: str,
        sticker: Dict[str, Any]
    ) -> Dict[Any, Any]:
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
        return self._make_request("addStickerToSet", method="POST", data=payload)

    def set_sticker_position_in_set(
        self,
        sticker: str,
        position: int
    ) -> Dict[Any, Any]:
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
        return self._make_request("setStickerPositionInSet", method="POST", data=payload)

    def delete_sticker_from_set(
        self,
        sticker: str
    ) -> Dict[Any, Any]:
        """
        Delete a sticker from a set created by the bot.

        :param sticker: File identifier of the sticker to delete.
        :return: True on success.
        """
        payload = {"sticker": sticker}
        return self._make_request("deleteStickerFromSet", method="POST", data=payload)

    def replace_sticker_in_set(
        self,
        user_id: int,
        name: str,
        old_sticker: str,
        sticker: Dict[str, Any]
    ) -> Dict[Any, Any]:
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
            "sticker": json.dumps(sticker),
        }
        return self._make_request("replaceStickerInSet", method="POST", data=payload)

    def set_sticker_emoji_list(
        self,
        sticker: str,
        emoji_list: List[str]
    ) -> Dict[Any, Any]:
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
        return self._make_request("setStickerEmojiList", method="POST", data=payload)

    def set_sticker_keywords(
        self,
        sticker: str,
        keywords: Optional[List[str]] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setStickerKeywords", method="POST", data=filtered_payload)

    def set_sticker_mask_position(
        self,
        sticker: str,
        mask_position: Optional[Dict[str, Any]] = None
    ) -> Dict[Any, Any]:
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
            "mask_position": json.dumps(mask_position) if mask_position is not None else None,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setStickerMaskPosition", method="POST", data=filtered_payload)

    def set_sticker_set_title(
        self,
        name: str,
        title: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("setStickerSetTitle", method="POST", data=payload)

    def set_sticker_set_thumbnail(
        self,
        name: str,
        user_id: int,
        thumbnail: Optional[Union[str, bytes]] = None,
        format: str = "static"
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("setStickerSetThumbnail", method="POST", data=filtered_payload, files=files)

    def set_custom_emoji_sticker_set_thumbnail(
        self,
        name: str,
        custom_emoji_id: Optional[str] = None
    ) -> Dict[Any, Any]:
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
        return self._make_request("setCustomEmojiStickerSetThumbnail", method="POST", data=payload)

    def delete_sticker_set(
        self,
        name: str
    ) -> Dict[Any, Any]:
        """
        Delete a sticker set that was created by the bot.

        :param name: Name of the sticker set to delete.
        :return: True on success.
        """
        payload = {"name": name}
        return self._make_request("deleteStickerSet", method="POST", data=payload)

    def answer_inline_query(
        self,
        inline_query_id: str,
        results: List[Dict[str, Any]],
        cache_time: Optional[int] = None,
        is_personal: Optional[bool] = None,
        next_offset: Optional[str] = None,
        button: Optional[Dict[str, Any]] = None
    ) -> Dict[Any, Any]:
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
            "results": json.dumps(results),
            "cache_time": cache_time,
            "is_personal": is_personal,
            "next_offset": next_offset,
            "button": json.dumps(button) if button is not None else None,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("answerInlineQuery", method="POST", data=filtered_payload)

    def create_inline_query_result_article(
        id: str,
        title: str,
        input_message_content: Dict[str, Any],
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        url: Optional[str] = None,
        description: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultArticle object.

        Represents a link to an article or web page.

        :param id: Unique identifier for this result, 1-64 bytes.
        :param title: Title of the result.
        :param input_message_content: Content of the message to be sent when the result is chosen.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param url: Optional URL of the result.
        :param description: Optional short description of the result.
        :param thumbnail_url: Optional URL of the thumbnail for the result.
        :param thumbnail_width: Optional width of the thumbnail.
        :param thumbnail_height: Optional height of the thumbnail.
        :return: A dictionary representing an InlineQueryResultArticle.
        """
        result = {
            "type": "article",
            "id": id,
            "title": title,
            "input_message_content": input_message_content,
            "reply_markup": reply_markup,
            "url": url,
            "description": description,
            "thumbnail_url": thumbnail_url,
            "thumbnail_width": thumbnail_width,
            "thumbnail_height": thumbnail_height,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_photo(
        id: str,
        photo_url: str,
        thumbnail_url: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultPhoto object.

        Represents a link to a photo. By default, this photo will be sent by the user with optional caption.
        Alternatively, you can use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1-64 bytes.
        :param photo_url: A valid URL of the photo (JPEG only, max 5MB).
        :param thumbnail_url: URL of the thumbnail (JPEG/GIF/MP4, recommended 80x80).
        :param title: Optional title for the result.
        :param description: Optional short description of the result.
        :param caption: Optional caption of the photo to be sent (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (can be used instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the photo.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the photo.
        :param photo_width: Optional width of the photo.
        :param photo_height: Optional height of the photo.
        :return: A dictionary representing an InlineQueryResultPhoto.
        """
        result = {
            "type": "photo",
            "id": id,
            "photo_url": photo_url,
            "thumbnail_url": thumbnail_url,
            "title": title,
            "description": description,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
            "photo_width": photo_width,
            "photo_height": photo_height,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_gif(
        id: str,
        gif_url: str,
        thumbnail_url: str,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        gif_width: Optional[int] = None,
        gif_height: Optional[int] = None,
        gif_duration: Optional[int] = None,
        thumbnail_mime_type: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultGif object.

        Represents a link to an animated GIF file.
        By default, this GIF will be sent by the user with optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1-64 bytes.
        :param gif_url: A valid URL for the GIF file.
        :param thumbnail_url: URL of the static (JPEG/GIF) or animated (MPEG4) thumbnail.
        :param title: Optional title for the result.
        :param caption: Optional caption of the GIF (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the GIF.
        :param gif_width: Optional width of the GIF.
        :param gif_height: Optional height of the GIF.
        :param gif_duration: Optional duration of the GIF in seconds.
        :param thumbnail_mime_type: MIME type of the thumbnail: 'image/jpeg', 'image/gif', or 'video/mp4'. Default: 'image/jpeg'.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the GIF.
        :return: A dictionary representing an InlineQueryResultGif.
        """
        result = {
            "type": "gif",
            "id": id,
            "gif_url": gif_url,
            "thumbnail_url": thumbnail_url,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "gif_width": gif_width,
            "gif_height": gif_height,
            "gif_duration": gif_duration,
            "thumbnail_mime_type": thumbnail_mime_type,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_results_button(
        text: str,
        web_app: Optional[WebAppInfo] = None,
        start_parameter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultsButton object.

        Represents a button to be shown above inline query results.
        You must use exactly one of the optional fields: web_app or start_parameter.

        :param text: Label text on the button.
        :param web_app: Description of the Web App to launch when the button is pressed.
        :param start_parameter: Deep-linking parameter for the /start message sent to the bot when the button is pressed.
                                Must be 1–64 characters, containing only A-Z, a-z, 0-9, _, -.
        :return: A dictionary representing an InlineQueryResultsButton.
        """
        if not web_app and not start_parameter:
            raise ValueError("Either 'web_app' or 'start_parameter' must be provided.")

        button = {
            "text": text,
            "web_app": web_app,
            "start_parameter": start_parameter,
        }
        return {k: v for k, v in button.items() if v is not None}

    def create_inline_query_result_mpeg4_gif(
        id: str,
        mpeg4_url: str,
        thumbnail_url: str,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        mpeg4_width: Optional[int] = None,
        mpeg4_height: Optional[int] = None,
        mpeg4_duration: Optional[int] = None,
        thumbnail_mime_type: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultMpeg4Gif object.

        Represents a link to a video animation (H.264/MPEG-4 AVC without sound).
        By default, the MPEG-4 file will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param mpeg4_url: A valid URL for the MPEG4 file.
        :param thumbnail_url: URL of the static (JPEG/GIF) or animated (MPEG4) thumbnail.
        :param title: Optional title for the result.
        :param caption: Optional caption of the video to be sent (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (can be used instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the video.
        :param mpeg4_width: Optional width of the video.
        :param mpeg4_height: Optional height of the video.
        :param mpeg4_duration: Optional duration of the video in seconds.
        :param thumbnail_mime_type: MIME type of the thumbnail: 'image/jpeg', 'image/gif', or 'video/mp4'. Default: 'image/jpeg'.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the animation.
        :return: A dictionary representing an InlineQueryResultMpeg4Gif.
        """
        result = {
            "type": "mpeg4_gif",
            "id": id,
            "mpeg4_url": mpeg4_url,
            "thumbnail_url": thumbnail_url,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "mpeg4_width": mpeg4_width,
            "mpeg4_height": mpeg4_height,
            "mpeg4_duration": mpeg4_duration,
            "thumbnail_mime_type": thumbnail_mime_type,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_video(
        id: str,
        video_url: str,
        mime_type: str,
        thumbnail_url: str,
        title: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        video_width: Optional[int] = None,
        video_height: Optional[int] = None,
        video_duration: Optional[int] = None,
        description: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultVideo object.

        Represents a link to a page with an embedded video player or a video file.
        By default, the video file will be sent by the user with an optional caption.
        If the video is embedded (e.g., YouTube), you MUST use input_message_content to replace the content.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param video_url: A valid URL for the embedded video player or video file.
        :param mime_type: MIME type of the content: 'text/html' (for embedded players) or 'video/mp4'.
        :param thumbnail_url: URL of the thumbnail (JPEG only).
        :param title: Title for the result.
        :param caption: Optional caption of the video to be sent (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the video.
        :param video_width: Optional width of the video.
        :param video_height: Optional height of the video.
        :param video_duration: Optional duration of the video in seconds.
        :param description: Optional short description of the result.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the video. **Required** if mime_type is 'text/html'.
        :return: A dictionary representing an InlineQueryResultVideo.
        """
        if mime_type not in ("text/html", "video/mp4"):
            raise ValueError("mime_type must be 'text/html' or 'video/mp4'")

        if mime_type == "text/html" and not input_message_content:
            raise ValueError("input_message_content is required when mime_type is 'text/html' (e.g., YouTube)")

        result = {
            "type": "video",
            "id": id,
            "video_url": video_url,
            "mime_type": mime_type,
            "thumbnail_url": thumbnail_url,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "video_width": video_width,
            "video_height": video_height,
            "video_duration": video_duration,
            "description": description,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_audio(
        id: str,
        audio_url: str,
        title: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        performer: Optional[str] = None,
        audio_duration: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultAudio object.

        Represents a link to an MP3 audio file.
        By default, the audio file will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param audio_url: A valid URL for the audio file.
        :param title: Title of the audio.
        :param caption: Optional caption of the audio (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param performer: Optional performer of the audio.
        :param audio_duration: Optional duration of the audio in seconds.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the audio.
        :return: A dictionary representing an InlineQueryResultAudio.
        """
        result = {
            "type": "audio",
            "id": id,
            "audio_url": audio_url,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "performer": performer,
            "audio_duration": audio_duration,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_voice(
        id: str,
        voice_url: str,
        title: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        voice_duration: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultVoice object.

        Represents a link to a voice recording (.OGG with OPUS).
        By default, the voice recording will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param voice_url: A valid URL for the voice recording.
        :param title: Title of the recording.
        :param caption: Optional caption of the voice message (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param voice_duration: Optional duration of the recording in seconds.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the voice recording.
        :return: A dictionary representing an InlineQueryResultVoice.
        """
        result = {
            "type": "voice",
            "id": id,
            "voice_url": voice_url,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "voice_duration": voice_duration,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_document(
        id: str,
        title: str,
        document_url: str,
        mime_type: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        description: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultDocument object.

        Represents a link to a file (.PDF or .ZIP).
        By default, the file will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param title: Title for the result.
        :param document_url: A valid URL for the file.
        :param mime_type: MIME type: 'application/pdf' or 'application/zip'.
        :param caption: Optional caption of the document (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param description: Optional short description of the result.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the file.
        :param thumbnail_url: Optional URL of the thumbnail (JPEG only).
        :param thumbnail_width: Optional width of the thumbnail.
        :param thumbnail_height: Optional height of the thumbnail.
        :return: A dictionary representing an InlineQueryResultDocument.
        """
        if mime_type not in ("application/pdf", "application/zip"):
            raise ValueError("mime_type must be 'application/pdf' or 'application/zip'")

        result = {
            "type": "document",
            "id": id,
            "title": title,
            "document_url": document_url,
            "mime_type": mime_type,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "description": description,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
            "thumbnail_url": thumbnail_url,
            "thumbnail_width": thumbnail_width,
            "thumbnail_height": thumbnail_height,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_location(
        id: str,
        latitude: float,
        longitude: float,
        title: str,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultLocation object.

        Represents a location on a map.
        By default, the location will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param latitude: Location latitude in degrees.
        :param longitude: Location longitude in degrees.
        :param title: Title of the location.
        :param horizontal_accuracy: Radius of uncertainty for the location in meters (0–1500).
        :param live_period: Period in seconds during which the location can be updated (60–86400 or 0x7FFFFFFF).
        :param heading: Direction of movement in degrees (1–360).
        :param proximity_alert_radius: Maximum distance for proximity alerts in meters (1–100000).
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the location.
        :param thumbnail_url: Optional URL of the thumbnail for the result.
        :param thumbnail_width: Optional width of the thumbnail.
        :param thumbnail_height: Optional height of the thumbnail.
        :return: A dictionary representing an InlineQueryResultLocation.
        """
        result = {
            "type": "location",
            "id": id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "horizontal_accuracy": horizontal_accuracy,
            "live_period": live_period,
            "heading": heading,
            "proximity_alert_radius": proximity_alert_radius,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
            "thumbnail_url": thumbnail_url,
            "thumbnail_width": thumbnail_width,
            "thumbnail_height": thumbnail_height,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_venue(
        id: str,
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultVenue object.

        Represents a venue.
        By default, the venue will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param latitude: Latitude of the venue in degrees.
        :param longitude: Longitude of the venue in degrees.
        :param title: Title of the venue.
        :param address: Address of the venue.
        :param foursquare_id: Optional Foursquare identifier of the venue.
        :param foursquare_type: Optional Foursquare type of the venue (e.g., 'arts_entertainment/aquarium').
        :param google_place_id: Optional Google Places identifier of the venue.
        :param google_place_type: Optional Google Places type of the venue.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the venue.
        :param thumbnail_url: Optional URL of the thumbnail for the result.
        :param thumbnail_width: Optional width of the thumbnail.
        :param thumbnail_height: Optional height of the thumbnail.
        :return: A dictionary representing an InlineQueryResultVenue.
        """
        result = {
            "type": "venue",
            "id": id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address,
            "foursquare_id": foursquare_id,
            "foursquare_type": foursquare_type,
            "google_place_id": google_place_id,
            "google_place_type": google_place_type,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
            "thumbnail_url": thumbnail_url,
            "thumbnail_width": thumbnail_width,
            "thumbnail_height": thumbnail_height,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_contact(
        id: str,
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None,
        thumbnail_url: Optional[str] = None,
        thumbnail_width: Optional[int] = None,
        thumbnail_height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultContact object.

        Represents a contact with a phone number.
        By default, the contact will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param phone_number: Contact's phone number.
        :param first_name: Contact's first name.
        :param last_name: Optional contact's last name.
        :param vcard: Optional vCard data about the contact (0–2048 bytes).
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the contact.
        :param thumbnail_url: Optional URL of the thumbnail for the result.
        :param thumbnail_width: Optional width of the thumbnail.
        :param thumbnail_height: Optional height of the thumbnail.
        :return: A dictionary representing an InlineQueryResultContact.
        """
        result = {
            "type": "contact",
            "id": id,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "vcard": vcard,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
            "thumbnail_url": thumbnail_url,
            "thumbnail_width": thumbnail_width,
            "thumbnail_height": thumbnail_height,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_game(
        id: str,
        game_short_name: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultGame object.

        Represents a game.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param game_short_name: Short name of the game.
        :param reply_markup: Optional inline keyboard attached to the message.
        :return: A dictionary representing an InlineQueryResultGame.
        """
        result = {
            "type": "game",
            "id": id,
            "game_short_name": game_short_name,
            "reply_markup": reply_markup,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_photo(
        id: str,
        photo_file_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedPhoto object.

        Represents a link to a photo stored on Telegram servers.
        By default, the photo will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param photo_file_id: A valid file identifier of the photo stored on Telegram servers.
        :param title: Optional title for the result.
        :param description: Optional short description of the result.
        :param caption: Optional caption of the photo (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the photo.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the photo.
        :return: A dictionary representing an InlineQueryResultCachedPhoto.
        """
        result = {
            "type": "photo",
            "id": id,
            "photo_file_id": photo_file_id,
            "title": title,
            "description": description,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_gif(
        id: str,
        gif_file_id: str,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedGif object.

        Represents a link to an animated GIF stored on Telegram servers.
        By default, the GIF will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param gif_file_id: A valid file identifier for the GIF stored on Telegram servers.
        :param title: Optional title for the result.
        :param caption: Optional caption of the GIF (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the GIF.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the GIF animation.
        :return: A dictionary representing an InlineQueryResultCachedGif.
        """
        result = {
            "type": "gif",
            "id": id,
            "gif_file_id": gif_file_id,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_mpeg4_gif(
        id: str,
        mpeg4_file_id: str,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedMpeg4Gif object.

        Represents a link to a video animation (H.264/MPEG-4 AVC without sound) stored on Telegram servers.
        By default, the MPEG-4 file will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param mpeg4_file_id: A valid file identifier for the MPEG4 file stored on Telegram servers.
        :param title: Optional title for the result.
        :param caption: Optional caption of the video to be sent (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (can be used instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the video.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the animation.
        :return: A dictionary representing an InlineQueryResultCachedMpeg4Gif.
        """
        result = {
            "type": "mpeg4_gif",
            "id": id,
            "mpeg4_file_id": mpeg4_file_id,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_sticker(
        id: str,
        sticker_file_id: str,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedSticker object.

        Represents a link to a sticker stored on Telegram servers.
        By default, the sticker will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param sticker_file_id: A valid file identifier of the sticker stored on Telegram servers.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the sticker.
        :return: A dictionary representing an InlineQueryResultCachedSticker.
        """
        result = {
            "type": "sticker",
            "id": id,
            "sticker_file_id": sticker_file_id,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_document(
        id: str,
        title: str,
        document_file_id: str,
        description: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedDocument object.

        Represents a link to a file stored on Telegram servers.
        By default, the file will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param title: Title for the result.
        :param document_file_id: A valid file identifier for the document stored on Telegram servers.
        :param description: Optional short description of the result.
        :param caption: Optional caption of the document (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the file.
        :return: A dictionary representing an InlineQueryResultCachedDocument.
        """
        result = {
            "type": "document",
            "id": id,
            "title": title,
            "document_file_id": document_file_id,
            "description": description,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_video(
        id: str,
        video_file_id: str,
        title: str,
        description: Optional[str] = None,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        show_caption_above_media: Optional[bool] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedVideo object.

        Represents a link to a video file stored on Telegram servers.
        By default, the video will be sent by the user with an optional caption.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param video_file_id: A valid file identifier for the video stored on Telegram servers.
        :param title: Title for the result.
        :param description: Optional short description of the result.
        :param caption: Optional caption of the video (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param show_caption_above_media: Pass True to show the caption above the video.
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the video.
        :return: A dictionary representing an InlineQueryResultCachedVideo.
        """
        result = {
            "type": "video",
            "id": id,
            "video_file_id": video_file_id,
            "title": title,
            "description": description,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "show_caption_above_media": show_caption_above_media,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_voice(
        id: str,
        voice_file_id: str,
        title: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedVoice object.

        Represents a link to a voice message stored on Telegram servers.
        By default, the voice message will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param voice_file_id: A valid file identifier for the voice message stored on Telegram servers.
        :param title: Title of the voice message.
        :param caption: Optional caption of the voice message (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the voice recording.
        :return: A dictionary representing an InlineQueryResultCachedVoice.
        """
        result = {
            "type": "voice",
            "id": id,
            "voice_file_id": voice_file_id,
            "title": title,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_inline_query_result_cached_audio(
        id: str,
        audio_file_id: str,
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None,
        caption_entities: Optional[List[MessageEntity]] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create an InlineQueryResultCachedAudio object.

        Represents a link to an MP3 audio file stored on Telegram servers.
        By default, the audio file will be sent by the user.
        Alternatively, use input_message_content to send a different message.

        :param id: Unique identifier for this result, 1–64 bytes.
        :param audio_file_id: A valid file identifier for the audio file stored on Telegram servers.
        :param caption: Optional caption of the audio (0–1024 characters).
        :param parse_mode: Mode for parsing entities in the caption ('HTML', 'MarkdownV2').
        :param caption_entities: List of special entities in the caption (instead of parse_mode).
        :param reply_markup: Optional inline keyboard attached to the message.
        :param input_message_content: Content to send instead of the audio.
        :return: A dictionary representing an InlineQueryResultCachedAudio.
        """
        result = {
            "type": "audio",
            "id": id,
            "audio_file_id": audio_file_id,
            "caption": caption,
            "parse_mode": parse_mode,
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
            "input_message_content": input_message_content,
        }
        return {k: v for k, v in result.items() if v is not None}

    def create_input_text_message_content(
        message_text: str,
        parse_mode: Optional[str] = None,
        entities: Optional[List[MessageEntity]] = None,
        link_preview_options: Optional[LinkPreviewOptions] = None
    ) -> Dict[str, Any]:
        """
        Create an InputTextMessageContent object.

        Represents the content of a text message to be sent as the result of an inline query.

        :param message_text: Text of the message to be sent (1–4096 characters).
        :param parse_mode: Mode for parsing entities in the text ('HTML', 'MarkdownV2').
        :param entities: List of special entities in the text (can be used instead of parse_mode).
        :param link_preview_options: Options for link preview generation.
        :return: A dictionary representing an InputTextMessageContent.
        """
        content = {
            "message_text": message_text,
            "parse_mode": parse_mode,
            "entities": entities,
            "link_preview_options": link_preview_options,
        }
        return {k: v for k, v in content.items() if v is not None}

    def create_input_location_message_content(
        latitude: float,
        longitude: float,
        horizontal_accuracy: Optional[float] = None,
        live_period: Optional[int] = None,
        heading: Optional[int] = None,
        proximity_alert_radius: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an InputLocationMessageContent object.

        Represents the content of a location message to be sent as the result of an inline query.

        :param latitude: Latitude of the location in degrees.
        :param longitude: Longitude of the location in degrees.
        :param horizontal_accuracy: Radius of uncertainty for the location in meters (0–1500).
        :param live_period: Period in seconds during which the location can be updated (60–86400 or 0x7FFFFFFF).
        :param heading: Direction of movement in degrees (1–360).
        :param proximity_alert_radius: Maximum distance for proximity alerts in meters (1–100000).
        :return: A dictionary representing an InputLocationMessageContent.
        """
        content = {
            "latitude": latitude,
            "longitude": longitude,
            "horizontal_accuracy": horizontal_accuracy,
            "live_period": live_period,
            "heading": heading,
            "proximity_alert_radius": proximity_alert_radius,
        }
        return {k: v for k, v in content.items() if v is not None}

    def create_input_venue_message_content(
        latitude: float,
        longitude: float,
        title: str,
        address: str,
        foursquare_id: Optional[str] = None,
        foursquare_type: Optional[str] = None,
        google_place_id: Optional[str] = None,
        google_place_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an InputVenueMessageContent object.

        Represents the content of a venue message to be sent as the result of an inline query.

        :param latitude: Latitude of the venue in degrees.
        :param longitude: Longitude of the venue in degrees.
        :param title: Name of the venue.
        :param address: Address of the venue.
        :param foursquare_id: Optional Foursquare identifier of the venue.
        :param foursquare_type: Optional Foursquare type of the venue (e.g., 'arts_entertainment/aquarium').
        :param google_place_id: Optional Google Places identifier of the venue.
        :param google_place_type: Optional Google Places type of the venue.
        :return: A dictionary representing an InputVenueMessageContent.
        """
        content = {
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address,
            "foursquare_id": foursquare_id,
            "foursquare_type": foursquare_type,
            "google_place_id": google_place_id,
            "google_place_type": google_place_type,
        }
        return {k: v for k, v in content.items() if v is not None}

    def create_input_contact_message_content(
        phone_number: str,
        first_name: str,
        last_name: Optional[str] = None,
        vcard: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create an InputContactMessageContent object.

        Represents the content of a contact message to be sent as the result of an inline query.

        :param phone_number: Contact's phone number.
        :param first_name: Contact's first name.
        :param last_name: Optional contact's last name.
        :param vcard: Optional vCard data about the contact (0–2048 bytes).
        :return: A dictionary representing an InputContactMessageContent.
        """
        content = {
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "vcard": vcard,
        }
        return {k: v for k, v in content.items() if v is not None}

    def create_input_invoice_message_content(
        title: str,
        description: str,
        payload: str,
        provider_token: Optional[str],
        currency: str,
        prices: List[Dict[str, Any]],
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Create an InputInvoiceMessageContent object.

        Represents the content of an invoice message to be sent as the result of an inline query.

        :param title: Product name (1–32 characters).
        :param description: Product description (1–255 characters).
        :param payload: Bot-defined invoice payload (1–128 bytes). Not shown to the user.
        :param provider_token: Payment provider token from @BotFather. Pass empty string for payments in Telegram Stars.
        :param currency: Three-letter ISO 4217 currency code (e.g., 'USD') or 'XTR' for Telegram Stars.
        :param prices: Price breakdown as a list of LabeledPrice objects. Must contain exactly one item for Telegram Stars.
        :param max_tip_amount: Maximum tip amount in smallest currency units (e.g., 145 for $1.45). Defaults to 0.
        :param suggested_tip_amounts: List of suggested tip amounts (positive, increasing, <= max_tip_amount). Max 4 items.
        :param provider_data: JSON-serialized data to share with the payment provider.
        :param photo_url: URL of the product photo for the invoice.
        :param photo_size: Photo size in bytes.
        :param photo_width: Photo width.
        :param photo_height: Photo height.
        :param need_name: Pass True if user's full name is required to complete the order.
        :param need_phone_number: Pass True if user's phone number is required.
        :param need_email: Pass True if user's email address is required.
        :param need_shipping_address: Pass True if shipping address is required.
        :param send_phone_number_to_provider: Pass True to send user's phone number to the provider.
        :param send_email_to_provider: Pass True to send user's email to the provider.
        :param is_flexible: Pass True if the final price depends on the shipping method.
        :return: A dictionary representing an InputInvoiceMessageContent.
        """
        if currency == "XTR" and provider_token != "":
            raise ValueError("For payments in Telegram Stars (XTR), provider_token must be an empty string.")

        content = {
            "title": title,
            "description": description,
            "payload": payload,
            "provider_token": provider_token,
            "currency": currency,
            "prices": prices,
            "max_tip_amount": max_tip_amount,
            "suggested_tip_amounts": suggested_tip_amounts,
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
        return {k: v for k, v in content.items() if v is not None}

    def create_chosen_inline_result(
        result_id: str,
        from_user: Dict[str, Any],
        query: str,
        location: Optional[Dict[str, Any]] = None,
        inline_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a ChosenInlineResult object (simulated for testing or internal use).

        Represents a result of an inline query that was chosen by the user and sent to their chat partner.
        Note: This object is received in updates only if inline feedback is enabled via @BotFather.

        :param result_id: The unique identifier for the result that was chosen.
        :param from_user: The user that chose the result (User object).
        :param query: The query that was used to obtain the result.
        :param location: Optional. Sender's location, only for bots that require user location.
        :param inline_message_id: Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached.
                                Can be used to edit the message later.
        :return: A dictionary representing a ChosenInlineResult object.
        """
        result = {
            "result_id": result_id,
            "from": from_user,
            "query": query,
            "location": location,
            "inline_message_id": inline_message_id,
        }
        return {k: v for k, v in result.items() if v is not None}

    def answer_web_app_query(
        self,
        web_app_query_id: str,
        result: Dict[str, Any]
    ) -> Dict[Any, Any]:
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
        return self._make_request("answerWebAppQuery", method="POST", data=payload)

    def create_sent_web_app_message(
        inline_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a SentWebAppMessage object (typically returned by answerWebAppQuery).

        Describes an inline message sent by a Web App on behalf of a user.

        :param inline_message_id: Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached.
        :return: A dictionary representing a SentWebAppMessage object.
        """
        return {
            "inline_message_id": inline_message_id,
        }

    def save_prepared_inline_message(
        self,
        user_id: int,
        result: Dict[str, Any],
        allow_user_chats: Optional[bool] = None,
        allow_bot_chats: Optional[bool] = None,
        allow_group_chats: Optional[bool] = None,
        allow_channel_chats: Optional[bool] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("savePreparedInlineMessage", method="POST", data=filtered_payload)

    def create_prepared_inline_message(
        id: str,
        expiration_date: int
    ) -> Dict[str, Any]:
        """
        Create a PreparedInlineMessage object (returned by savePreparedInlineMessage).

        Describes an inline message that can be sent by a user of a Mini App.

        :param id: Unique identifier of the prepared message.
        :param expiration_date: Expiration date of the prepared message, in Unix time. Expired messages cannot be used.
        :return: A dictionary representing a PreparedInlineMessage object.
        """
        return {
            "id": id,
            "expiration_date": expiration_date,
        }

    def send_invoice(
        self,
        chat_id: Union[int, str],
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[Dict[str, Any]],
        message_thread_id: Optional[int] = None,
        direct_messages_topic_id: Optional[int] = None,
        provider_token: Optional[str] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        start_parameter: Optional[str] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_paid_broadcast: Optional[bool] = None,
        message_effect_id: Optional[str] = None,
        suggested_post_parameters: Optional[SuggestedPostParameters] = None,
        reply_parameters: Optional[ReplyParameters] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None
    ) -> Dict[Any, Any]:
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
            raise ValueError("For payments in Telegram Stars (XTR), provider_token must be an empty string.")

        payload = {
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("sendInvoice", method="POST", data=filtered_payload)

    def create_invoice_link(
        self,
        title: str,
        description: str,
        payload: str,
        currency: str,
        prices: List[Dict[str, Any]],
        business_connection_id: Optional[str] = None,
        provider_token: Optional[str] = None,
        subscription_period: Optional[int] = None,
        max_tip_amount: Optional[int] = None,
        suggested_tip_amounts: Optional[List[int]] = None,
        provider_data: Optional[str] = None,
        photo_url: Optional[str] = None,
        photo_size: Optional[int] = None,
        photo_width: Optional[int] = None,
        photo_height: Optional[int] = None,
        need_name: Optional[bool] = None,
        need_phone_number: Optional[bool] = None,
        need_email: Optional[bool] = None,
        need_shipping_address: Optional[bool] = None,
        send_phone_number_to_provider: Optional[bool] = None,
        send_email_to_provider: Optional[bool] = None,
        is_flexible: Optional[bool] = None
    ) -> Dict[Any, Any]:
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
                raise ValueError("For payments in Telegram Stars (XTR), provider_token must be an empty string.")
            if subscription_period is not None and subscription_period != 2592000:
                raise ValueError("For Telegram Stars subscriptions, subscription_period must be 2592000 (30 days).")

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
            "suggested_tip_amounts": json.dumps(suggested_tip_amounts) if suggested_tip_amounts is not None else None,
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

        filtered_payload = {k: v for k, v in payload_data.items() if v is not None}
        return self._make_request("createInvoiceLink", method="POST", data=filtered_payload)

    def answer_shipping_query(
        self,
        shipping_query_id: str,
        ok: bool,
        shipping_options: Optional[List[Dict[str, Any]]] = None,
        error_message: Optional[str] = None
    ) -> Dict[Any, Any]:
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
            "shipping_options": json.dumps(shipping_options) if shipping_options is not None else None,
            "error_message": error_message,
        }

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("answerShippingQuery", method="POST", data=filtered_payload)

    def answer_pre_checkout_query(
        self,
        pre_checkout_query_id: str,
        ok: bool,
        error_message: Optional[str] = None
    ) -> Dict[Any, Any]:
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

        filtered_payload = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("answerPreCheckoutQuery", method="POST", data=filtered_payload)

    def get_my_star_balance(self) -> Dict[Any, Any]:
        """
        Get the current Telegram Stars balance of the bot.

        Requires no parameters.

        On success, returns a StarAmount object.

        :return: A StarAmount object containing the bot's current Telegram Stars balance.
        """
        return self._make_request("getMyStarBalance", method="GET")

    def get_star_transactions(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> Dict[Any, Any]:
        """
        Get the bot's Telegram Star transactions in chronological order.

        On success, returns a StarTransactions object.

        :param offset: Number of transactions to skip in the response.
        :param limit: Maximum number of transactions to retrieve (1–100). Defaults to 100.
        :return: A StarTransactions object on success.
        """
        payload = {
            "offset": offset,
            "limit": limit,
        }

        filtered_params = {k: v for k, v in payload.items() if v is not None}
        return self._make_request("getStarTransactions", method="GET", params=filtered_params)

    def refund_star_payment(
        self,
        user_id: int,
        telegram_payment_charge_id: str
    ) -> Dict[Any, Any]:
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
        return self._make_request("refundStarPayment", method="POST", data=payload)

    def edit_user_star_subscription(
        self,
        user_id: int,
        telegram_payment_charge_id: str,
        is_canceled: bool
    ) -> Dict[Any, Any]:
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
        return self._make_request("editUserStarSubscription", method="POST", data=payload)

def create_shipping_query(
    id: str,
    from_user: Dict[str, Any],
    invoice_payload: str,
    shipping_address: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a ShippingQuery object.

    This object contains information about an incoming shipping query.
    It is sent when the user has selected a shipping address and a shipping option is needed.

    :param id: Unique identifier for the query.
    :param from_user: User who sent the query (User object).
    :param invoice_payload: Bot-specified invoice payload (1-128 bytes). Used for internal tracking.
    :param shipping_address: User's specified shipping address (ShippingAddress object).
    :return: A dictionary representing a ShippingQuery object.
    """
    return {
        "id": id,
        "from": from_user,
        "invoice_payload": invoice_payload,
        "shipping_address": shipping_address,
    }

def create_pre_checkout_query(
    id: str,
    from_user: Dict[str, Any],
    currency: str,
    total_amount: int,
    invoice_payload: str,
    shipping_option_id: Optional[str] = None,
    order_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a PreCheckoutQuery object.

    This object contains information about an incoming pre-checkout query.
    It is sent after the user has reviewed the invoice and confirmed the shipping address (if applicable),
    but before the actual payment is processed.

    The bot must respond within 10 seconds using answerPreCheckoutQuery.

    :param id: Unique identifier for the query.
    :param from_user: User who sent the query (User object).
    :param currency: Three-letter ISO 4217 currency code (e.g., 'USD') or 'XTR' for Telegram Stars.
    :param total_amount: Total price in the smallest units of the currency (e.g., 145 for $1.45).
    :param invoice_payload: Bot-specified invoice payload (1-128 bytes). Used for internal tracking.
    :param shipping_option_id: Optional. Identifier of the shipping option chosen by the user.
    :param order_info: Optional. Order information provided by the user (OrderInfo object).
    :return: A dictionary representing a PreCheckoutQuery object.
    """
    query = {
        "id": id,
        "from": from_user,
        "currency": currency,
        "total_amount": total_amount,
        "invoice_payload": invoice_payload,
        "shipping_option_id": shipping_option_id,
        "order_info": order_info,
    }
    return {k: v for k, v in query.items() if v is not None}

def create_paid_media_purchased(
    from_user: Dict[str, Any],
    paid_media_payload: str
) -> Dict[str, Any]:
    """
    Create a PaidMediaPurchased object.

    This object contains information about a successful purchase of paid media.
    It is received as part of an Update when a user buys access to media sent via sendPaidMedia.

    :param from_user: User who purchased the media (User object).
    :param paid_media_payload: Bot-specified paid media payload (0-128 bytes). Used for internal processes.
    :return: A dictionary representing a PaidMediaPurchased object.
    """
    return {
        "from": from_user,
        "paid_media_payload": paid_media_payload,
    }

def create_revenue_withdrawal_state_pending() -> Dict[str, Any]:
    """
    Create a RevenueWithdrawalStatePending object.

    Represents a revenue withdrawal operation that is currently in progress.

    :return: A dictionary representing a RevenueWithdrawalStatePending object.
    """
    return {
        "type": "pending"
    }

def create_revenue_withdrawal_state_succeeded(
    date: int,
    url: str
) -> Dict[str, Any]:
    """
    Create a RevenueWithdrawalStateSucceeded object.

    Represents a revenue withdrawal operation that has successfully completed.

    :param date: Date the withdrawal was completed, in Unix time.
    :param url: An HTTPS URL that can be used to view transaction details.
    :return: A dictionary representing a RevenueWithdrawalStateSucceeded object.
    """
    return {
        "type": "succeeded",
        "date": date,
        "url": url,
    }

def create_revenue_withdrawal_state_failed() -> Dict[str, Any]:
    """
    Create a RevenueWithdrawalStateFailed object.

    Represents a revenue withdrawal operation that has failed and the transaction was refunded.

    :return: A dictionary representing a RevenueWithdrawalStateFailed object.
    """
    return {
        "type": "failed"
    }

def create_affiliate_info(
    commission_per_mille: int,
    amount: int,
    affiliate_user: Optional[Dict[str, Any]] = None,
    affiliate_chat: Optional[Dict[str, Any]] = None,
    nanostar_amount: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create an AffiliateInfo object.

    Contains information about an affiliate that received a commission via a transaction.

    :param commission_per_mille: Number of Telegram Stars received by the affiliate for each 1000 Stars received by the bot.
    :param amount: Integer amount of Telegram Stars received by the affiliate (rounded to 0; can be negative for refunds).
    :param affiliate_user: Optional. The bot or user that received the commission.
    :param affiliate_chat: Optional. The chat that received the commission.
    :param nanostar_amount: Optional. Number of 1/1000000000 shares of Telegram Stars received by the affiliate.
    :return: A dictionary representing an AffiliateInfo object.
    """
    info = {
        "commission_per_mille": commission_per_mille,
        "amount": amount,
        "affiliate_user": affiliate_user,
        "affiliate_chat": affiliate_chat,
        "nanostar_amount": nanostar_amount,
    }
    return {k: v for k, v in info.items() if v is not None}

def create_transaction_partner_user(
    user: Dict[str, Any],
    transaction_type: str,
    affiliate: Optional[Dict[str, Any]] = None,
    invoice_payload: Optional[str] = None,
    subscription_period: Optional[int] = None,
    paid_media: Optional[List[Dict[str, Any]]] = None,
    paid_media_payload: Optional[str] = None,
    gift: Optional[Dict[str, Any]] = None,
    premium_subscription_duration: Optional[int] = None
) -> Dict[str, Any]:
    """
    Create a TransactionPartnerUser object.

    Describes a transaction with a user (e.g., an invoice payment, a gift purchase).

    :param user: Information about the user.
    :param transaction_type: Type of the transaction: 'invoice_payment', 'paid_media_payment', 'gift_purchase', 'premium_purchase', 'business_account_transfer'.
    :param affiliate: Optional. Information about the affiliate that received a commission.
    :param invoice_payload: Optional. Bot-specified invoice payload (for 'invoice_payment').
    :param subscription_period: Optional. Duration of the paid subscription in seconds (for 'invoice_payment').
    :param paid_media: Optional. Information about the paid media bought by the user (for 'paid_media_payment').
    :param paid_media_payload: Optional. Bot-specified paid media payload (for 'paid_media_payment').
    :param gift: Optional. The gift sent to the user by the bot (for 'gift_purchase').
    :param premium_subscription_duration: Optional. Number of months the gifted Telegram Premium subscription is active for (for 'premium_purchase').
    :return: A dictionary representing a TransactionPartnerUser object.
    """
    partner = {
        "type": "user",
        "user": user,
        "transaction_type": transaction_type,
        "affiliate": affiliate,
        "invoice_payload": invoice_payload,
        "subscription_period": subscription_period,
        "paid_media": paid_media,
        "paid_media_payload": paid_media_payload,
        "gift": gift,
        "premium_subscription_duration": premium_subscription_duration,
    }
    return {k: v for k, v in partner.items() if v is not None}

def create_transaction_partner_chat(
    chat: Dict[str, Any],
    gift: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a TransactionPartnerChat object.

    Describes a transaction with a chat (e.g., sending a gift to a channel).

    :param chat: Information about the chat.
    :param gift: Optional. The gift sent to the chat by the bot.
    :return: A dictionary representing a TransactionPartnerChat object.
    """
    partner = {
        "type": "chat",
        "chat": chat,
        "gift": gift,
    }
    return {k: v for k, v in partner.items() if v is not None}

def create_transaction_partner_affiliate_program(
    sponsor_user: Optional[Dict[str, Any]],
    commission_per_mille: int
) -> Dict[str, Any]:
    """
    Create a TransactionPartnerAffiliateProgram object.

    Describes the affiliate program that issued a commission received via a transaction.

    :param sponsor_user: Optional. Information about the bot that sponsored the affiliate program.
    :param commission_per_mille: Number of Telegram Stars received by the bot for each 1000 Stars received by the affiliate sponsor.
    :return: A dictionary representing a TransactionPartnerAffiliateProgram object.
    """
    return {
        "type": "affiliate_program",
        "sponsor_user": sponsor_user,
        "commission_per_mille": commission_per_mille,
    }

def create_transaction_partner_fragment(
    withdrawal_state: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a TransactionPartnerFragment object.

    Describes a withdrawal transaction with Fragment.

    :param withdrawal_state: Optional. State of the outgoing withdrawal transaction.
    :return: A dictionary representing a TransactionPartnerFragment object.
    """
    return {
        "type": "fragment",
        "withdrawal_state": withdrawal_state,
    }

def create_transaction_partner_telegram_ads() -> Dict[str, Any]:
    """
    Create a TransactionPartnerTelegramAds object.

    Describes a withdrawal transaction to the Telegram Ads platform.

    :return: A dictionary representing a TransactionPartnerTelegramAds object.
    """
    return {
        "type": "telegram_ads"
    }

def create_transaction_partner_telegram_api(
    request_count: int
) -> Dict[str, Any]:
    """
    Create a TransactionPartnerTelegramApi object.

    Describes a transaction with payment for paid broadcasting.

    :param request_count: The number of successful requests that exceeded regular limits and were billed.
    :return: A dictionary representing a TransactionPartnerTelegramApi object.
    """
    return {
        "type": "telegram_api",
        "request_count": request_count,
    }

def create_transaction_partner_other() -> Dict[str, Any]:
    """
    Create a TransactionPartnerOther object.

    Describes a transaction with an unknown source or recipient.

    :return: A dictionary representing a TransactionPartnerOther object.
    """
    return {
        "type": "other"
    }

def create_star_transaction(
    id: str,
    amount: int,
    date: int,
    nanostar_amount: Optional[int] = None,
    source: Optional[Dict[str, Any]] = None,
    receiver: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a StarTransaction object.

    Describes a Telegram Star transaction (e.g., a payment from a user, a withdrawal).

    :param id: Unique identifier of the transaction.
    :param amount: Integer amount of Telegram Stars transferred.
    :param date: Date the transaction was created, in Unix time.
    :param nanostar_amount: Optional. Number of 1/1000000000 shares of Telegram Stars transferred.
    :param source: Optional. Source of the transaction (for incoming transactions).
    :param receiver: Optional. Receiver of the transaction (for outgoing transactions).
    :return: A dictionary representing a StarTransaction object.
    """
    transaction = {
        "id": id,
        "amount": amount,
        "date": date,
        "nanostar_amount": nanostar_amount,
        "source": source,
        "receiver": receiver,
    }
    return {k: v for k, v in transaction.items() if v is not None}

def create_star_transactions(
    transactions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create a StarTransactions object.

    Contains a list of Telegram Star transactions.

    :param transactions: The list of StarTransaction objects.
    :return: A dictionary representing a StarTransactions object.
    """
    return {
        "transactions": transactions
    }

def create_passport_data(
    data: List[Dict[str, Any]],
    credentials: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Create a PassportData object.

    Describes Telegram Passport data shared with the bot by the user.

    :param data: Array of EncryptedPassportElement objects.
    :param credentials: EncryptedCredentials object required to decrypt the data.
    :return: A dictionary representing a PassportData object.
    """
    return {
        "data": data,
        "credentials": credentials,
    }

def create_passport_file(
    file_id: str,
    file_unique_id: str,
    file_size: int,
    file_date: int
) -> Dict[str, Any]:
    """
    Create a PassportFile object.

    Represents a file uploaded to Telegram Passport.

    :param file_id: Identifier for the file.
    :param file_unique_id: Unique identifier for the file.
    :param file_size: File size in bytes.
    :param file_date: Unix time when the file was uploaded.
    :return: A dictionary representing a PassportFile object.
    """
    return {
        "file_id": file_id,
        "file_unique_id": file_unique_id,
        "file_size": file_size,
        "file_date": file_date,
    }

def create_encrypted_passport_element(
    type: str,
    data: Optional[str] = None,
    phone_number: Optional[str] = None,
    email: Optional[str] = None,
    files: Optional[List[Dict[str, Any]]] = None,
    front_side: Optional[Dict[str, Any]] = None,
    reverse_side: Optional[Dict[str, Any]] = None,
    selfie: Optional[Dict[str, Any]] = None,
    translation: Optional[List[Dict[str, Any]]] = None,
    hash: str = None
) -> Dict[str, Any]:
    """
    Create an EncryptedPassportElement object.

    Describes a document or other element shared with the bot via Telegram Passport.

    :param type: Element type: 'personal_details', 'passport', 'driver_license', etc.
    :param data: Optional. Base64-encoded encrypted data (for certain types).
    :param phone_number: Optional. Verified phone number (for 'phone_number' type).
    :param email: Optional. Verified email address (for 'email' type).
    :param files: Optional. Array of encrypted files (for certain types).
    :param front_side: Optional. Encrypted file with the front side of a document.
    :param reverse_side: Optional. Encrypted file with the reverse side of a document.
    :param selfie: Optional. Encrypted file with a user's selfie holding a document.
    :param translation: Optional. Array of encrypted files with translated versions of documents.
    :param hash: Base64-encoded element hash for error reporting.
    :return: A dictionary representing an EncryptedPassportElement object.
    """
    element = {
        "type": type,
        "data": data,
        "phone_number": phone_number,
        "email": email,
        "files": files,
        "front_side": front_side,
        "reverse_side": reverse_side,
        "selfie": selfie,
        "translation": translation,
        "hash": hash,
    }
    return {k: v for k, v in element.items() if v is not None}

def create_encrypted_credentials(
    data: str,
    hash: str,
    secret: str
) -> Dict[str, Any]:
    """
    Create an EncryptedCredentials object.

    Describes data required for decrypting and authenticating EncryptedPassportElement.

    :param data: Base64-encoded encrypted JSON-serialized data.
    :param hash: Base64-encoded data hash for authentication.
    :param secret: Base64-encoded secret, encrypted with the bot's public key.
    :return: A dictionary representing an EncryptedCredentials object.
    """
    return {
        "data": data,
        "hash": hash,
        "secret": secret,
    }

def set_passport_data_errors(
    self,
    user_id: int,
    errors: List[Dict[str, Any]]
) -> Dict[Any, Any]:
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
    return self._make_request("setPassportDataErrors", method="POST", data=payload)

def create_passport_element_error_data_field(
    type: str,
    field_name: str,
    data_hash: str,
    message: str
) -> Dict[str, Any]:
    """
    Create a PassportElementErrorDataField object.

    Represents an issue in a data field provided by the user (e.g., invalid name or date).
    The error is resolved when the field's value changes.

    :param type: The section of Telegram Passport with the error: 'personal_details', 'passport', etc.
    :param field_name: Name of the data field which has the error.
    :param data_hash: Base64-encoded data hash.
    :param message: Error message shown to the user.
    :return: A dictionary representing a PassportElementErrorDataField object.
    """
    return {
        "source": "data",
        "type": type,
        "field_name": field_name,
        "data_hash": data_hash,
        "message": message,
    }

def create_passport_element_error_front_side(
    type: str,
    file_hash: str,
    message: str
) -> Dict[str, Any]:
    """
    Create a PassportElementErrorFrontSide object.

    Represents an issue with the front side of a document (e.g., blurry photo).
    The error is resolved when the file changes.

    :param type: The section of Telegram Passport with the issue: 'passport', 'driver_license', etc.
    :param file_hash: Base64-encoded hash of the file.
    :param message: Error message shown to the user.
    :return: A dictionary representing a PassportElementErrorFrontSide object.
    """
    return {
        "source": "front_side",
        "type": type,
        "file_hash": file_hash,
        "message": message,
    }

def send_game(
    self,
    chat_id: int,
    game_short_name: str,
    business_connection_id: Optional[str] = None,
    message_thread_id: Optional[int] = None,
    disable_notification: Optional[bool] = None,
    protect_content: Optional[bool] = None,
    allow_paid_broadcast: Optional[bool] = None,
    message_effect_id: Optional[str] = None,
    reply_parameters: Optional[ReplyParameters] = None,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> Dict[Any, Any]:
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

    filtered_payload = {k: v for k, v in payload.items() if v is not None}
    return self._make_request("sendGame", method="POST", data=filtered_payload)

def create_game(
    title: str,
    description: str,
    photo: List[Dict[str, Any]],
    text: Optional[str] = None,
    text_entities: Optional[List[MessageEntity]] = None,
    animation: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a Game object.

    Represents a game configured via @BotFather.

    :param title: Title of the game.
    :param description: Description of the game.
    :param photo: Array of PhotoSize objects representing the photo that will be displayed in the game message.
    :param text: Optional. Brief description of the game or high scores. Can be up to 4096 characters.
                 This text can be automatically updated by the bot using setGameScore or manually edited.
    :param text_entities: Optional. List of special entities (like usernames, URLs, commands) that appear in the text.
    :param animation: Optional. Animation (GIF or H.264/MPEG-4 AVC video without sound) to be displayed in the game message.
                      Must be uploaded via @BotFather.
    :return: A dictionary representing a Game object.
    """
    game = {
        "title": title,
        "description": description,
        "photo": photo,
        "text": text,
        "text_entities": text_entities,
        "animation": animation,
    }
    return {k: v for k, v in game.items() if v is not None}

def create_callback_game() -> Dict[str, Any]:
    """
    Create a CallbackGame object.

    A placeholder object that currently holds no information.
    Used as a type of InlineKeyboardButton to launch a game.

    Use @BotFather to set up your game.

    :return: An empty dictionary representing a CallbackGame object.
    """
    return {}

def set_game_score(
    self,
    user_id: int,
    score: int,
    force: Optional[bool] = None,
    disable_edit_message: Optional[bool] = None,
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None
) -> Dict[Any, Any]:
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
        raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

    payload = {
        "user_id": user_id,
        "score": score,
        "force": force,
        "disable_edit_message": disable_edit_message,
        "chat_id": chat_id,
        "message_id": message_id,
        "inline_message_id": inline_message_id,
    }

    filtered_payload = {k: v for k, v in payload.items() if v is not None}
    return self._make_request("setGameScore", method="POST", data=filtered_payload)

def get_game_high_scores(
    self,
    user_id: int,
    chat_id: Optional[int] = None,
    message_id: Optional[int] = None,
    inline_message_id: Optional[str] = None
) -> Dict[Any, Any]:
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
        raise ValueError("Either (chat_id and message_id) or inline_message_id must be provided.")

    payload = {
        "user_id": user_id,
        "chat_id": chat_id,
        "message_id": message_id,
        "inline_message_id": inline_message_id,
    }

    filtered_params = {k: v for k, v in payload.items() if v is not None}
    return self._make_request("getGameHighScores", method="GET", params=filtered_params)

def create_game_high_score(
    position: int,
    user: Dict[str, Any],
    score: int
) -> Dict[str, Any]:
    """
    Create a GameHighScore object.

    Represents one row in the high scores table for a game.

    :param position: Position in the high score table.
    :param user: User object representing the player.
    :param score: The player's score.
    :return: A dictionary representing a GameHighScore object.
    """
    return {
        "position": position,
        "user": user,
        "score": score,
    }
