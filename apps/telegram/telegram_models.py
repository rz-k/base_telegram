from __future__ import annotations

from typing import Annotated, List, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    PositiveInt,
    TypeAdapter,
    field_validator,
    model_validator,
)


class _BaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
    )

    def to_dict(self, **kwargs):
        return self.model_dump(exclude_none=True, **kwargs)


class Update(_BaseModel):
    update_id: int
    message: Message | None = None
    edited_message: Message | None = None
    channel_post: Message | None = None
    edited_channel_post: Message | None = None
    business_connection: BusinessConnection | None = None
    business_message: Message | None = None
    edited_business_message: Message | None = None
    deleted_business_messages: BusinessMessagesDeleted | None = None
    guest_message: Message | None = None
    message_reaction: MessageReactionUpdated | None = None
    message_reaction_count: MessageReactionCountUpdated | None = None
    inline_query: InlineQuery | None = None
    chosen_inline_result: ChosenInlineResult | None = None
    callback_query: CallbackQuery | None = None
    shipping_query: ShippingQuery | None = None
    pre_checkout_query: PreCheckoutQuery | None = None
    purchased_paid_media: PaidMediaPurchased | None = None
    poll: Poll | None = None
    poll_answer: PollAnswer | None = None
    my_chat_member: ChatMemberUpdated | None = None
    chat_member: ChatMemberUpdated | None = None
    chat_join_request: ChatJoinRequest | None = None
    chat_boost: ChatBoostUpdated | None = None
    removed_chat_boost: ChatBoostRemoved | None = None
    managed_bot: ManagedBotUpdated | None = None


