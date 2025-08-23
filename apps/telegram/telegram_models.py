from __future__ import annotations

from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator


class User(BaseModel):
    id: int = Field(..., alias="id")
    is_bot: bool = Field(..., alias="is_bot")
    first_name: str = Field(..., alias="first_name")
    last_name: Optional[str] = Field(None, alias="last_name")
    username: Optional[str] = Field(None, alias="username")
    language_code: Optional[str] = Field(None, alias="language_code")
    is_premium: Optional[bool] = Field(None, alias="is_premium")
    added_to_attachment_menu: Optional[bool] = Field(None, alias="added_to_attachment_menu")
    can_join_groups: Optional[bool] = Field(None, alias="can_join_groups")
    can_read_all_group_messages: Optional[bool] = Field(None, alias="can_read_all_group_messages")
    supports_inline_queries: Optional[bool] = Field(None, alias="supports_inline_queries")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ChatPhoto(BaseModel):
    small_file_id: str = Field(..., alias="small_file_id")
    small_file_unique_id: str = Field(..., alias="small_file_unique_id")
    big_file_id: str = Field(..., alias="big_file_id")
    big_file_unique_id: str = Field(..., alias="big_file_unique_id")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ChatPermissions(BaseModel):
    can_send_messages: Optional[bool] = Field(None, alias="can_send_messages")
    can_send_media_messages: Optional[bool] = Field(None, alias="can_send_media_messages")
    can_send_polls: Optional[bool] = Field(None, alias="can_send_polls")
    can_send_other_messages: Optional[bool] = Field(None, alias="can_send_other_messages")
    can_add_web_page_previews: Optional[bool] = Field(None, alias="can_add_web_page_previews")
    can_change_info: Optional[bool] = Field(None, alias="can_change_info")
    can_invite_users: Optional[bool] = Field(None, alias="can_invite_users")
    can_pin_messages: Optional[bool] = Field(None, alias="can_pin_messages")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ChatLocation(BaseModel):
    location: Location = Field(..., alias="location")
    address: str = Field(..., alias="address")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Chat(BaseModel):
    id: int = Field(..., alias="id")
    type: str = Field(..., alias="type")
    title: Optional[str] = Field(None, alias="title")
    username: Optional[str] = Field(None, alias="username")
    first_name: Optional[str] = Field(None, alias="first_name")
    last_name: Optional[str] = Field(None, alias="last_name")
    is_forum: Optional[bool] = Field(None, alias="is_forum")
    photo: Optional[ChatPhoto] = Field(None, alias="photo")
    active_usernames: Optional[List[str]] = Field(None, alias="active_usernames")
    emoji_status_custom_emoji_id: Optional[str] = Field(None, alias="emoji_status_custom_emoji_id")
    bio: Optional[str] = Field(None, alias="bio")
    has_private_forwards: Optional[bool] = Field(None, alias="has_private_forwards")
    has_restricted_voice_and_video_messages: Optional[bool] = Field(None, alias="has_restricted_voice_and_video_messages")
    join_to_send_messages: Optional[bool] = Field(None, alias="join_to_send_messages")
    join_by_request: Optional[bool] = Field(None, alias="join_by_request")
    description: Optional[str] = Field(None, alias="description")
    invite_link: Optional[str] = Field(None, alias="invite_link")
    pinned_message: Optional[Message] = Field(None, alias="pinned_message")
    permissions: Optional[ChatPermissions] = Field(None, alias="permissions")
    slow_mode_delay: Optional[int] = Field(None, alias="slow_mode_delay")
    message_auto_delete_time: Optional[int] = Field(None, alias="message_auto_delete_time")
    has_protected_content: Optional[bool] = Field(None, alias="has_protected_content")
    sticker_set_name: Optional[str] = Field(None, alias="sticker_set_name")
    can_set_sticker_set: Optional[bool] = Field(None, alias="can_set_sticker_set")
    linked_chat_id: Optional[int] = Field(None, alias="linked_chat_id")
    location: Optional[ChatLocation] = Field(None, alias="location")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class MessageEntity(BaseModel):
    type: str = Field(..., alias="type")
    offset: int = Field(..., alias="offset")
    length: int = Field(..., alias="length")
    url: Optional[str] = Field(None, alias="url")
    user: Optional[User] = Field(None, alias="user")
    language: Optional[str] = Field(None, alias="language")
    custom_emoji_id: Optional[str] = Field(None, alias="custom_emoji_id")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PhotoSize(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    width: int = Field(..., alias="width")
    height: int = Field(..., alias="height")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class MaskPosition(BaseModel):
    point: str = Field(..., alias="point")
    x_shift: float = Field(..., alias="x_shift")
    y_shift: float = Field(..., alias="y_shift")
    scale: float = Field(..., alias="scale")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Animation(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    width: int = Field(..., alias="width")
    height: int = Field(..., alias="height")
    duration: int = Field(..., alias="duration")
    thumb: Optional[PhotoSize] = Field(None, alias="thumb")
    file_name: Optional[str] = Field(None, alias="file_name")
    mime_type: Optional[str] = Field(None, alias="mime_type")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Audio(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    duration: int = Field(..., alias="duration")
    performer: Optional[str] = Field(None, alias="performer")
    title: Optional[str] = Field(None, alias="title")
    file_name: Optional[str] = Field(None, alias="file_name")
    mime_type: Optional[str] = Field(None, alias="mime_type")
    file_size: Optional[int] = Field(None, alias="file_size")
    thumb: Optional[PhotoSize] = Field(None, alias="thumb")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Document(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    thumb: Optional[PhotoSize] = Field(None, alias="thumb")
    file_name: Optional[str] = Field(None, alias="file_name")
    mime_type: Optional[str] = Field(None, alias="mime_type")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Sticker(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    type: str = Field(..., alias="type")
    width: int = Field(..., alias="width")
    height: int = Field(..., alias="height")
    is_animated: bool = Field(..., alias="is_animated")
    is_video: bool = Field(..., alias="is_video")
    thumb: Optional[PhotoSize] = Field(None, alias="thumb")
    emoji: Optional[str] = Field(None, alias="emoji")
    set_name: Optional[str] = Field(None, alias="set_name")
    mask_position: Optional[MaskPosition] = Field(None, alias="mask_position")
    custom_emoji_id: Optional[str] = Field(None, alias="custom_emoji_id")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Video(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    width: int = Field(..., alias="width")
    height: int = Field(..., alias="height")
    duration: int = Field(..., alias="duration")
    thumb: Optional[PhotoSize] = Field(None, alias="thumb")
    file_name: Optional[str] = Field(None, alias="file_name")
    mime_type: Optional[str] = Field(None, alias="mime_type")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Voice(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    duration: int = Field(..., alias="duration")
    mime_type: Optional[str] = Field(None, alias="mime_type")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class VideoNote(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    length: int = Field(..., alias="length")
    duration: int = Field(..., alias="duration")
    thumb: Optional[PhotoSize] = Field(None, alias="thumb")
    file_size: Optional[int] = Field(None, alias="file_size")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Contact(BaseModel):
    phone_number: str = Field(..., alias="phone_number")
    first_name: str = Field(..., alias="first_name")
    last_name: Optional[str] = Field(None, alias="last_name")
    user_id: Optional[int] = Field(None, alias="user_id")
    vcard: Optional[str] = Field(None, alias="vcard")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Dice(BaseModel):
    emoji: str = Field(..., alias="emoji")
    value: int = Field(..., alias="value")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PollOption(BaseModel):
    text: str = Field(..., alias="text")
    voter_count: int = Field(..., alias="voter_count")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PollAnswer(BaseModel):
    poll_id: str = Field(..., alias="poll_id")
    user: User = Field(..., alias="user")
    option_ids: List[int] = Field(..., alias="option_ids")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Poll(BaseModel):
    id: str = Field(..., alias="id")
    question: str = Field(..., alias="question")
    options: List[PollOption] = Field(..., alias="options")
    total_voter_count: int = Field(..., alias="total_voter_count")
    is_closed: bool = Field(..., alias="is_closed")
    is_anonymous: bool = Field(..., alias="is_anonymous")
    type: str = Field(..., alias="type")
    allows_multiple_answers: bool = Field(..., alias="allows_multiple_answers")
    correct_option_id: Optional[int] = Field(None, alias="correct_option_id")
    explanation: Optional[str] = Field(None, alias="explanation")
    explanation_entities: Optional[List[MessageEntity]] = Field(None, alias="explanation_entities")
    open_period: Optional[int] = Field(None, alias="open_period")
    close_date: Optional[int] = Field(None, alias="close_date")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Location(BaseModel):
    longitude: float = Field(..., alias="longitude")
    latitude: float = Field(..., alias="latitude")
    horizontal_accuracy: Optional[float] = Field(None, alias="horizontal_accuracy")
    live_period: Optional[int] = Field(None, alias="live_period")
    heading: Optional[int] = Field(None, alias="heading")
    proximity_alert_radius: Optional[int] = Field(None, alias="proximity_alert_radius")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Venue(BaseModel):
    location: Location = Field(..., alias="location")
    title: str = Field(..., alias="title")
    address: str = Field(..., alias="address")
    foursquare_id: Optional[str] = Field(None, alias="foursquare_id")
    foursquare_type: Optional[str] = Field(None, alias="foursquare_type")
    google_place_id: Optional[str] = Field(None, alias="google_place_id")
    google_place_type: Optional[str] = Field(None, alias="google_place_type")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Invoice(BaseModel):
    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")
    start_parameter: str = Field(..., alias="start_parameter")
    currency: str = Field(..., alias="currency")
    total_amount: int = Field(..., alias="total_amount")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class OrderInfo(BaseModel):
    name: Optional[str] = Field(None, alias="name")
    phone_number: Optional[str] = Field(None, alias="phone_number")
    email: Optional[str] = Field(None, alias="email")
    shipping_address: Optional[ShippingAddress] = Field(None, alias="shipping_address")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ShippingAddress(BaseModel):
    country_code: str = Field(..., alias="country_code")
    state: str = Field(..., alias="state")
    city: str = Field(..., alias="city")
    street_line1: str = Field(..., alias="street_line1")
    street_line2: str = Field(..., alias="street_line2")
    post_code: str = Field(..., alias="post_code")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class SuccessfulPayment(BaseModel):
    currency: str = Field(..., alias="currency")
    total_amount: int = Field(..., alias="total_amount")
    invoice_payload: str = Field(..., alias="invoice_payload")
    shipping_option_id: Optional[str] = Field(None, alias="shipping_option_id")
    order_info: Optional[OrderInfo] = Field(None, alias="order_info")
    telegram_payment_charge_id: str = Field(..., alias="telegram_payment_charge_id")
    provider_payment_charge_id: str = Field(..., alias="provider_payment_charge_id")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PassportFile(BaseModel):
    file_id: str = Field(..., alias="file_id")
    file_unique_id: str = Field(..., alias="file_unique_id")
    file_size: int = Field(..., alias="file_size")
    file_date: int = Field(..., alias="file_date")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class EncryptedPassportElement(BaseModel):
    type: str = Field(..., alias="type")
    data: Optional[str] = Field(None, alias="data")
    phone_number: Optional[str] = Field(None, alias="phone_number")
    email: Optional[str] = Field(None, alias="email")
    files: Optional[List[PassportFile]] = Field(None, alias="files")
    front_side: Optional[PassportFile] = Field(None, alias="front_side")
    reverse_side: Optional[PassportFile] = Field(None, alias="reverse_side")
    selfie: Optional[PassportFile] = Field(None, alias="selfie")
    translation: Optional[List[PassportFile]] = Field(None, alias="translation")
    hash: str = Field(..., alias="hash")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class EncryptedCredentials(BaseModel):
    data: str = Field(..., alias="data")
    hash: str = Field(..., alias="hash")
    secret: str = Field(..., alias="secret")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PassportData(BaseModel):
    data: List[EncryptedPassportElement] = Field(..., alias="data")
    credentials: EncryptedCredentials = Field(..., alias="credentials")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ProximityAlertTriggered(BaseModel):
    traveler: User = Field(..., alias="traveler")
    watcher: User = Field(..., alias="watcher")
    distance: int = Field(..., alias="distance")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class MessageAutoDeleteTimerChanged(BaseModel):
    message_auto_delete_time: int = Field(..., alias="message_auto_delete_time")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class VoiceChatScheduled(BaseModel):
    start_date: int = Field(..., alias="start_date")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class VoiceChatStarted(BaseModel):
    pass

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class VoiceChatEnded(BaseModel):
    duration: int = Field(..., alias="duration")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class VoiceChatParticipantsInvited(BaseModel):
    users: List[User] = Field(..., alias="users")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ForumTopicCreated(BaseModel):
    message_thread_id: int = Field(..., alias="message_thread_id")
    name: str = Field(..., alias="name")
    icon_color: int = Field(..., alias="icon_color")
    icon_custom_emoji_id: Optional[str] = Field(None, alias="icon_custom_emoji_id")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ForumTopicClosed(BaseModel):
    message_thread_id: int = Field(..., alias="message_thread_id")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ForumTopicReopened(BaseModel):
    message_thread_id: int = Field(..., alias="message_thread_id")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class GeneralForumTopicHidden(BaseModel):
    pass

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class GeneralForumTopicUnhidden(BaseModel):
    pass

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class LoginUrl(BaseModel):
    url: str = Field(..., alias="url")
    forward_text: Optional[str] = Field(None, alias="forward_text")
    bot_username: Optional[str] = Field(None, alias="bot_username")
    request_write_access: Optional[bool] = Field(None, alias="request_write_access")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class CallbackGame(BaseModel):
    pass

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class WebAppInfo(BaseModel):
    url: str = Field(..., alias="url")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class InlineKeyboardButton(BaseModel):
    text: str = Field(..., alias="text")
    url: Optional[str] = Field(None, alias="url")
    login_url: Optional[LoginUrl] = Field(None, alias="login_url")
    callback_data: Optional[str] = Field(None, alias="callback_data")
    switch_inline_query: Optional[str] = Field(None, alias="switch_inline_query")
    switch_inline_query_current_chat: Optional[str] = Field(None, alias="switch_inline_query_current_chat")
    callback_game: Optional[CallbackGame] = Field(None, alias="callback_game")
    pay: Optional[bool] = Field(None, alias="pay")
    web_app: Optional[WebAppInfo] = Field(None, alias="web_app")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class InlineKeyboardMarkup(BaseModel):
    inline_keyboard: List[List[InlineKeyboardButton]] = Field(..., alias="inline_keyboard")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class WebAppData(BaseModel):
    data: str = Field(..., alias="data")
    button_text: str = Field(..., alias="button_text")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class Game(BaseModel):
    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None


class Message(BaseModel):
    message_id: int = Field(..., alias="message_id")
    from_user: Optional[User] = Field(None, alias="from")
    sender_chat: Optional[Chat] = Field(None, alias="sender_chat")
    date: int = Field(..., alias="date")
    chat: Chat = Field(..., alias="chat")
    forward_from: Optional[User] = Field(None, alias="forward_from")
    forward_from_chat: Optional[Chat] = Field(None, alias="forward_from_chat")
    forward_from_message_id: Optional[int] = Field(None, alias="forward_from_message_id")
    forward_signature: Optional[str] = Field(None, alias="forward_signature")
    forward_sender_name: Optional[str] = Field(None, alias="forward_sender_name")
    forward_date: Optional[int] = Field(None, alias="forward_date")
    is_topic_message: Optional[bool] = Field(None, alias="is_topic_message")
    is_automatic_forward: Optional[bool] = Field(None, alias="is_automatic_forward")
    reply_to_message: Optional[Message] = Field(None, alias="reply_to_message")
    via_bot: Optional[User] = Field(None, alias="via_bot")
    edit_date: Optional[int] = Field(None, alias="edit_date")
    has_protected_content: Optional[bool] = Field(None, alias="has_protected_content")
    media_group_id: Optional[str] = Field(None, alias="media_group_id")
    author_signature: Optional[str] = Field(None, alias="author_signature")
    text: Optional[str] = Field(None, alias="text")
    entities: Optional[List[MessageEntity]] = Field(None, alias="entities")
    animation: Optional[Animation] = Field(None, alias="animation")
    audio: Optional[Audio] = Field(None, alias="audio")
    document: Optional[Document] = Field(None, alias="document")
    photo: Optional[List[PhotoSize]] = Field(None, alias="photo")
    sticker: Optional[Sticker] = Field(None, alias="sticker")
    video: Optional[Video] = Field(None, alias="video")
    video_note: Optional[VideoNote] = Field(None, alias="video_note")
    voice: Optional[Voice] = Field(None, alias="voice")
    caption: Optional[str] = Field(None, alias="caption")
    caption_entities: Optional[List[MessageEntity]] = Field(None, alias="caption_entities")
    contact: Optional[Contact] = Field(None, alias="contact")
    dice: Optional[Dice] = Field(None, alias="dice")
    game: Optional[Game] = Field(None, alias="game")
    poll: Optional[Poll] = Field(None, alias="poll")
    venue: Optional[Venue] = Field(None, alias="venue")
    location: Optional[Location] = Field(None, alias="location")
    new_chat_members: Optional[List[User]] = Field(None, alias="new_chat_members")
    left_chat_member: Optional[User] = Field(None, alias="left_chat_member")
    new_chat_title: Optional[str] = Field(None, alias="new_chat_title")
    new_chat_photo: Optional[List[PhotoSize]] = Field(None, alias="new_chat_photo")
    delete_chat_photo: Optional[bool] = Field(None, alias="delete_chat_photo")
    group_chat_created: Optional[bool] = Field(None, alias="group_chat_created")
    supergroup_chat_created: Optional[bool] = Field(None, alias="supergroup_chat_created")
    channel_chat_created: Optional[bool] = Field(None, alias="channel_chat_created")
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = Field(None, alias="message_auto_delete_timer_changed")
    migrate_to_chat_id: Optional[int] = Field(None, alias="migrate_to_chat_id")
    migrate_from_chat_id: Optional[int] = Field(None, alias="migrate_from_chat_id")
    pinned_message: Optional[Message] = Field(None, alias="pinned_message")
    invoice: Optional[Invoice] = Field(None, alias="invoice")
    successful_payment: Optional[SuccessfulPayment] = Field(None, alias="successful_payment")
    connected_website: Optional[str] = Field(None, alias="connected_website")
    passport_data: Optional[PassportData] = Field(None, alias="passport_data")
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = Field(None, alias="proximity_alert_triggered")
    forum_topic_created: Optional[ForumTopicCreated] = Field(None, alias="forum_topic_created")
    forum_topic_closed: Optional[ForumTopicClosed] = Field(None, alias="forum_topic_closed")
    forum_topic_reopened: Optional[ForumTopicReopened] = Field(None, alias="forum_topic_reopened")
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = Field(None, alias="general_forum_topic_hidden")
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = Field(None, alias="general_forum_topic_unhidden")
    voice_chat_scheduled: Optional[VoiceChatScheduled] = Field(None, alias="voice_chat_scheduled")
    voice_chat_started: Optional[VoiceChatStarted] = Field(None, alias="voice_chat_started")
    voice_chat_ended: Optional[VoiceChatEnded] = Field(None, alias="voice_chat_ended")
    voice_chat_participants_invited: Optional[VoiceChatParticipantsInvited] = Field(None, alias="voice_chat_participants_invited")
    reply_markup: Optional[InlineKeyboardMarkup] = Field(None, alias="reply_markup")
    web_app_data: Optional[WebAppData] = Field(None, alias="web_app_data")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @staticmethod
    def convert_unicode(text: str) -> str:
        """
        Converts Persian digits to English digits.
        """
        trans_table = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
        return text.translate(trans_table)

    @field_validator("text", mode="before", check_fields=True)
    def normalize_text(cls, v):
        if v is not None:
            return cls.convert_unicode(v)
        return v

class InlineQuery(BaseModel):
    id: str = Field(..., alias="id")
    from_user: User = Field(..., alias="from")
    query: str = Field(..., alias="query")
    offset: str = Field(..., alias="offset")
    chat_type: Optional[str] = Field(None, alias="chat_type")
    location: Optional[Location] = Field(None, alias="location")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ChosenInlineResult(BaseModel):
    result_id: str = Field(..., alias="result_id")
    from_user: User = Field(..., alias="from")
    location: Optional[Location] = Field(None, alias="location")
    inline_message_id: Optional[str] = Field(None, alias="inline_message_id")
    query: str = Field(..., alias="query")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class CallbackQuery(BaseModel):
    id: str = Field(..., alias="id")
    from_user: User = Field(..., alias="from")
    message: Optional[Message] = Field(None, alias="message")
    inline_message_id: Optional[str] = Field(None, alias="inline_message_id")
    chat_instance: str = Field(..., alias="chat_instance")
    data: Optional[str] = Field(None, alias="data")
    game_short_name: Optional[str] = Field(None, alias="game_short_name")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ShippingQuery(BaseModel):
    id: str = Field(..., alias="id")
    from_user: User = Field(..., alias="from")
    invoice_payload: str = Field(..., alias="invoice_payload")
    shipping_address: ShippingAddress = Field(..., alias="shipping_address")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class PreCheckoutQuery(BaseModel):
    id: str = Field(..., alias="id")
    from_user: User = Field(..., alias="from")
    currency: str = Field(..., alias="currency")
    total_amount: int = Field(..., alias="total_amount")
    invoice_payload: str = Field(..., alias="invoice_payload")
    shipping_option_id: Optional[str] = Field(None, alias="shipping_option_id")
    order_info: Optional[OrderInfo] = Field(None, alias="order_info")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ChatInviteLink(BaseModel):
    invite_link: str = Field(..., alias="invite_link")
    creator: User = Field(..., alias="creator")
    creates_join_request: bool = Field(..., alias="creates_join_request")
    is_primary: bool = Field(..., alias="is_primary")
    is_revoked: bool = Field(..., alias="is_revoked")
    name: Optional[str] = Field(None, alias="name")
    expire_date: Optional[int] = Field(None, alias="expire_date")
    member_limit: Optional[int] = Field(None, alias="member_limit")
    pending_join_request_count: Optional[int] = Field(None, alias="pending_join_request_count")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class ChatMemberOwner(BaseModel):
    status: Literal["creator"] = Field(..., alias="status")
    user: User = Field(..., alias="user")
    is_anonymous: bool = Field(..., alias="is_anonymous")
    custom_title: Optional[str] = Field(None, alias="custom_title")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class ChatMemberAdministrator(BaseModel):
    status: Literal["administrator"] = Field(..., alias="status")
    user: User = Field(..., alias="user")
    can_be_edited: bool = Field(..., alias="can_be_edited")
    is_anonymous: bool = Field(..., alias="is_anonymous")
    can_manage_chat: bool = Field(..., alias="can_manage_chat")
    can_delete_messages: bool = Field(..., alias="can_delete_messages")
    can_manage_video_chats: bool = Field(..., alias="can_manage_video_chats")
    can_restrict_members: bool = Field(..., alias="can_restrict_members")
    can_promote_members: bool = Field(..., alias="can_promote_members")
    can_change_info: bool = Field(..., alias="can_change_info")
    can_invite_users: bool = Field(..., alias="can_invite_users")
    can_post_messages: Optional[bool] = Field(None, alias="can_post_messages")
    can_edit_messages: Optional[bool] = Field(None, alias="can_edit_messages")
    can_pin_messages: Optional[bool] = Field(None, alias="can_pin_messages")
    can_manage_topics: Optional[bool] = Field(None, alias="can_manage_topics")
    custom_title: Optional[str] = Field(None, alias="custom_title")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class ChatMemberMember(BaseModel):
    status: Literal["member"] = Field(..., alias="status")
    user: User = Field(..., alias="user")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class ChatMemberRestricted(BaseModel):
    status: Literal["restricted"] = Field(..., alias="status")
    user: User = Field(..., alias="user")
    is_member: bool = Field(..., alias="is_member")
    can_send_messages: Optional[bool] = Field(None, alias="can_send_messages")
    can_send_media_messages: Optional[bool] = Field(None, alias="can_send_media_messages")
    can_send_polls: Optional[bool] = Field(None, alias="can_send_polls")
    can_send_other_messages: Optional[bool] = Field(None, alias="can_send_other_messages")
    can_add_web_page_previews: Optional[bool] = Field(None, alias="can_add_web_page_previews")
    can_change_info: Optional[bool] = Field(None, alias="can_change_info")
    can_invite_users: Optional[bool] = Field(None, alias="can_invite_users")
    can_pin_messages: Optional[bool] = Field(None, alias="can_pin_messages")
    can_manage_topics: Optional[bool] = Field(None, alias="can_manage_topics")
    until_date: int = Field(..., alias="until_date")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class ChatMemberLeft(BaseModel):
    status: Literal["left"] = Field(..., alias="status")
    user: User = Field(..., alias="user")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

class ChatMemberBanned(BaseModel):
    status: Literal["kicked"] = Field(..., alias="status")
    user: User = Field(..., alias="user")
    until_date: int = Field(..., alias="until_date")

    model_config = ConfigDict(populate_by_name=True, extra="allow")

ChatMember = Union[
    ChatMemberOwner,
    ChatMemberAdministrator,
    ChatMemberMember,
    ChatMemberRestricted,
    ChatMemberLeft,
    ChatMemberBanned,
]

class ChatMemberUpdated(BaseModel):
    chat: Chat = Field(..., alias="chat")
    from_user: User = Field(..., alias="from")
    date: int = Field(..., alias="date")
    old_chat_member: ChatMember = Field(..., alias="old_chat_member")
    new_chat_member: ChatMember = Field(..., alias="new_chat_member")
    invite_link: Optional[ChatInviteLink] = Field(None, alias="invite_link")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class ChatJoinRequest(BaseModel):
    chat: Chat = Field(..., alias="chat")
    from_user: User = Field(..., alias="from")
    date: int = Field(..., alias="date")
    bio: Optional[str] = Field(None, alias="bio")
    invite_link: Optional[ChatInviteLink] = Field(None, alias="invite_link")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class Update(BaseModel):
    update_id: int = Field(..., alias="update_id")
    message: Optional[Message] = Field(None, alias="message")
    edited_message: Optional[Message] = Field(None, alias="edited_message")
    channel_post: Optional[Message] = Field(None, alias="channel_post")
    edited_channel_post: Optional[Message] = Field(None, alias="edited_channel_post")
    inline_query: Optional[InlineQuery] = Field(None, alias="inline_query")
    chosen_inline_result: Optional[ChosenInlineResult] = Field(None, alias="chosen_inline_result")
    callback_query: Optional[CallbackQuery] = Field(None, alias="callback_query")
    shipping_query: Optional[ShippingQuery] = Field(None, alias="shipping_query")
    pre_checkout_query: Optional[PreCheckoutQuery] = Field(None, alias="pre_checkout_query")
    poll: Optional[Poll] = Field(None, alias="poll")
    poll_answer: Optional[PollAnswer] = Field(None, alias="poll_answer")
    my_chat_member: Optional[ChatMemberUpdated] = Field(None, alias="my_chat_member")
    chat_member: Optional[ChatMemberUpdated] = Field(None, alias="chat_member")
    chat_join_request: Optional[ChatJoinRequest] = Field(None, alias="chat_join_request")

    model_config = ConfigDict(populate_by_name=True, extra="allow")


# Resolve forward references
InlineQuery.model_rebuild()
ChosenInlineResult.model_rebuild()
CallbackQuery.model_rebuild()
ShippingQuery.model_rebuild()
PreCheckoutQuery.model_rebuild()
ChatInviteLink.model_rebuild()
ChatMemberUpdated.model_rebuild()
ChatJoinRequest.model_rebuild()
Update.model_rebuild()
Chat.model_rebuild()
Message.model_rebuild()
ChatMemberOwner.model_rebuild()
ChatMemberAdministrator.model_rebuild()
ChatMemberMember.model_rebuild()
ChatMemberRestricted.model_rebuild()
ChatMemberLeft.model_rebuild()
ChatMemberBanned.model_rebuild()
