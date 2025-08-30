from typing import List, TypedDict, Union

# -------------------------------
# Basic Types
# -------------------------------

class User(TypedDict, total=False):
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str
    is_premium: bool
    added_to_attachment_menu: bool
    can_join_groups: bool
    can_read_all_group_messages: bool
    supports_inline_queries: bool


class WebAppInfo(TypedDict, total=False):
    url: str


class LoginUrl(TypedDict, total=False):
    url: str
    forward_text: str
    bot_username: str
    request_write_access: bool


class SwitchInlineQueryChosenChat(TypedDict, total=False):
    query: str
    allow_user_chats: bool
    allow_bot_chats: bool
    allow_group_chats: bool
    allow_channel_chats: bool


class CopyTextButton(TypedDict, total=False):
    text: str


class CallbackGame(TypedDict, total=False):
    pass  # No fields defined in API


# -------------------------------
# MessageEntity
# -------------------------------

class MessageEntity(TypedDict, total=False):
    """
    Represents one special entity in a text message (e.g., @mentions, #hashtags, bold, links).
    https://core.telegram.org/bots/api#messageentity
    """
    type: str  # Required
    offset: int  # Required
    length: int  # Required
    url: str
    user: User
    language: str
    custom_emoji_id: str


# -------------------------------
# LinkPreviewOptions
# -------------------------------

class LinkPreviewOptions(TypedDict, total=False):
    """
    Options for link preview generation in a message.
    """
    is_disabled: bool
    url: str
    prefer_small_media: bool
    prefer_large_media: bool
    show_above_text: bool


# -------------------------------
# SuggestedPostParameters
# -------------------------------

class SuggestedPostPrice(TypedDict, total=False):
    amount: int  # Required (assumed from context)
    currency: str  # Required (assumed from context)


class SuggestedPostParameters(TypedDict, total=False):
    """
    Parameters of a suggested post (e.g., for monetized messages).
    """
    price: SuggestedPostPrice
    send_date: int  # Unix timestamp


# -------------------------------
# ReplyParameters
# -------------------------------

class ReplyParameters(TypedDict, total=False):
    """
    Describes the message to reply to, with optional quoting.
    """
    message_id: int  # Required
    chat_id: Union[int, str]
    allow_sending_without_reply: bool
    quote: str
    quote_parse_mode: str
    quote_entities: List[MessageEntity]
    quote_position: int
    checklist_task_id: int


# -------------------------------
# InlineKeyboardButton & InlineKeyboardMarkup
# -------------------------------

class InlineKeyboardButton(TypedDict, total=False):
    """
    One button of an inline keyboard.
    Exactly one of the optional fields should be set.
    """
    text: str  # Required
    url: str
    callback_data: str
    web_app: WebAppInfo
    login_url: LoginUrl
    switch_inline_query: str
    switch_inline_query_current_chat: str
    switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat
    copy_text: CopyTextButton
    callback_game: CallbackGame
    pay: bool


class InlineKeyboardMarkup(TypedDict, total=False):
    """
    Inline keyboard attached to a message.
    """
    inline_keyboard: List[List[InlineKeyboardButton]]  # Required


# -------------------------------
# ReplyKeyboardButton & ReplyKeyboardMarkup
# -------------------------------

class KeyboardButtonPollType(TypedDict, total=False):
    type: str


class KeyboardButtonRequestChat(TypedDict, total=False):
    request_id: int
    chat_type: str
    name: str
    username: str
    bot: bool


class KeyboardButtonRequestUser(TypedDict, total=False):
    request_id: int
    user_is_bot: bool
    user_is_premium: bool
    name: str
    username: str


class KeyboardButton(TypedDict, total=False):
    text: str  # Required
    request_contact: bool
    request_location: bool
    request_poll: KeyboardButtonPollType
    request_chat: KeyboardButtonRequestChat
    request_user: KeyboardButtonRequestUser
    web_app: WebAppInfo


class ReplyKeyboardMarkup(TypedDict, total=False):
    """
    Custom reply keyboard.
    """
    keyboard: List[List[KeyboardButton]]  # Required
    is_persistent: bool
    resize_keyboard: bool
    one_time_keyboard: bool
    input_field_placeholder: str
    selective: bool


# -------------------------------
# ReplyKeyboardRemove & ForceReply
# -------------------------------

class ReplyKeyboardRemove(TypedDict, total=False):
    """
    Instruction to remove the current reply keyboard.
    """
    remove_keyboard: bool  # Must be True
    selective: bool


class ForceReply(TypedDict, total=False):
    """
    Instruction to force a reply from the user.
    """
    force_reply: bool  # Must be True
    input_field_placeholder: str
    selective: bool


# -------------------------------
# Union Type for Reply Markup
# -------------------------------

ReplyMarkup = Union[
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply
]
