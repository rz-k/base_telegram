import json
import threading
from typing import Dict, List, Optional, Union

import requests

from utils.load_env import env


class Telegram:

    webhook_url: str = 'https://api.telegram.org/bot{}/{}'
    webhook_url_file: str = 'https://api.telegram.org/file/bot{}/{}'
    headers : dict = {"Cache-Control": "no-cache"}
    proxy: dict = {}

    def bot(self, telegram_method, data, method='GET', input_file=None, params: dict = None):
        if params is None:
            params = {}
        if env.get("PROXY_SOCKS", None):
            self.proxy = {
                "http": f'socks5h://{env.get("PROXY_SOCKS")}',
                "https": f'socks5h://{env.get("PROXY_SOCKS")}'
            }
        url = self.webhook_url.format(env.get("TOKEN"), telegram_method)
        try:
            if method == 'GET':
                request = requests.get(url, params=data, proxies=self.proxy, headers=self.headers, timeout=30)
                return json.loads(request.text)
            else:
                request = requests.post(
                    url=url, data=data, params=params,
                    files=input_file, timeout=100,
                    proxies=self.proxy, headers=self.headers
                )
                if request.text:
                    return json.loads(request.text)
                return {}

        except Exception as error:
            print("Error in Telegram Class: ", error)

    def send_message(self: "Telegram",
        chat_id: Union[int, str],
        text: str,
        parse_mode: Optional["ParseMode"] = "html", # type: ignore  # noqa: F821
        entities: List["MessageEntity"] = None, # type: ignore  # noqa: F821
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        schedule_date: "datetime" = None,  # noqa: F821 # type: ignore
        protect_content: bool = None,
        reply_markup: Union[
            "InlineKeyboardMarkup",  # noqa: F821 # type: ignore
            "ReplyKeyboardMarkup",  # noqa: F821 # type: ignore
            "ReplyKeyboardRemove",  # noqa: F821 # type: ignore
            "ForceReply"  # noqa: F821 # type: ignore
        ] = None
    ):
        """
        This Method for sending a message in telegram.

          Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            text (``str``):
                Text of the message to be sent.

            parse_mode (`str`, *optional*):
               By default, texts are parsed as HTML styles.

            entities (`list`, *optional*):
                List of special entities that appear in message text.

            disable_web_page_preview (`bool`, *optional*):
                Disables link previews for links in this message.

            disable_notification (`bool`, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (`int`, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (`datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content(`bool`, *optional*):
                Protects the contents of the sent message from forwarding and saving.

            reply_markup (`list`, *optional*):
                An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        """
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "entities": entities,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "reply_to_message_id": reply_to_message_id,
            "schedule_date": schedule_date,
            "protect_content": protect_content,
            "reply_markup": reply_markup
        }
        result = self.bot(telegram_method="sendMessage", data=data)
        return result

    def edit_message_text(self, chat_id, message_id, text, **kwargs):
        """
            This Method for sending message in telegram.
            **kwargs :
                parse_mode-> Str ,
                entities-> List ,
                disable_web_page_preview -> Bool ,
                disable_notification = > Bool ,
                protect_content -> Bool ,
                reply_to_message_id - > Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup - > List ,
        """
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": "html",
            "disable_web_page_preview": "true"
        }
        data.update(**kwargs)
        result = self.bot(telegram_method="editMessageText", data=data)
        return result

    def edit_message_media(self, chat_id, message_id, **kwargs):
        """
            This Method for edit media message in telegram.
            **kwargs :
                parse_mode-> Str
                entities-> List
                disable_web_page_preview -> Bool
                disable_notification = > Bool
                protect_content -> Bool
                reply_to_message_id - > Int
                allow_sending_without_reply -> Bool
                reply_markup - > List
        """
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        data.update(**kwargs)
        result = self.bot(telegram_method="editMessageMedia", data=data, method="POST")
        return result

    def edit_message_caption(self, chat_id, message_id, **kwargs):
        """
            This Method for edit caption message in telegram.
            **kwargs :
                parse_mode-> Str
                entities-> List
                disable_web_page_preview -> Bool
                disable_notification = > Bool
                protect_content -> Bool
                reply_to_message_id - > Int
                allow_sending_without_reply -> Bool
                reply_markup - > List
        """
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        data.update(**kwargs)
        result = self.bot(telegram_method="editMessageCaption", data=data, method="POST")
        return result

    def forward_message(self, chat_id, from_chat_id, message_id: int, **kwargs):
        """
        This Method for forward message in telegram.
            **kwargs :
                disable_notification - > Bool ,
                protect_content - > Bool
        """
        data = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }

        data.update(**kwargs)
        result = self.bot(telegram_method="forwardMessage", data=data)
        return result

    def copy_message(self, chat_id, from_chat_id, message_id: int, **kwargs):
        """
        This Method for Copy message in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
        """
        data = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id
        }

        data.update(**kwargs)
        result = self.bot(telegram_method="copyMessage", data=data)
        return result

    def send_photo(self, chat_id, photo, **kwargs):
        """
        This Method for send_Photo in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
        """
        method = 'GET'
        file_photo=None
        data = {
            "chat_id": chat_id,
            "parse_mode": "html"
        }
        if isinstance(photo, bytes):
            method = 'POST'
            file_photo = {
                "photo": photo
            }
        else:
            data.update({
                "photo": photo
            })
        params = {}
        data.update(**kwargs)
        result = self.bot("sendPhoto", data=data, method=method, params=params, input_file=file_photo)
        return result

    def send_sticker(self, chat_id, sticker, **kwargs):
        """
        This Method for sendSticker in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
        """
        method = 'GET'
        data = {
            "chat_id": chat_id,
        }
        file_sticker = None
        if isinstance(sticker, bytes):
            method = 'POST'
            file_sticker = {
                "sticker": sticker
            }
        else:
            data.update({"sticker": sticker})

        params = {}
        data.update(**kwargs)
        result = self.bot("sendSticker", data=data, method=method, params=params, input_file=file_sticker)
        return result

    def is_join_channel(self, chat_id, user_id, **kwargs):
        if chat_id.isnumeric():
            chat_id = chat_id if '@' in chat_id else '@'+str(chat_id)
        data = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        data.update(**kwargs)
        result = self.bot(telegram_method="getChatMember", data=data)
        if result['ok']:
            return result['result']['status'] != 'left'
        else:
            return False

    def get_chat_member(self, chat_id, user_id, **kwargs):
        data = {
            "chat_id": chat_id,
            "user_id": user_id
        }
        data.update(**kwargs)
        result = self.bot(telegram_method="getChatMember", data=data)
        if result['ok']:
            return result
        return False

    def send_audio(self, chat_id, audio, **kwargs):
        """
        This Method for send_Audio in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
                duration -> Int ,
                performer -> Str ,
                title  -> Str ,
                thumb  -> Str & File ,
        """
        method = 'GET'
        if isinstance(audio, bytes):
            method = 'POST'

        data = {
            "chat_id": str(chat_id),
        }
        file_audio = {
            "audio": audio
        }

        data.update(**kwargs)
        result = self.bot("sendAudio", data=data, method=method, input_file=file_audio)
        return result

    def send_document(self, chat_id, document, **kwargs):
        """
        This Method for send_Document in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_content_type_detection -> Bool ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
        """
        method = 'POST'
        data = {
            "chat_id": str(chat_id)
        }
        file_doc = {
            "document": document
        }

        data.update(**kwargs)
        result = self.bot("sendDocument", data=data, method=method, input_file=file_doc)
        return result

    def send_video(self, chat_id, video, **kwargs):
        """
        This Method for send_Video in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_content_type_detection -> Bool ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
                duration -> Int ,
                width -> Int ,
                height -> Int ,
                thumb  -> Str & File ,
                supports_streaming  -> Bool ,

        """
        method = 'GET'
        if isinstance(video, bytes):
            method = 'POST'

        data = {
            "chat_id": str(chat_id),
            "video": video
        }

        data.update(**kwargs)
        result = self.bot("sendVideo", data=data, method=method)
        return result

    def send_animation(self, chat_id, animation, **kwargs):
        """
        This Method for send_Animation in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_content_type_detection -> Bool ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
                duration -> Int ,
                width -> Int ,
                height -> Int ,
                thumb  -> Str & File ,
        """
        method = 'GET'
        if isinstance(animation, bytes):
            method = 'POST'

        data = {
            "chat_id": str(chat_id)
        }
        file_animation = {
            "animation": animation
        }

        data.update(**kwargs)
        result = self.bot("sendAnimation", data=data, method=method, input_file=file_animation)
        return result

    def send_voice(self, chat_id, voice, **kwargs):
        """
        This Method for send_Voice in telegram.
            **kwargs :
                caption -> Str ,
                parse_mode -> Str ,
                caption_entities -> List ,
                disable_content_type_detection -> Bool ,
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
                duration -> Int ,
                thumb  -> Str & File ,

        """
        method = 'GET'
        if isinstance(voice, bytes):
            method = 'POST'

        data = {
            "chat_id": str(chat_id)
        }
        file_voice = {
            "voice": voice
        }

        data.update(**kwargs)
        result = self.bot("sendVoice", data=data, method=method, input_file=file_voice)
        return result

    def send_video_note(self, chat_id, video_note, **kwargs):
        """
        This Method for send_VideoNote in telegram.
            **kwargs :
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
                reply_markup -> List ,
                duration -> Int ,
                thumb  -> Str & File ,
                length -> Int
        """
        method = 'GET'
        if isinstance(video_note, bytes):
            method = 'POST'

        data = {
            "chat_id": str(chat_id)
        }
        file_video_note = {
            "video_note": video_note
        }

        data.update(**kwargs)
        result = self.bot("sendVideoNote", data=data, method=method, input_file=file_video_note)
        return result

    def send_media_group(self, chat_id, media: list, **kwargs):
        """
        This Method for send_MediaGroup in telegram.
            **kwargs :
                disable_notification -> Bool ,
                protect_content -> Bool ,
                reply_to_message_id -> Int ,
                allow_sending_without_reply -> Bool ,
        """
        method = 'GET'
        if isinstance(media[0], bytes):
            method = 'POST'

        data = {
            "chat_id": str(chat_id),
        }
        file_media = {
            "media": media
        }

        data.update(**kwargs)
        result = self.bot("sendMediaGroup", data=data, method=method, input_file=file_media)
        return result

    def send_action(self, chat_id, action="typing", **kwargs) -> Dict:
        """
        This Method for sendChatAction in telegram.
            **kwargs :
                disable_notification -> Bool ,
        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id),
            "action":action
        }

        result = self.bot("sendChatAction", data=data, method=method)
        return result

    def send_answer_callback_query(self, callback_query_id, text: str, **kwargs):
        """
        This Method for send_AnswerCallbackQuery in telegram.
            **kwargs :
                show_alert -> Bool ,
                url -> text ,
                cache_time -> Int ,
        """
        method = 'GET'

        data = {
            "callback_query_id": str(callback_query_id),
            "text": text
        }
        data.update(**kwargs)
        result = self.bot("answerCallbackQuery", data=data, method=method)
        return result

    def delete_message(self, chat_id, message_id: int):
        """
        This Method for delete_Message in telegram.

        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id),
            "message_id": message_id
        }

        result = self.bot("deleteMessage", data=data, method=method)
        return result

    def get_count_member_chat(self, chat_id):
        """
        This Method for get_count_chat in telegram.

        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id)
        }
        result = self.bot("getChatMembersCount", data=data, method=method)
        return result

    def left_chat(self, chat_id):
        """
        This Method for left chat in telegram.

        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id)
        }
        result = self.bot("leaveChat", data=data, method=method)
        return result

    def get_file(self, file_id):
        """
        This Method for get file in telegram.

        """
        method = 'GET'
        data = {
            "file_id": str(file_id)
        }
        result = self.bot("getFile", data=data, method=method)
        return result

    def get_link_invite(self, chat_id):
        """
        This Method for get_link in telegram.

        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id)
        }

        result = self.bot("exportChatInviteLink", data=data, method=method)
        return result

    def promote_chat_member(self, chat_id, user_id, **kwargs):
        """
        This Method for promote_hat_member in telegram.
        can_change_info=0
        can_post_messages=0
        can_edit_messages=0
        can_delete_messages=1
        can_invite_users=1
        can_restrict_members=1
        can_pin_messages=1
        can_promote_members=0
        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id),
            "user_id": str(user_id),
        }
        data.update(kwargs)
        result = self.bot("promoteChatMember", data=data, method=method)
        return result

    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title , **kwargs):
        """
        This Method for setChatAdministratorCustomTitle in telegram.
        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id),
            "user_id": str(user_id),
            "custom_title": custom_title
        }
        data.update(kwargs)
        result = self.bot("setChatAdministratorCustomTitle", data=data, method=method)
        return result

    def user_joined(self, chat_id, user_id):
        """
            Use this method to get information about a member of a chat.
            Returns a ChatMember object on success.
        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id),
            "user_id": str(user_id)
        }

        result = self.bot("getChatMember", data=data, method=method)
        return result

    def download_file(self, path):
        """
            Use this method to get information about a member of a chat.
            Returns a ChatMember object on success.
        """
        if env.PROXY_SOCKS:
            self.proxy = {
                "http": f'socks5h://{env.PROXY_SOCKS}',
                "https": f'socks5h://{env.PROXY_SOCKS}'
            }
        url = self.webhook_url_file.format(env.TOKEN, path)
        try:
            request = requests.get(url, proxies=self.proxy, headers=self.headers, timeout=30)
            return request.content
        except:  # noqa: E722, S110
            pass


    def send_memory_file_to_user(self,chat_id ,path, method="sticker", msg_id=1):
        import random
        from io import BytesIO
        if env.PROXY_SOCKS:
            self.proxy = {
                "http": f'socks5h://{env.PROXY_SOCKS}',
                "https": f'socks5h://{env.PROXY_SOCKS}'
            }
        url = self.webhook_url_file.format(env.TOKEN, path)
        request = requests.get(url, proxies=self.proxy, headers=self.headers, timeout=30)
        file_content = BytesIO(request.content)
        file_content.name=random.randint(1, 90909090).__str__()+".webp"  # noqa: S311
        file_content.seek(0)

        if method == "sticker":
            self.send_sticker(chat_id, file_content.read(), reply_to_message_id=msg_id)
        elif method == 'photo':
            self.send_photo(chat_id, file_content.read(), reply_to_message_id=msg_id)
        file_content.close()

    def kick_chat_member(self, chat_id, user_id):
        """
            Use this method to kickChatMember member of a chat.
            Returns a result success.
        """
        method = 'GET'
        data = {
            "chat_id": str(chat_id),
            "user_id": str(user_id)
        }

        result = self.bot("kickChatMember", data=data, method=method)
        return result


    def restrict_chat_member(self, chat_id, user_id, permissions: dict, **kwargs):
        """
            until_date:	Integer (mute time)
            Use this method to restrictChatMember member of a chat.
            Returns a result success.
        """
        method = 'GET'
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": json.dumps(permissions)
        }
        data.update(kwargs)
        result = self.bot("restrictChatMember", data=data, method=method)
        return result

    def pin_chat_message(self, chat_id, message_id, **kwargs):
        """
            disable_notification:	Bool (notif to all)
            Use this method to pinChatMessage member of a chat.
            Returns a result success.
        """
        method = 'GET'
        data = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        data.update(kwargs)
        result = self.bot("pinChatMessage", data=data, method=method)
        return result

    def unpin_chat_message(self, chat_id, message_id):
        """
            Use this method to unpinChatMessage member of a chat.
            Returns a result success.
        """
        method = 'GET'
        data = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        result = self.bot("unpinChatMessage", data=data, method=method)
        return result

    def unpins_chat_message(self, chat_id):
        """
            Use this method to unpinAllChatMessages member of a chat.
            Returns a result success.
        """
        method = 'GET'
        data = {
            "chat_id": chat_id
        }
        result = self.bot("unpinAllChatMessages", data=data, method=method)
        return result

    def delete_messages(self, chat_id, message_id, count=100):
        message_id = message_id - 1
        for _ in range(count):
            message_id-=1
            t = threading.Thread(
                target=self.delete_message,
                args=[
                    chat_id,
                    message_id
                ]
            )
            t.start()
    def edit_message_replay_markup(self, chat_id, message_id, **kwargs):
        """
            This Method for edit media message in telegram.
            **kwargs :
                reply_markup - > List
        """
        data = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        data.update(**kwargs)
        result = self.bot(telegram_method="editMessageReplyMarkup", data=data, method="POST")
        return result