class User(_BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    can_join_groups: bool | None = None
    can_read_all_group_messages: bool | None = None
    supports_guest_queries: bool | None = None
    supports_inline_queries: bool | None = None
    can_connect_to_business: bool | None = None
    has_main_web_app: bool | None = None
    has_topics_enabled: bool | None = None
    allows_users_to_create_topics: bool | None = None
    can_manage_bots: bool | None = None
    supports_join_request_queries: bool | None = None


class Chat(_BaseModel):
    id: int
    type: str
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_forum: bool | None = None
    is_direct_messages: str | None = None


class ChatFullInfo(_BaseModel):
    id: int
    type: str
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_forum: bool | None = None
    is_direct_messages: bool | None = None
    accent_color_id: int
    max_reaction_count: int
    photo: ChatPhoto | None = None
    active_usernames: List[str] | None = None
    birthdate: Birthdate | None = None
    business_intro: BusinessIntro | None = None
    business_location: BusinessLocation | None = None
    business_opening_hours: BusinessOpeningHours | None = None
    personal_chat: Chat | None = None
    parent_chat: Chat | None = None
    available_reactions: List[ReactionType] | None = None
    background_custom_emoji_id: str | None = None
    profile_accent_color_id: int | None = None
    profile_background_custom_emoji_id: str | None = None
    emoji_status_custom_emoji_id: str | None = None
    emoji_status_expiration_date: int | None = None
    bio: str | None = None
    has_private_forwards: bool | None = None
    has_restricted_voice_and_video_messages: bool | None = None
    join_to_send_messages: bool | None = None
    join_by_request: bool | None = None
    description: str | None = None
    invite_link: str | None = None
    pinned_message: Message | None = None
    permissions: ChatPermissions | None = None
    accepted_gift_types: AcceptedGiftTypes
    can_send_paid_media: bool | None = None
    slow_mode_delay: int | None = None
    unrestrict_boost_count: int | None = None
    message_auto_delete_time: int | None = None
    has_aggressive_anti_spam_enabled: bool | None = None
    has_hidden_members: bool | None = None
    has_protected_content: bool | None = None
    has_visible_history: bool | None = None
    sticker_set_name: str | None = None
    can_set_sticker_set: bool | None = None
    custom_emoji_sticker_set_name: str | None = None
    linked_chat_id: int | None = None
    location: ChatLocation | None = None
    rating: UserRating | None = None
    first_profile_audio: Audio | None = None
    unique_gift_colors: UniqueGiftColors | None = None
    paid_message_star_count: int | None = None
    guard_bot: User | None = None


class Message(_BaseModel):
    """Telegram Message object representation."""

    message_id: int = Field(..., alias="id")
    message_thread_id: int | None = None
    direct_messages_topic: DirectMessagesTopic | None = None
    from_user: User | None = Field(None, alias="from")
    sender_chat: Chat | None = None
    sender_boost_count: int | None = None
    sender_business_bot: User | None = None
    sender_tag: str | None = None
    date: PositiveInt
    guest_query_id: str | None = None
    business_connection_id: str | None = None
    chat: Chat
    forward_origin: MessageOrigin | None = None
    is_topic_message: bool | None = None
    is_automatic_forward: bool | None = None
    reply_to_message: Message | None = None
    external_reply: ExternalReplyInfo | None = None
    quote: TextQuote | None = None
    reply_to_story: Story | None = None
    reply_to_checklist_task_id: int | None = None
    reply_to_poll_option_id: str | None = None
    via_bot: User | None = None
    guest_bot_caller_user: User | None = None
    guest_bot_caller_chat: Chat | None = None
    edit_date: int | None = None
    has_protected_content: bool | None = None
    is_from_offline: bool | None = None
    is_paid_post: bool | None = None
    media_group_id: str | None = None
    author_signature: str | None = None
    paid_star_count: int | None = None
    text: str | None = None
    entities: List[MessageEntity] | None = None
    link_preview_options: LinkPreviewOptions | None = None
    suggested_post_info: SuggestedPostInfo | None = None
    effect_id: str | None = None
    rich_message: RichMessage | None = None
    animation: Animation | None = None
    audio: Audio | None = None
    document: Document | None = None
    live_photo: LivePhoto | None = None
    paid_media: PaidMediaInfo | None = None
    photo: List[PhotoSize] | None = None
    sticker: Sticker | None = None
    story: Story | None = None
    video: Video | None = None
    video_note: VideoNote | None = None
    voice: Voice | None = None
    caption: str | None = None
    caption_entities: List[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    has_media_spoiler: bool | None = None
    checklist: Checklist | None = None
    contact: Contact | None = None
    dice: Dice | None = None
    game: Game | None = None
    poll: Poll | None = None
    venue: Venue | None = None
    location: Location | None = None
    new_chat_members: List[User] | None = None
    left_chat_member: User | None = None
    chat_owner_left: ChatOwnerLeft | None = None
    chat_owner_changed: ChatOwnerChanged | None = None
    new_chat_title: str | None = None
    new_chat_photo: List[PhotoSize] | None = None
    delete_chat_photo: bool | None = None
    group_chat_created: bool | None = None
    supergroup_chat_created: bool | None = None
    channel_chat_created: bool | None = None
    message_auto_delete_timer_changed: MessageAutoDeleteTimerChanged | None = None
    migrate_to_chat_id: int | None = None
    migrate_from_chat_id: int | None = None
    pinned_message: Message | None = None
    invoice: Invoice | None = None
    successful_payment: SuccessfulPayment | None = None
    refunded_payment: RefundedPayment | None = None
    users_shared: UsersShared | None = None
    chat_shared: ChatShared | None = None
    gift: Gift | None = None
    unique_gift: UniqueGift | None = None
    gift_upgrade_sent: GiftInfo | None = None
    connected_website: str | None = None
    write_access_allowed: WriteAccessAllowed | None = None
    passport_data: PassportData | None = None
    proximity_alert_triggered: ProximityAlertTriggered | None = None
    boost_added: ChatBoostAdded | None = None
    chat_background_set: ChatBackground | None = None
    checklist_tasks_done: ChecklistTasksDone | None = None
    checklist_tasks_added: ChecklistTasksAdded | None = None
    direct_message_price_changed: DirectMessagePriceChanged | None = None
    forum_topic_created: ForumTopicCreated | None = None
    forum_topic_edited: ForumTopicEdited | None = None
    forum_topic_closed: ForumTopicClosed | None = None
    forum_topic_reopened: ForumTopicReopened | None = None
    general_forum_topic_hidden: GeneralForumTopicHidden | None = None
    general_forum_topic_unhidden: GeneralForumTopicUnhidden | None = None
    giveaway_created: GiveawayCreated | None = None
    giveaway: Giveaway | None = None
    giveaway_winners: GiveawayWinners | None = None
    giveaway_completed: GiveawayCompleted | None = None
    managed_bot_created: ManagedBotCreated | None = None
    paid_message_price_changed: PaidMessagePriceChanged | None = None
    poll_option_added: PollOptionAdded | None = None
    poll_option_deleted: PollOptionDeleted | None = None
    suggested_post_approved: SuggestedPostApproved | None = None
    suggested_post_approval_failed: SuggestedPostApprovalFailed | None = None
    suggested_post_declined: SuggestedPostDeclined | None = None
    suggested_post_paid: SuggestedPostPaid | None = None
    suggested_post_refunded: SuggestedPostRefunded | None = None
    video_chat_scheduled: VideoChatScheduled | None = None
    video_chat_started: VideoChatStarted | None = None
    video_chat_ended: VideoChatEnded | None = None
    video_chat_participants_invited: VideoChatParticipantsInvited | None = None
    web_app_data: WebAppData | None = None
    reply_markup: InlineKeyboardMarkup | None = None

    @property
    def id(self) -> int:
        return self.message_id

    @staticmethod
    def convert_unicode(text: str) -> str:
        """
        Converts Persian/Arabic digits to English/Latin digits.
        """
        persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
        arabic_to_english = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
        text = text.translate(persian_to_english)
        return text.translate(arabic_to_english)

    @field_validator("text", mode="before", check_fields=True)
    def normalize_text(cls, v):
        if v is not None:
            return cls.convert_unicode(v)
        return v


class MessageId(_BaseModel):
    message_id: int


class InaccessibleMessage(_BaseModel):
    chat: Chat
    message_id: int
    date: Literal[0] = 0


class MessageEntity(_BaseModel):
    type: str
    offset: int
    length: int
    url: str | None = None
    user: User | None = None
    language: str | None = None
    custom_emoji_id: str | None = None
    date_time_format: str | None = None


class TextQuote(_BaseModel):
    text: str
    entities: List[MessageEntity] | None = None
    position: int
    is_manual: bool


class ExternalReplyInfo(_BaseModel):
    origin: MessageOrigin | None
    chat: Chat | None = None
    message_id: int | None = None
    link_preview_options: LinkPreviewOptions | None = None
    animation: Animation | None = None
    audio: Audio | None = None
    document: Document | None = None
    live_photo: LivePhoto | None = None
    paid_media: PaidMediaInfo | None = None
    photo: list[PhotoSize] | None = None
    sticker: Sticker | None = None
    story: Story | None = None
    video: Video | None = None
    video_note: VideoNote | None = None
    voice: Voice | None = None
    has_media_spoiler: bool | None = None
    checklist: Checklist | None = None
    contact: Contact | None = None
    dice: Dice | None = None
    game: Game | None = None
    giveaway: Giveaway | None = None
    giveaway_winners: GiveawayWinners | None = None
    invoice: Invoice | None = None
    location: Location | None = None
    poll: Poll | None = None
    venue: Venue | None = None


class ReplyParameters(_BaseModel):
    message_id: int
    chat_id: int | str | None = None
    allow_sending_without_reply: bool | None = None
    quote: str | None = None
    quote_parse_mode: str | None = None
    quote_entities: List[MessageEntity] | None = None
    quote_position: int | None = None
    checklist_task_id: int | None = None
    poll_option_id: str | None = None


class MessageOriginUser(_BaseModel):
    type: Literal["user"] = "user"
    date: int
    sender_user: User


class MessageOriginHiddenUser(_BaseModel):
    type: Literal["hidden_user"] = "hidden_user"
    date: int
    sender_user_name: str


class MessageOriginChat(_BaseModel):
    type: Literal["chat"] = "chat"
    date: int
    sender_chat: Chat
    author_signature: str | None = None


class MessageOriginChannel(_BaseModel):
    type: Literal["channel"] = "channel"
    date: int
    chat: Chat
    message_id: int
    author_signature: str | None = None


class PhotoSize(_BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None = None


class Animation(_BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class Audio(_BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    performer: str | None = None
    title: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    thumbnail: PhotoSize | None = None


class Document(_BaseModel):
    file_id: str
    file_unique_id: str
    thumbnail: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class LivePhoto(_BaseModel):
    photo: list[PhotoSize] | None = None
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    mime_type: str | None = None
    file_size: int | None = None


class Story(_BaseModel):
    chat: Chat
    id: int


class VideoQuality(_BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    codec: str
    file_size: int | None = None


class Video(_BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: PhotoSize | None = None
    cover: list[PhotoSize] | None = None
    start_timestamp: int | None = None
    qualities: list[VideoQuality] | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class VideoNote(_BaseModel):
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumbnail: PhotoSize | None = None
    file_size: int | None = None


class MaskPosition(_BaseModel):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class File(_BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int | None = None
    file_path: str | None = None


class Sticker(_BaseModel):
    file_id: str
    file_unique_id: str
    type: str  # regular | mask | custom_emoji
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: PhotoSize | None = None
    emoji: str | None = None
    set_name: str | None = None
    premium_animation: File | None = None
    mask_position: MaskPosition | None = None
    custom_emoji_id: str | None = None
    needs_repainting: bool | None = None
    file_size: int | None = None


class StickerSet(_BaseModel):
    name: str
    title: str
    sticker_type: str  # "regular", "mask", "custom_emoji"
    stickers: List[Sticker]
    thumbnail: PhotoSize | None = None


class InputSticker(_BaseModel):
    sticker: str
    format_: str = Field(..., alias="format")  # "static", "animated", "video"
    emoji_list: list[str]
    mask_position: MaskPosition | None = None
    keywords: list[str] | None = None


class RichMessage(_BaseModel):
    blocks: list[RichBlock]
    is_rtl: bool | None = None


class InputRichMessage(_BaseModel):
    html: str | None = None
    markdown: str | None = None
    is_rtl: bool | None = None
    skip_entity_detection: bool | None = None


class RichTextBold(_BaseModel):
    type: str = "bold"
    text: RichText


class RichTextItalic(_BaseModel):
    type: str = "italic"
    text: RichText


class RichTextUnderline(_BaseModel):
    type: str = "underline"
    text: RichText


class RichTextStrikethrough(_BaseModel):
    type: str = "strikethrough"
    text: RichText


class RichTextSpoiler(_BaseModel):
    type: str = "spoiler"
    text: RichText


class RichTextDateTime(_BaseModel):
    type: str = "date_time"
    text: RichText
    unix_time: int
    date_time_format: str


class RichTextTextMention(_BaseModel):
    type: str = "text_mention"
    text: RichText
    user: User


class RichTextSubscript(_BaseModel):
    type: str = "subscript"
    text: RichText


class RichTextSuperscript(_BaseModel):
    type: str = "superscript"
    text: RichText


class RichTextMarked(_BaseModel):
    type: str = "marked"
    text: RichText


class RichTextCode(_BaseModel):
    type: str = "code"
    text: RichText


class RichTextCustomEmoji(_BaseModel):
    type: str = "custom_emoji"
    custom_emoji_id: str
    alternative_text: str


class RichTextMathematicalExpression(_BaseModel):
    type: str = "mathematical_expression"
    expression: str


class RichTextUrl(_BaseModel):
    type: str = "url"
    text: RichText
    url: str


class RichTextEmailAddress(_BaseModel):
    type: str = "email_address"
    text: RichText
    email_address: str


class RichTextPhoneNumber(_BaseModel):
    type: str = "phone_number"
    text: RichText
    phone_number: str


class RichTextBankCardNumber(_BaseModel):
    type: str = "bank_card_number"
    text: RichText
    bank_card_number: str


class RichTextMention(_BaseModel):
    type: str = "mention"
    text: RichText
    username: str


class RichTextHashtag(_BaseModel):
    type: str = "hashtag"
    text: RichText
    hashtag: str


class RichTextCashtag(_BaseModel):
    type: str = "cashtag"
    text: RichText
    cashtag: str


class RichTextBotCommand(_BaseModel):
    type: str = "bot_command"
    text: RichText
    bot_command: str


class RichTextAnchor(_BaseModel):
    type: str = "anchor"
    name: str


class RichTextAnchorLink(_BaseModel):
    type: str = "anchor_link"
    text: RichText
    anchor_name: str


class RichTextReference(_BaseModel):
    type: str = "reference"
    text: RichText
    name: str


class RichTextReferenceLink(_BaseModel):
    type: str = "reference_link"
    text: RichText
    reference_name: str


class RichBlockCaption(_BaseModel):
    text: RichText
    credit: RichText


class RichBlockTableCell(_BaseModel):
    text: RichText
    is_header: bool | None
    colspan: int | None
    rowspan: int | None
    align: str
    valign: str


class RichBlockListItem(_BaseModel):
    label: str
    blocks: List[RichBlock]
    has_checkbox: bool | None
    is_checked: bool | None
    value: int | None
    type: str | None


class RichBlockParagraph(_BaseModel):
    type: str = "paragraph"
    text: RichText


class RichBlockSectionHeading(_BaseModel):
    type: str = "heading"
    text: RichText
    size: int


class RichBlockPreformatted(_BaseModel):
    type: str = "pre"
    text: RichText
    language: str | None


class RichBlockFooter(_BaseModel):
    type: str = "footer"
    text: RichText


class RichBlockDivider(_BaseModel):
    type: str = "divider"


class RichBlockMathematicalExpression(_BaseModel):
    type: str = "mathematical_expression"
    expression: str


class RichBlockAnchor(_BaseModel):
    type: str = "anchor"
    name: str


class RichBlockList(_BaseModel):
    type: str = "list"
    items: list[RichBlockListItem]


class RichBlockBlockQuotation(_BaseModel):
    type: str = "blockquote"
    blocks: list[RichBlock]
    credit: RichText


class RichBlockPullQuotation(_BaseModel):
    type: str = "pullquote"
    text: RichText
    credit: RichText


class RichBlockCollage(_BaseModel):
    type: str = "collage"
    blocks: list[RichBlock]
    caption: RichBlockCaption | None = None


class RichBlockSlideshow(_BaseModel):
    type: str = "slideshow"
    blocks: list[RichBlock]
    caption: RichBlockCaption | None = None


class RichBlockTable(_BaseModel):
    type: str = "table"
    cells: list[list[RichBlockTableCell]]
    is_bordered: bool | None = None
    is_striped: bool | None = None
    caption: RichText | None = None


class RichBlockDetails(_BaseModel):
    type: str = "details"
    summary: RichText
    blocks: list[RichBlock]
    is_open: bool | None = None


class RichBlockMap(_BaseModel):
    type: str = "map"
    location: Location
    zoom: int
    width: int
    height: int
    caption: RichBlockCaption | None = None


class RichBlockAnimation(_BaseModel):
    type: str = "animation"
    animation: Animation
    has_spoiler: bool | None = None
    caption: RichBlockCaption | None = None


class RichBlockAudio(_BaseModel):
    type: str = "audio"
    audio: Audio
    caption: RichBlockCaption | None = None


class RichBlockPhoto(_BaseModel):
    type: str = "photo"
    photo: list[PhotoSize]
    has_spoiler: bool | None = None
    caption: RichBlockCaption | None = None


class RichBlockVideo(_BaseModel):
    type: str = "video"
    video: Video
    has_spoiler: bool | None = None
    caption: RichBlockCaption | None = None


class RichBlockVoiceNote(_BaseModel):
    type: str = "voice_note"
    voice_note: Voice
    caption: RichBlockCaption | None = None


class RichBlockThinking(_BaseModel):
    type: str = "thinking"
    text: RichText


class Voice(_BaseModel):
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str | None = None
    file_size: int | None = None


class PaidMedia(_BaseModel):
    type: str


class PaidMediaInfo(_BaseModel):
    star_count: int
    paid_media: list[PaidMedia]


class PaidMediaPreview(_BaseModel):
    type: str = "preview"
    width: int | None = None
    height: int | None = None
    duration: int | None = None


class PaidMediaLivePhoto(_BaseModel):
    type: str = "live_photo"
    live_photo: LivePhoto


class PaidMediaPhoto(_BaseModel):
    type: str = "photo"
    photo: list[PhotoSize]


class PaidMediaVideo(_BaseModel):
    type: str = "video"
    video: Video


class Contact(_BaseModel):
    phone_number: str
    first_name: str
    last_name: str | None = None
    user_id: int | None = None
    vcard: str | None = None


class Dice(_BaseModel):
    emoji: str
    value: int


class Link(_BaseModel):
    url: str


class PollMedia(_BaseModel):
    animation: Animation | None = None
    audio: Audio | None = None
    document: Document | None = None
    link: Link | None = None
    live_photo: LivePhoto | None = None
    location: Location | None = None
    photo: list[PhotoSize] | None = None
    sticker: Sticker | None = None
    venue: Venue | None = None
    video: Video | None = None


class PollOption(_BaseModel):
    persistent_id: str
    text: str
    text_entities: list[MessageEntity] | None = None
    media: PollMedia | None = None
    voter_count: int
    added_by_user: User | None = None
    added_by_chat: Chat | None = None
    addition_date: int | None = None


class InputPollOption(_BaseModel):
    text: str
    text_parse_mode: str | None = None
    text_entities: list[MessageEntity] | None = None
    media: InputPollOptionMedia | None = None


class PollAnswer(_BaseModel):
    poll_id: str
    voter_chat: Chat | None = None
    user: User | None = None
    option_ids: list[int]
    option_persistent_ids: list[str] | None = None


class Poll(_BaseModel):
    id: str
    question: str
    question_entities: list[MessageEntity] | None = None
    options: list[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    members_only: bool
    country_codes: list[str] | None = None
    allows_revoting: bool
    correct_option_ids: list[int] | None = None
    explanation: str | None = None
    explanation_entities: list[MessageEntity] | None = None
    explanation_media: PollMedia | None = None
    open_period: int | None = None
    close_date: int | None = None
    description: str | None = None
    description_entities: list[MessageEntity] | None = None
    media: PollMedia | None = None


class ChecklistTask(_BaseModel):
    id: int
    text: str
    text_entities: list[MessageEntity] | None = None
    completed_by_user: User | None = None
    completed_by_chat: Chat | None = None
    completion_date: int | None = None


class Checklist(_BaseModel):
    title: str
    title_entities: list[MessageEntity] | None = None
    tasks: list[ChecklistTask]
    others_can_add_tasks: bool | None = None
    others_can_mark_tasks_as_done: bool | None = None


class InputChecklistTask(_BaseModel):
    id: int
    text: str
    parse_mode: str | None = None
    text_entities: list[MessageEntity] | None = None


class InputChecklist(_BaseModel):
    title: str
    parse_mode: str | None = None
    title_entities: list[MessageEntity] | None = None
    tasks: list[InputChecklistTask]
    others_can_add_tasks: bool | None = None
    others_can_mark_tasks_as_done: bool | None = None


class ChecklistTasksDone(_BaseModel):
    checklist_message: Message | None = None
    marked_as_done_task_ids: list[int] | None = None
    marked_as_not_done_task_ids: list[int] | None = None


class ChecklistTasksAdded(_BaseModel):
    checklist_message: Message | None = None
    tasks: list[ChecklistTask]


class Location(_BaseModel):
    latitude: float
    longitude: float
    horizontal_accuracy: float | None = None
    live_period: int | None = None
    heading: int | None = None
    proximity_alert_radius: int | None = None


class Venue(_BaseModel):
    location: Location
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None


class WebAppData(_BaseModel):
    data: str
    button_text: str


class ProximityAlertTriggered(_BaseModel):
    traveler: User
    watcher: User
    distance: int


class MessageAutoDeleteTimerChanged(_BaseModel):
    message_auto_delete_time: int


class ManagedBotCreated(_BaseModel):
    bot: User


class ManagedBotUpdated(_BaseModel):
    user: User
    bot: User


class PollOptionAdded(_BaseModel):
    poll_message: MaybeInaccessibleMessage | None = None
    option_persistent_id: str
    option_text: str
    option_text_entities: list[MessageEntity] | None = None


class PollOptionDeleted(_BaseModel):
    poll_message: MaybeInaccessibleMessage | None = None
    option_persistent_id: str
    option_text: str
    option_text_entities: list[MessageEntity] | None = None


class ChatBoostAdded(_BaseModel):
    boost_count: int


class BackgroundFill(_BaseModel):
    type: str


class BackgroundFillSolid(_BaseModel):
    type: Literal["solid"] = "solid"
    color: int


class BackgroundFillGradient(_BaseModel):
    type: Literal["gradient"] = "gradient"
    top_color: int
    bottom_color: int
    rotation_angle: int


class BackgroundFillFreeformGradient(_BaseModel):
    type: Literal["freeform_gradient"] = "freeform_gradient"
    colors: list[int]


class BackgroundType(_BaseModel):
    type: str


class BackgroundTypeFill(_BaseModel):
    type: Literal["fill"] = "fill"
    fill: BackgroundFill
    dark_theme_dimming: int


class BackgroundTypeWallpaper(_BaseModel):
    type: Literal["wallpaper"] = "wallpaper"
    document: Document
    dark_theme_dimming: int
    is_blurred: bool | None = None
    is_moving: bool | None = None


class BackgroundTypePattern(_BaseModel):
    type: Literal["pattern"] = "pattern"
    document: Document
    fill: BackgroundFill
    intensity: int
    is_inverted: bool | None = None
    is_moving: bool | None = None


class BackgroundTypeChatTheme(_BaseModel):
    type: Literal["chat_theme"] = "chat_theme"
    theme_name: str


class ChatBackground(_BaseModel):
    type: BackgroundType


class ForumTopicCreated(_BaseModel):
    name: str
    icon_color: int
    icon_custom_emoji_id: str | None = None
    is_name_implicit: bool | None = None


class ForumTopicClosed(_BaseModel):
    pass


class ForumTopicEdited(_BaseModel):
    name: str | None = None
    icon_custom_emoji_id: str | None = None


class ForumTopicReopened(_BaseModel):
    pass


class GeneralForumTopicHidden(_BaseModel):
    pass


class GeneralForumTopicUnhidden(_BaseModel):
    pass


class SharedUser(_BaseModel):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo: list[PhotoSize] | None = None


class UsersShared(_BaseModel):
    request_id: int
    users: list[SharedUser]


class ChatShared(_BaseModel):
    request_id: int
    chat_id: int
    title: str | None = None
    username: str | None = None
    photo: list[PhotoSize] | None = None


class WriteAccessAllowed(_BaseModel):
    from_request: bool | None = None
    web_app_name: str | None = None
    from_attachment_menu: bool | None = None


class VideoChatScheduled(_BaseModel):
    start_date: int


class VideoChatStarted(_BaseModel):
    pass


class VideoChatEnded(_BaseModel):
    duration: int


class VideoChatParticipantsInvited(_BaseModel):
    users: list[User]


class PaidMessagePriceChanged(_BaseModel):
    paid_message_star_count: int


class DirectMessagePriceChanged(_BaseModel):
    are_direct_messages_enabled: bool
    direct_message_star_count: int | None = None


class GiveawayCreated(_BaseModel):
    prize_star_count: int | None = None


class Giveaway(_BaseModel):
    chats: list[Chat]
    winners_selection_date: int
    winner_count: int
    only_new_members: bool | None = None
    has_public_winners: bool | None = None
    prize_description: str | None = None
    country_codes: list[str] | None = None
    prize_star_count: int | None = None
    premium_subscription_month_count: int | None = None


class GiveawayWinners(_BaseModel):
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: list[User]
    additional_chat_count: int | None = None
    prize_star_count: int | None = None
    premium_subscription_month_count: int | None = None
    unclaimed_prize_count: int | None = None
    only_new_members: bool | None = None
    was_refunded: bool | None = None
    prize_description: str | None = None


class GiveawayCompleted(_BaseModel):
    winner_count: int
    unclaimed_prize_count: int | None = None
    giveaway_message: Message | None = None
    is_star_giveaway: bool | None = None


class LinkPreviewOptions(_BaseModel):
    is_disabled: bool | None = None
    url: str | None = None
    prefer_small_media: bool | None = None
    prefer_large_media: bool | None = None
    show_above_text: bool | None = None


class DirectMessagesTopic(_BaseModel):
    topic_id: int
    user: User | None = None


class UserProfilePhotos(_BaseModel):
    total_count: int
    photos: list[list[PhotoSize]]


class UserProfileAudios(_BaseModel):
    total_count: int
    audios: list[Audio]


class WebAppInfo(_BaseModel):
    url: str


class SentWebAppMessage(_BaseModel):
    web_app_query_id: str
    result: InlineQueryResult


class SentGuestMessage(_BaseModel):
    inline_message_id: str


class CopyTextButton(_BaseModel):
    text: str


class CallbackGame(_BaseModel):
    pass


class Game(_BaseModel):
    title: str
    description: str
    photo: list[PhotoSize]
    text: str | None = None
    text_entities: list[MessageEntity] | None = None
    animation: Animation | None = None


class GameHighScore(_BaseModel):
    position: int
    user: User
    score: int


class ChatInviteLink(_BaseModel):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: str | None = None
    expire_date: int | None = None
    member_limit: int | None = None
    pending_join_request_count: int | None = None
    subscription_period: int | None = None
    subscription_price: int | None = None


class ChatAdministratorRights(_BaseModel):
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: bool | None = None
    can_edit_messages: bool | None = None
    can_pin_messages: bool | None = None
    can_manage_topics: bool | None = None
    can_manage_direct_messages: bool | None = None
    can_manage_tags: bool | None = None


class ChatMemberUpdated(_BaseModel):
    chat: Chat
    from_user: User = Field(..., alias="from")
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: ChatInviteLink | None = None
    via_join_request: bool | None = None
    via_chat_folder_invite_link: bool | None = None


class ChatMemberOwner(_BaseModel):
    status: Literal["creator"] = "creator"
    user: User
    is_anonymous: bool
    custom_title: str | None = None


class ChatMemberAdministrator(_BaseModel):
    status: Literal["administrator"] = "administrator"
    user: User
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: bool | None = None
    can_edit_messages: bool | None = None
    can_pin_messages: bool | None = None
    can_manage_topics: bool | None = None
    can_manage_direct_messages: bool | None = None
    can_manage_tags: bool | None = None
    custom_title: str | None = None


class ChatMemberMember(_BaseModel):
    status: Literal["member"] = "member"
    tag: str | None = None
    user: User
    until_date: int | None = None


class ChatMemberRestricted(_BaseModel):
    status: Literal["restricted"] = "restricted"
    tag: str | None = None
    user: User
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_previews: bool
    can_react_to_messages: bool
    can_edit_tag: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int


class ChatMemberLeft(_BaseModel):
    status: Literal["left"] = "left"
    user: User


class ChatMemberBanned(_BaseModel):
    status: Literal["kicked"] = "kicked"
    user: User
    until_date: int


class ChatJoinRequest(_BaseModel):
    chat: Chat
    from_user: User = Field(..., alias="from")
    user_chat_id: int
    date: int
    bio: str | None = None
    invite_link: ChatInviteLink | None = None
    query_id: str | None = None


class ChatPermissions(_BaseModel):
    can_send_messages: bool | None = None
    can_send_audios: bool | None = None
    can_send_documents: bool | None = None
    can_send_photos: bool | None = None
    can_send_videos: bool | None = None
    can_send_video_notes: bool | None = None
    can_send_voice_notes: bool | None = None
    can_send_polls: bool | None = None
    can_send_other_messages: bool | None = None
    can_add_web_page_previews: bool | None = None
    can_react_to_messages: bool | None = None
    can_edit_tag: bool | None = None
    can_change_info: bool | None = None
    can_invite_users: bool | None = None
    can_pin_messages: bool | None = None
    can_manage_topics: bool | None = None


class ChatPhoto(_BaseModel):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatLocation(_BaseModel):
    location: Location
    address: str


class PreparedInlineMessage(_BaseModel):
    id: str
    expiration_date: int


class KeyboardButtonRequestUsers(_BaseModel):
    request_id: int
    user_is_bot: bool | None = None
    user_is_premium: bool | None = None
    max_quantity: int | None = None
    request_name: bool | None = None
    request_username: bool | None = None
    request_photo: bool | None = None


class KeyboardButtonRequestChat(_BaseModel):
    request_id: int
    chat_is_channel: bool
    chat_is_forum: bool | None = None
    chat_has_username: bool | None = None
    chat_is_created: bool | None = None
    user_administrator_rights: ChatAdministratorRights | None = None
    bot_administrator_rights: ChatAdministratorRights | None = None
    bot_is_member: bool | None = None
    request_title: bool | None = None
    request_username: bool | None = None
    request_photo: bool | None = None


class KeyboardButtonRequestManagedBot(_BaseModel):
    request_id: int
    suggested_name: str | None = None
    suggested_username: str | None = None


class KeyboardButtonPollType(_BaseModel):
    type: str | None = None


class KeyboardButton(_BaseModel):
    text: str
    icon_custom_emoji_id: str | None = None
    style: str | None = None  # Must be one of "danger", "success" or "primary" or None
    request_users: KeyboardButtonRequestUsers | None = None
    request_chat: KeyboardButtonRequestChat | None = None
    request_managed_bot: KeyboardButtonRequestManagedBot | None = None
    request_contact: bool | None = None
    request_location: bool | None = None
    request_poll: KeyboardButtonPollType | None = None
    web_app: WebAppInfo | None = None


class ReplyKeyboardMarkup(_BaseModel):
    keyboard: list[list[KeyboardButton]]
    is_persistent: bool | None = None
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    input_field_placeholder: str | None = None
    selective: bool | None = None


class ReplyKeyboardRemove(_BaseModel):
    remove_keyboard: bool
    selective: bool | None = None


class SwitchInlineQueryChosenChat(_BaseModel):
    query: str | None = None
    allow_user_chats: bool | None = None
    allow_bot_chats: bool | None = None
    allow_group_chats: bool | None = None
    allow_channel_chats: bool | None = None


class LoginUrl(_BaseModel):
    url: str
    forward_text: str | None = None
    bot_username: str | None = None
    request_write_access: bool | None = None


class InlineKeyboardButton(_BaseModel):
    text: str
    icon_custom_emoji_id: str | None = None
    style: str | None = None  # Must be one of "danger", "success" or "primary" or None
    url: str | None = None
    callback_data: str | None = None
    web_app: WebAppInfo | None = None
    login_url: LoginUrl | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat | None = None
    copy_text: CopyTextButton | None = None
    callback_game: CallbackGame | None = None
    pay: bool | None = None


class InlineKeyboardMarkup(_BaseModel):
    inline_keyboard: list[list[InlineKeyboardButton]]


class InlineQueryResultsButton(_BaseModel):
    text: str
    web_app: WebAppInfo | None = None
    start_parameter: str | None = None

    @model_validator(mode="after")
    def validate_field_exists(self) -> InlineQueryResultsButton:
        if not self.web_app and not self.start_parameter:
            raise ValueError("Either 'web_app' or 'start_parameter' must be provided.")

        return self


class InlineQuery(_BaseModel):
    id: str
    from_user: User = Field(..., alias="from")
    query: str
    offset: str
    chat_type: str | None = None
    location: Location | None = None


class ChosenInlineResult(_BaseModel):
    result_id: str
    from_user: User = Field(..., alias="from")
    location: Location | None = None
    inline_message_id: str | None = None
    query: str


class InlineQueryResultArticle(_BaseModel):
    type: str = "article"
    id: str
    title: str
    input_message_content: InputMessageContent
    reply_markup: InlineKeyboardMarkup | None = None
    url: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultPhoto(_BaseModel):
    type: str = "photo"
    id: str
    photo_url: str
    thumbnail_url: str
    photo_width: int | None = None
    photo_height: int | None = None
    title: str | None = None
    description: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultGif(_BaseModel):
    type: str = "gif"
    id: str
    gif_url: str
    gif_width: int | None = None
    gif_height: int | None = None
    gif_duration: int | None = None
    thumbnail_url: str
    thumbnail_mime_type: str | None = None
    title: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultMpeg4Gif(_BaseModel):
    type: str = "mpeg4_gif"
    id: str
    mpeg4_url: str
    mpeg4_width: int | None = None
    mpeg4_height: int | None = None
    mpeg4_duration: int | None = None
    thumbnail_url: str
    thumbnail_mime_type: str | None = None
    title: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultVideo(_BaseModel):
    type: str = "video"
    id: str
    video_url: str
    mime_type: Literal["text/html", "video/mp4"]
    thumbnail_url: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    video_width: int | None = None
    video_height: int | None = None
    video_duration: int | None = None
    description: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None

    @model_validator(mode="before")
    def validate_content_exists_in_text_mime_type(self) -> InlineQueryResultVideo:
        if self.mime_type == "text/html" and not self.input_message_content:
            raise ValueError(
                "input_message_content is required when mime_type is 'text/html' (e.g., YouTube)"
            )

        return self


class InlineQueryResultAudio(_BaseModel):
    type: str = "audio"
    id: str
    audio_url: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    performer: str | None = None
    audio_duration: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultVoice(_BaseModel):
    type: str = "voice"
    id: str
    voice_url: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    voice_duration: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultDocument(_BaseModel):
    type: str = "document"
    id: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    document_url: str
    mime_type: Literal["application/pdf", "application/zip"]
    description: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultLocation(_BaseModel):
    type: str = "location"
    id: str
    latitude: float
    longitude: float
    title: str
    horizontal_accuracy: float | None = None
    live_period: int | None = None
    heading: int | None = None
    proximity_alert_radius: int | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultVenue(_BaseModel):
    type: str = "venue"
    id: str
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultContact(_BaseModel):
    type: str = "contact"
    id: str
    phone_number: str
    first_name: str
    last_name: str | None = None
    vcard: str | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None
    thumbnail_url: str | None = None
    thumbnail_width: int | None = None
    thumbnail_height: int | None = None


class InlineQueryResultGame(_BaseModel):
    type: str = "game"
    id: str
    game_short_name: str
    reply_markup: InlineKeyboardMarkup | None = None


class InlineQueryResultCachedPhoto(_BaseModel):
    type: str = "photo"
    id: str
    photo_file_id: str
    title: str | None = None
    description: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedGif(_BaseModel):
    type: str = "gif"
    id: str
    gif_file_id: str
    title: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedMpeg4Gif(_BaseModel):
    type: str = "mpeg4_gif"
    id: str
    mpeg4_file_id: str
    title: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedSticker(_BaseModel):
    type: str = "sticker"
    id: str
    sticker_file_id: str
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedDocument(_BaseModel):
    type: str = "document"
    id: str
    title: str
    document_file_id: str
    description: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedVideo(_BaseModel):
    type: str = "video"
    id: str
    video_file_id: str
    title: str
    description: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedVoice(_BaseModel):
    type: str = "voice"
    id: str
    voice_file_id: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class InlineQueryResultCachedAudio(_BaseModel):
    type: str = "audio"
    id: str
    audio_file_id: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None
    reply_markup: InlineKeyboardMarkup | None = None
    input_message_content: InputMessageContent | None = None


class AnswerInlineQuery(_BaseModel):
    inline_query_id: str
    results: list[InlineQueryResult]
    cache_time: int | None = 300
    is_personal: bool | None = None
    next_offset: str | None = None
    button: InlineQueryResultsButton | None = None


class CallbackQuery(_BaseModel):
    id: str
    from_user: User = Field(..., alias="from")
    message: MaybeInaccessibleMessage | None = None
    inline_message_id: str | None = None
    chat_instance: str
    data: str | None = None
    game_short_name: str | None = None


class ForceReply(_BaseModel):
    force_reply: bool
    input_field_placeholder: str | None = None
    selective: bool | None = None


class Birthdate(_BaseModel):
    day: int
    month: int
    year: int | None = None


class BusinessIntro(_BaseModel):
    title: str | None = None
    message: str | None = None
    sticker: Sticker | None = None


class BusinessLocation(_BaseModel):
    address: str
    location: Location | None = None


class BusinessOpeningHoursInterval(_BaseModel):
    opening_minute: int
    closing_minute: int


class BusinessOpeningHours(_BaseModel):
    time_zone_name: str
    opening_hours: list[BusinessOpeningHoursInterval]


class UserRating(_BaseModel):
    level: int
    rating: int
    current_level_rating: int
    next_level_rating: int | None = None


class StoryAreaPosition(_BaseModel):
    x_percentage: float
    y_percentage: float
    width_percentage: float
    height_percentage: float
    rotation_angle: float
    corner_radius_percentage: float


class LocationAddress(_BaseModel):
    country_code: str
    state: str | None = None
    city: str | None = None
    street: str | None = None


class ReactionTypeEmoji(_BaseModel):
    type: Literal["emoji"] = "emoji"
    emoji: str


class ReactionTypeCustomEmoji(_BaseModel):
    type: Literal["custom_emoji"] = "custom_emoji"
    custom_emoji_id: str


class ReactionTypePaid(_BaseModel):
    type: Literal["paid"] = "paid"


class ReactionCount(_BaseModel):
    type: ReactionType
    total_count: int


class StoryAreaTypeLocation(_BaseModel):
    type: Literal["location"] = "location"
    latitude: float
    longitude: float
    address: LocationAddress | None = None


class StoryAreaTypeSuggestedReaction(_BaseModel):
    type: Literal["suggested_reaction"] = "suggested_reaction"
    reaction_type: ReactionType
    is_dark: bool | None = None
    is_flipped: bool | None = None


class StoryAreaTypeLink(_BaseModel):
    type: Literal["link"] = "link"
    url: str


class StoryAreaTypeWeather(_BaseModel):
    type: Literal["weather"] = "weather"
    temperature: float
    emoji: str
    background_color: int


class StoryAreaTypeUniqueGift(_BaseModel):
    type: Literal["unique_gift"] = "unique_gift"
    name: str


class StoryArea(_BaseModel):
    position: StoryAreaPosition
    type: StoryAreaType


class MessageReactionUpdated(_BaseModel):
    chat: Chat
    message_id: int
    user: User | None = None
    actor_chat: Chat | None = None
    date: int
    old_reaction: list[ReactionType]
    new_reaction: list[ReactionType]


class MessageReactionCountUpdated(_BaseModel):
    chat: Chat
    message_id: int
    date: int
    reactions: list[ReactionCount]


class ForumTopic(_BaseModel):
    message_thread_id: int
    name: str
    icon_color: int
    icon_custom_emoji_id: str | None = None
    is_name_implicit: bool | None = None


class GiftBackground(_BaseModel):
    center_color: int
    edge_color: int
    text_color: int


class Gift(_BaseModel):
    id: str
    sticker: Sticker
    star_count: int
    upgrade_star_count: int | None = None
    is_premium: bool | None = None
    has_colors: bool | None = None
    total_count: int | None = None
    remaining_count: int | None = None
    personal_total_count: int | None = None
    personal_remaining_count: int | None = None
    background: GiftBackground | None = None
    unique_gift_variant_count: int | None = None
    publisher_chat: Chat | None = None


class Gifts(_BaseModel):
    gifts: list[Gift]


class UniqueGiftModel(_BaseModel):
    name: str
    sticker: Sticker
    rarity_per_mille: int
    rarity: str  # Currently, can be "uncommon", "rare", "epic", or "legendary".


class UniqueGiftSymbol(_BaseModel):
    name: str
    sticker: Sticker
    rarity_per_mille: int


class UniqueGiftBackdropColors(_BaseModel):
    center_color: int
    edge_color: int
    symbol_color: int
    text_color: int


class UniqueGiftBackdrop(_BaseModel):
    name: str
    colors: UniqueGiftBackdropColors
    rarity_per_mille: int


class UniqueGiftColors(_BaseModel):
    model_custom_emoji_id: str
    symbol_custom_emoji_id: str
    light_theme_main_color: int
    light_theme_other_colors: list[int]
    dark_theme_main_color: int
    dark_theme_other_colors: list[int]


class UniqueGift(_BaseModel):
    gift_id: str
    base_name: str
    name: str
    number: int
    model: UniqueGiftModel
    symbol: UniqueGiftSymbol
    backdrop: UniqueGiftBackdrop
    is_premium: bool | None = None
    is_burned: bool | None = None
    is_from_blockchain: bool | None = None
    colors: UniqueGiftColors | None = None
    publisher_chat: Chat | None = None


class GiftInfo(_BaseModel):
    gift: Gift
    owned_gift_id: str | None = None
    convert_star_count: int | None = None
    prepaid_upgrade_star_count: int | None = None
    is_upgrade_separate: bool | None = None
    can_be_upgraded: bool | None = None
    text: str | None = None
    entities: list[MessageEntity] | None = None
    is_private: bool | None = None
    unique_gift_number: int | None = None


class UniqueGiftInfo(_BaseModel):
    gift: UniqueGift
    origin: str
    last_resale_currency: str | None = None
    last_resale_amount: int | None = None
    owned_gift_id: str | None = None
    transfer_star_count: int | None = None
    next_transfer_date: int | None = None


class OwnedGiftRegular(_BaseModel):
    type: Literal["regular"] = "regular"
    gift: Gift
    owned_gift_id: str | None = None
    sender_user: User | None = None
    send_date: int
    text: str | None = None
    entities: list[MessageEntity] | None = None
    is_private: bool | None = None
    is_saved: bool | None = None
    can_be_upgraded: bool | None = None
    was_refunded: bool | None = None
    convert_star_count: int | None = None
    prepaid_upgrade_star_count: int | None = None
    is_upgrade_separate: bool | None = None
    unique_gift_number: int | None = None


class OwnedGiftUnique(_BaseModel):
    type: Literal["unique"] = "unique"
    gift: UniqueGift
    owned_gift_id: str | None = None
    sender_user: User | None = None
    send_date: int
    is_saved: bool | None = None
    can_be_transferred: bool | None = None
    transfer_star_count: int | None = None
    next_transfer_date: int | None = None


class OwnedGifts(_BaseModel):
    total_count: int
    gifts: list[OwnedGift]  # OwnedGift can be OwnedGiftRegular or OwnedGiftUnique
    next_offset: str | None = None


class BotAccessSettings(_BaseModel):
    is_access_restricted: bool
    added_users: list[User]


class AcceptedGiftTypes(_BaseModel):
    unlimited_gifts: bool
    limited_gifts: bool
    unique_gifts: bool
    premium_subscription: bool
    gifts_from_channels: bool


class BotCommand(_BaseModel):
    command: str
    description: str


class BotCommandScopeDefault(_BaseModel):
    type: Literal["default"] = "default"


class BotCommandScopeAllPrivateChats(_BaseModel):
    type: Literal["all_private_chats"] = "all_private_chats"


class BotCommandScopeAllGroupChats(_BaseModel):
    type: Literal["all_group_chats"] = "all_group_chats"


class BotCommandScopeAllChatAdministrators(_BaseModel):
    type: Literal["all_chat_administrators"] = "all_chat_administrators"


class BotCommandScopeChat(_BaseModel):
    type: Literal["chat"] = "chat"
    chat_id: int | str  # chat ID or @supergroupusername


class BotCommandScopeChatAdministrators(_BaseModel):
    type: Literal["chat_administrators"] = "chat_administrators"
    chat_id: int | str  # chat ID or @supergroupusername


class BotCommandScopeChatMember(_BaseModel):
    type: Literal["chat_member"] = "chat_member"
    chat_id: int | str  # chat ID or @supergroupusername
    user_id: int  # target user ID


class BotName(_BaseModel):
    name: str


class BotDescription(_BaseModel):
    description: str


class BotShortDescription(_BaseModel):
    short_description: str


class MenuButtonCommands(_BaseModel):
    type: Literal["commands"] = "commands"


class MenuButtonWebApp(_BaseModel):
    type: Literal["web_app"] = "web_app"
    text: str
    web_app: WebAppInfo  # description of the Web App to launch


class MenuButtonDefault(_BaseModel):
    type: Literal["default"] = "default"


class ChatBoostSourcePremium(_BaseModel):
    source: Literal["premium"] = "premium"
    user: User


class ChatBoostSourceGiftCode(_BaseModel):
    source: Literal["gift_code"] = "gift_code"
    user: User


class ChatBoostSourceGiveaway(_BaseModel):
    source: Literal["giveaway"] = "giveaway"
    giveaway_message_id: int
    user: User | None = None
    prize_star_count: int | None = None
    is_unclaimed: bool | None = None


class ChatBoost(_BaseModel):
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource


class ChatBoostUpdated(_BaseModel):
    chat: Chat
    boost: ChatBoost


class ChatBoostRemoved(_BaseModel):
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource


class ChatOwnerLeft(_BaseModel):
    new_owner: User | None = None


class ChatOwnerChanged(_BaseModel):
    new_owner: User


class UserChatBoosts(_BaseModel):
    boosts: list[ChatBoost]


class BusinessBotRights(_BaseModel):
    can_reply: bool | None = None
    can_read_messages: bool | None = None
    can_delete_sent_messages: bool | None = None
    can_delete_all_messages: bool | None = None
    can_edit_name: bool | None = None
    can_edit_bio: bool | None = None
    can_edit_profile_photo: bool | None = None
    can_edit_username: bool | None = None
    can_change_gift_settings: bool | None = None
    can_view_gifts_and_stars: bool | None = None
    can_convert_gifts_to_stars: bool | None = None
    can_transfer_and_upgrade_gifts: bool | None = None
    can_transfer_stars: bool | None = None
    can_manage_stories: bool | None = None


class BusinessConnection(_BaseModel):
    id: str
    user: User
    user_chat_id: int
    date: int
    rights: BusinessBotRights | None = None
    is_enabled: bool


class BusinessMessagesDeleted(_BaseModel):
    business_connection_id: str
    chat: Chat
    message_ids: list[int]


class PreparedKeyboardButton(_BaseModel):
    id: str


class ResponseParameters(_BaseModel):
    migrate_to_chat_id: int | None = None
    retry_after: int | None = None


class InputMediaLocation(_BaseModel):
    type: str
    latitude: float
    longitude: float
    horizontal_accuracy: float | None = None


class InputMediaPhoto(_BaseModel):
    type: Literal["photo"] = "photo"
    media: str
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: List[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    has_spoiler: bool | None = None


class InputMediaSticker(_BaseModel):
    type: str
    media: str
    emoji: str | None = None


class InputMediaVenue(_BaseModel):
    type: str
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None


class InputMediaVideo(_BaseModel):
    type: Literal["video"] = "video"
    media: str
    thumbnail: str | None = None
    cover: str | None = None
    start_timestamp: int | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: List[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    supports_streaming: bool | None = None
    has_spoiler: bool | None = None


class InputMediaAnimation(_BaseModel):
    type: Literal["animation"] = "animation"
    media: str
    thumbnail: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: List[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    has_spoiler: bool | None = None


class InputMediaLink(_BaseModel):
    type: str
    url: str


class InputMediaAudio(_BaseModel):
    type: Literal["audio"] = "audio"
    media: str
    thumbnail: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: List[MessageEntity] | None = None
    duration: int | None = None
    performer: str | None = None
    title: str | None = None


class InputMediaDocument(_BaseModel):
    type: Literal["document"] = "document"
    media: str
    thumbnail: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: List[MessageEntity] | None = None
    disable_content_type_detection: bool | None = None


class InputMediaLivePhoto(_BaseModel):
    type: str
    media: str
    photo: str | None = None
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: List[MessageEntity] | None = None
    show_caption_above_media: bool | None = None
    has_spoiler: bool | None = None


class InputFile(_BaseModel):
    pass


class InputPaidMediaLivePhoto(_BaseModel):
    type: Literal["live_photo"] = "live_photo"
    media: str
    photo: str


class InputPaidMediaPhoto(_BaseModel):
    type: Literal["photo"] = "photo"
    media: str


class InputPaidMediaVideo(_BaseModel):
    type: Literal["video"] = "video"
    media: str
    thumbnail: str | None = None
    cover: str | None = None
    start_timestamp: int | None = None
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    supports_streaming: bool | None = None


class InputProfilePhotoStatic:
    type: Literal["static"] = "static"
    photo: str


class InputProfilePhotoAnimated:
    type: Literal["animated"] = "animated"
    animation: str
    main_frame_timestamp: float = 0.0


class InputStoryContentPhoto:
    type: Literal["photo"] = "photo"
    photo: str  # "attach://<file_attach_name>" or file path


class InputStoryContentVideo:
    type: Literal["video"] = "video"
    video: str  # "attach://<file_attach_name>" or file path
    duration: float = 0.0  # optional, 0-60 seconds
    cover_frame_timestamp: float = 0.0  # optional, default 0.0
    is_animation: bool = False  # optional, True if no sound


class Invoice(_BaseModel):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class LabeledPrice(_BaseModel):
    label: str
    amount: int


class ShippingAddress(_BaseModel):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class ShippingQuery(_BaseModel):
    id: str
    from_user: User = Field(..., alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress


class ShippingOption(_BaseModel):
    id: str
    title: str
    prices: list[LabeledPrice]


class RefundedPayment(_BaseModel):
    currency: str  # ISO 4217 code, currently always "XTR"
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str
    provider_payment_charge_id: str | None = None


class OrderInfo(_BaseModel):
    name: str | None = None
    phone_number: str | None = None
    email: str | None = None
    shipping_address: ShippingAddress | None = None


class SuccessfulPayment(_BaseModel):
    currency: str
    total_amount: int
    invoice_payload: str
    subscription_expiration_date: int | None = None
    is_recurring: bool | None = None
    is_first_recurring: bool | None = None
    shipping_option_id: str | None = None
    order_info: OrderInfo | None = None
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class PassportElementErrorDataField(_BaseModel):
    source: Literal["data"] = "data"
    type: str  # "personal_details", "passport", "driver_license", "identity_card", "internal_passport", "address"
    field_name: str
    data_hash: str
    message: str


class PassportElementErrorFrontSide(_BaseModel):
    source: Literal["front_side"] = "front_side"
    type: str  # "passport", "driver_license", "identity_card", "internal_passport"
    file_hash: str
    message: str


class PassportElementErrorReverseSide(_BaseModel):
    source: Literal["reverse_side"] = "reverse_side"
    type: str  # "driver_license", "identity_card"
    file_hash: str
    message: str


class PassportElementErrorSelfie(_BaseModel):
    source: Literal["selfie"] = "selfie"
    type: str  # "passport", "driver_license", "identity_card", "internal_passport"
    file_hash: str
    message: str


class PassportElementErrorFile(_BaseModel):
    source: Literal["file"] = "file"
    type: str  # "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration"
    file_hash: str
    message: str


class PassportElementErrorFiles(_BaseModel):
    source: Literal["files"] = "files"
    type: str  # "utility_bill", "bank_statement", "rental_agreement", "passport_registration", "temporary_registration"
    file_hashes: list[str]
    message: str


class PassportElementErrorTranslationFile(_BaseModel):
    source: Literal["translation_file"] = "translation_file"
    type: str  # "passport", "driver_license", "identity_card", "internal_passport",
    # "utility_bill", "bank_statement", "rental_agreement",
    # "passport_registration", "temporary_registration"
    file_hash: str
    message: str


class PassportElementErrorTranslationFiles(_BaseModel):
    source: Literal["translation_files"] = "translation_files"
    type: str  # same as above
    file_hashes: list[str]
    message: str


class PassportElementErrorUnspecified(_BaseModel):
    source: Literal["unspecified"] = "unspecified"
    type: str
    element_hash: str
    message: str


class PreCheckoutQuery(_BaseModel):
    id: str
    from_user: User = Field(..., alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: str | None = None
    order_info: OrderInfo | None = None


class PaidMediaPurchased(_BaseModel):
    from_user: User = Field(..., alias="from")
    paid_media_payload: str


class RevenueWithdrawalStatePending(_BaseModel):
    type: Literal["pending"] = "pending"


class RevenueWithdrawalStateSucceeded(_BaseModel):
    type: Literal["succeeded"] = "succeeded"
    date: int
    url: str


class RevenueWithdrawalStateFailed(_BaseModel):
    type: Literal["failed"] = "failed"


class AffiliateInfo(_BaseModel):
    amount: int
    commission_per_mille: int
    affiliate_user: User | None = None
    affiliate_chat: User | None = None
    nanostar_amount: int | None = None


class TransactionPartnerUser(_BaseModel):
    type: Literal["user"] = "user"
    transaction_type: str  # "invoice_payment", "paid_media_payment", "gift_purchase", "premium_purchase", "business_account_transfer"
    user: User
    affiliate: AffiliateInfo | None = None
    invoice_payload: str | None = None
    subscription_period: int | None = None
    paid_media: list[PaidMedia] | None = None
    paid_media_payload: str | None = None
    gift: Gift | None = None
    premium_subscription_duration: int | None = None


class TransactionPartnerChat(_BaseModel):
    type: Literal["chat"] = "chat"
    chat: Chat
    gift: Gift | None = None


class TransactionPartnerAffiliateProgram(_BaseModel):
    type: Literal["affiliate_program"] = "affiliate_program"
    sponsor_user: User | None = None
    commission_per_mille: int


class TransactionPartnerFragment(_BaseModel):
    type: Literal["fragment"] = "fragment"
    withdrawal_state: RevenueWithdrawalState | None = None


class TransactionPartnerTelegramAds(_BaseModel):
    type: Literal["telegram_ads"] = "telegram_ads"


class TransactionPartnerTelegramApi(_BaseModel):
    type: Literal["telegram_api"] = "telegram_api"
    request_count: int


class TransactionPartnerOther(_BaseModel):
    type: Literal["other"] = "other"


class StarAmount(_BaseModel):
    amount: int
    nanostar_amount: int | None = None


class StarTransaction(_BaseModel):
    id: str
    amount: int
    nanostar_amount: int | None = None
    date: int
    source: TransactionPartner | None = None
    receiver: TransactionPartner | None = None


class StarTransactions(_BaseModel):
    offset: int | None = None
    limit: int | None = None


class SuggestedPostPrice(_BaseModel):
    currency: str
    amount: int


class SuggestedPostInfo(_BaseModel):
    state: str
    price: SuggestedPostPrice | None = None
    send_date: int | None = None


class SuggestedPostParameters(_BaseModel):
    price: SuggestedPostPrice | None = None
    send_date: int | None = None


class SuggestedPostApproved(_BaseModel):
    suggested_post_message: Message | None = None
    price: SuggestedPostPrice | None = None
    send_date: int


class SuggestedPostApprovalFailed(_BaseModel):
    suggested_post_message: Message | None = None
    price: SuggestedPostPrice


class SuggestedPostDeclined(_BaseModel):
    suggested_post_message: Message | None = None
    comment: str | None = None


class SuggestedPostPaid(_BaseModel):
    suggested_post_message: Message | None = None
    currency: str
    amount: int | None = None
    star_amount: StarAmount | None = None


class SuggestedPostRefunded(_BaseModel):
    suggested_post_message: Message | None = None
    reason: str


class PassportFile(_BaseModel):
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(_BaseModel):
    type: str
    data: str | None = None
    phone_number: str | None = None
    email: str | None = None
    files: list[PassportFile] | None = None
    front_side: PassportFile | None = None
    reverse_side: PassportFile | None = None
    selfie: PassportFile | None = None
    translation: list[PassportFile] | None = None
    hash: str


class EncryptedCredentials(_BaseModel):
    data: str
    hash: str
    secret: str


class PassportData(_BaseModel):
    data: list[EncryptedPassportElement]
    credentials: EncryptedCredentials


class InputTextMessageContent(_BaseModel):
    message_text: str
    parse_mode: str | None = None
    entities: list[MessageEntity] | None = None
    link_preview_options: LinkPreviewOptions | None = None


class InputRichMessageContent(_BaseModel):
    rich_message: InputRichMessage


class InputLocationMessageContent(_BaseModel):
    latitude: float
    longitude: float
    horizontal_accuracy: float | None = None
    live_period: int | None = None
    heading: int | None = None
    proximity_alert_radius: int | None = None


class InputVenueMessageContent(_BaseModel):
    latitude: float
    longitude: float
    title: str
    address: str
    foursquare_id: str | None = None
    foursquare_type: str | None = None
    google_place_id: str | None = None
    google_place_type: str | None = None


class InputContactMessageContent(_BaseModel):
    phone_number: str
    first_name: str
    last_name: str | None = None
    vcard: str | None = None


class InputInvoiceMessageContent(_BaseModel):
    title: str
    description: str
    payload: str
    provider_token: str | None = None
    currency: str
    prices: list[LabeledPrice]
    max_tip_amount: int | None = None
    suggested_tip_amounts: list[int] | None = None
    provider_data: str | None = None
    photo_url: str | None = None
    photo_size: int | None = None
    photo_width: int | None = None
    photo_height: int | None = None
    need_name: bool | None = None
    need_phone_number: bool | None = None
    need_email: bool | None = None
    need_shipping_address: bool | None = None
    send_phone_number_to_provider: bool | None = None
    send_email_to_provider: bool | None = None
    is_flexible: bool | None = None

    @model_validator(mode="after")
    def validate_xtr_currency_rules(self) -> InputInvoiceMessageContent:
        if self.currency == "XTR" and self.provider_token != "":
            raise ValueError(
                "For payments in Telegram Stars (XTR), provider_token must be an empty string."
            )
        return self


# ─── Discriminated Unions ──────────────────────────────────────
ChatMember = Annotated[
    ChatMemberOwner
    | ChatMemberAdministrator
    | ChatMemberMember
    | ChatMemberRestricted
    | ChatMemberLeft
    | ChatMemberBanned,
    Discriminator("status"),
]

ReactionType = Annotated[
    ReactionTypeEmoji | ReactionTypeCustomEmoji | ReactionTypePaid,
    Discriminator("type"),
]

MessageOrigin = Annotated[
    MessageOriginUser
    | MessageOriginHiddenUser
    | MessageOriginChat
    | MessageOriginChannel,
    Discriminator("type"),
]

StoryAreaType = Annotated[
    StoryAreaTypeLocation
    | StoryAreaTypeSuggestedReaction
    | StoryAreaTypeLink
    | StoryAreaTypeWeather
    | StoryAreaTypeUniqueGift,
    Discriminator("type"),
]

OwnedGift = Annotated[OwnedGiftRegular | OwnedGiftUnique, Discriminator("type")]

BotCommandScope = Annotated[
    BotCommandScopeDefault
    | BotCommandScopeAllPrivateChats
    | BotCommandScopeAllGroupChats
    | BotCommandScopeAllChatAdministrators
    | BotCommandScopeChat
    | BotCommandScopeChatAdministrators
    | BotCommandScopeChatMember,
    Discriminator("type"),
]

MenuButton = Annotated[
    MenuButtonCommands | MenuButtonWebApp | MenuButtonDefault,
    Discriminator("type"),
]

ChatBoostSource = Annotated[
    ChatBoostSourcePremium | ChatBoostSourceGiftCode | ChatBoostSourceGiveaway,
    Discriminator("source"),
]

InputMedia = Annotated[
    InputMediaAnimation
    | InputMediaAudio
    | InputMediaDocument
    | InputMediaLivePhoto
    | InputMediaPhoto
    | InputMediaVideo,
    Discriminator("type"),
]

InputPollMedia = Annotated[
    InputMediaAnimation
    | InputMediaAudio
    | InputMediaDocument
    | InputMediaLivePhoto
    | InputMediaLocation
    | InputMediaPhoto
    | InputMediaVenue
    | InputMediaVideo,
    Discriminator("type"),
]

InputPollOptionMedia = Annotated[
    InputMediaAnimation
    | InputMediaLink
    | InputMediaLivePhoto
    | InputMediaLocation
    | InputMediaPhoto
    | InputMediaSticker
    | InputMediaVenue
    | InputMediaVideo,
    Discriminator("type"),
]

InputPaidMedia = Annotated[
    InputPaidMediaPhoto | InputPaidMediaVideo, Discriminator("type")
]

InputProfilePhoto = Annotated[
    InputProfilePhotoStatic | InputProfilePhotoAnimated, Discriminator("type")
]

InputStoryContent = Annotated[
    InputStoryContentPhoto | InputStoryContentVideo, Discriminator("type")
]

RevenueWithdrawalState = Annotated[
    RevenueWithdrawalStatePending
    | RevenueWithdrawalStateSucceeded
    | RevenueWithdrawalStateFailed,
    Discriminator("type"),
]

TransactionPartner = Annotated[
    TransactionPartnerUser
    | TransactionPartnerChat
    | TransactionPartnerAffiliateProgram
    | TransactionPartnerFragment
    | TransactionPartnerTelegramAds
    | TransactionPartnerTelegramApi
    | TransactionPartnerOther,
    Discriminator("type"),
]

PassportElementError = Annotated[
    PassportElementErrorDataField
    | PassportElementErrorFrontSide
    | PassportElementErrorReverseSide
    | PassportElementErrorSelfie
    | PassportElementErrorFile
    | PassportElementErrorFiles
    | PassportElementErrorTranslationFile
    | PassportElementErrorTranslationFiles
    | PassportElementErrorUnspecified,
    Discriminator("source"),
]


# ─── Simple Unions ─────────────────────────────────────────────
InlineQueryResult = (
    InlineQueryResultArticle
    | InlineQueryResultPhoto
    | InlineQueryResultGif
    | InlineQueryResultMpeg4Gif
    | InlineQueryResultVideo
    | InlineQueryResultAudio
    | InlineQueryResultVoice
    | InlineQueryResultDocument
    | InlineQueryResultLocation
    | InlineQueryResultVenue
    | InlineQueryResultContact
    | InlineQueryResultGame
    | InlineQueryResultCachedPhoto
    | InlineQueryResultCachedGif
    | InlineQueryResultCachedMpeg4Gif
    | InlineQueryResultCachedSticker
    | InlineQueryResultCachedDocument
    | InlineQueryResultCachedVideo
    | InlineQueryResultCachedVoice
    | InlineQueryResultCachedAudio
)

ReplyMarkup = (
    InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply
)

InputMessageContent = (
    InputTextMessageContent
    | InputRichMessageContent
    | InputLocationMessageContent
    | InputVenueMessageContent
    | InputContactMessageContent
    | InputInvoiceMessageContent
)

MaybeInaccessibleMessage = Message | InaccessibleMessage

RichText = (
    RichTextBold
    | RichTextItalic
    | RichTextUnderline
    | RichTextStrikethrough
    | RichTextSpoiler
    | RichTextDateTime
    | RichTextTextMention
    | RichTextSubscript
    | RichTextSuperscript
    | RichTextMarked
    | RichTextCode
    | RichTextCustomEmoji
    | RichTextMathematicalExpression
    | RichTextUrl
    | RichTextEmailAddress
    | RichTextPhoneNumber
    | RichTextBankCardNumber
    | RichTextMention
    | RichTextHashtag
    | RichTextCashtag
    | RichTextBotCommand
    | RichTextAnchor
    | RichTextAnchorLink
    | RichTextReference
    | RichTextReferenceLink
)

RichBlock = (
    RichBlockParagraph
    | RichBlockSectionHeading
    | RichBlockPreformatted
    | RichBlockFooter
    | RichBlockDivider
    | RichBlockMathematicalExpression
    | RichBlockAnchor
    | RichBlockList
    | RichBlockBlockQuotation
    | RichBlockPullQuotation
    | RichBlockCollage
    | RichBlockSlideshow
    | RichBlockTable
    | RichBlockDetails
    | RichBlockMap
    | RichBlockAnimation
    | RichBlockAudio
    | RichBlockPhoto
    | RichBlockVideo
    | RichBlockVoiceNote
    | RichBlockThinking
)

# ─── Type Adapters ─────────────────────────────────────────────
MessageIdList = TypeAdapter(List[MessageId])
StickerList = TypeAdapter(List[Sticker])
BotCommandList = TypeAdapter(List[BotCommand])
ChatMemberAdapter = TypeAdapter(ChatMember)
OwnedGiftAdapter = TypeAdapter(OwnedGift)
MenuButtonAdapter = TypeAdapter(MenuButton)
MessageListAdapter = TypeAdapter(list[Message])


# Resolve forward references
Update.model_rebuild()
ChatFullInfo.model_rebuild()
Message.model_rebuild()
ExternalReplyInfo.model_rebuild()
SentWebAppMessage.model_rebuild()
InlineQueryResultArticle.model_rebuild()
InlineQueryResultPhoto.model_rebuild()
InlineQueryResultGif.model_rebuild()
InlineQueryResultMpeg4Gif.model_rebuild()
InlineQueryResultVideo.model_rebuild()
InlineQueryResultAudio.model_rebuild()
InlineQueryResultVoice.model_rebuild()
InlineQueryResultDocument.model_rebuild()
InlineQueryResultLocation.model_rebuild()
InlineQueryResultVenue.model_rebuild()
InlineQueryResultContact.model_rebuild()
InlineQueryResultCachedPhoto.model_rebuild()
InlineQueryResultCachedGif.model_rebuild()
InlineQueryResultCachedMpeg4Gif.model_rebuild()
InlineQueryResultCachedSticker.model_rebuild()
InlineQueryResultCachedDocument.model_rebuild()
InlineQueryResultCachedVideo.model_rebuild()
InlineQueryResultCachedVoice.model_rebuild()
InlineQueryResultCachedAudio.model_rebuild()
AnswerInlineQuery.model_rebuild()
CallbackQuery.model_rebuild()
ChatMemberUpdated.model_rebuild()
ReactionCount.model_rebuild()
StoryAreaTypeSuggestedReaction.model_rebuild()
StoryArea.model_rebuild()
MessageReactionUpdated.model_rebuild()
OwnedGifts.model_rebuild()
ChatBoost.model_rebuild()
ChatBoostRemoved.model_rebuild()
TransactionPartnerFragment.model_rebuild()
StarTransaction.model_rebuild()
