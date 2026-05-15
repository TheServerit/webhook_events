from typing import TypedDict, NotRequired, TYPE_CHECKING

from .enums import try_enum, ChannelType, MessageType, MessageActivityType, MessageReferenceType, InteractionType, PollLayoutType, BaseThemeType
from .user import User, UserData, WebhookUser, WebhookUserData, Collectibles, CollectiblesData, AvatarDecoration, AvatarDecorationData
from .components import resolve_message_component, MessageComponentType, MessageComponentData, UnknownComponent, ComponentsWrapper
from .application import Application, ApplicationData, PartialApplication, PartialApplicationData
from .channel import Channel, ChannelData, PartialChannel, PartialChannelData
from .sticker import Sticker, PartialSticker, PartialStickerData
from .flags import MessageFlags, AttachmentFlags, MemberFlags
from .emoji import PartialEmoji, PartialEmojiData
from .embed import Embed, EmbedData
from .abc import Snowflake
from .color import Color
from .role import Role
from .cdn import Asset

from ..utils import iso_to_datetime

if TYPE_CHECKING:
    from .sticker import StickerData
    from .role import RoleData


__all__ = (
    "ChannelMention",
    "Attachment",
    "ReactionCountDetails",
    "Reaction",
    "MessageActivity",
    "MessageReference",
    "PartialMessage",
    "MessageSnapshot",
    "InteractionMetadata",
    "RoleSubscriptionData",
    "PartialMember",
    "Resolved",
    "PollMedia",
    "PollAnswer",
    "PollAnswerCounts",
    "PollResults",
    "Poll",
    "MessageCall",
    "SharedClientTheme",
    "Message",
)


class ChannelMentionData(TypedDict):
    id: str
    guild_id: str
    type: int
    name: str


class AttachmentData(TypedDict):
    id: str
    filename: str
    title: NotRequired[str]
    description: NotRequired[str]
    content_type: NotRequired[str]
    size: int
    url: str
    proxy_url: str
    height: NotRequired[int | None]
    width: NotRequired[int | None]
    placeholder: NotRequired[str]
    placeholder_version: NotRequired[int]
    ephemeral: NotRequired[bool]
    duration_secs: NotRequired[float]
    waveform: NotRequired[str]
    flags: NotRequired[int]
    clip_participants: NotRequired[list[UserData]]
    clip_created_at: NotRequired[str]
    application: NotRequired[ApplicationData | None]


class ReactionCountDetailsData(TypedDict):
    burst: int
    normal: int


class ReactionData(TypedDict):
    count: int
    count_details: ReactionCountDetailsData
    me: bool
    me_burst: bool
    emoji: PartialEmojiData
    burst_colors: list[str]


class MessageActivityData(TypedDict):
    type: int
    party_id: NotRequired[str]


class MessageReferenceData(TypedDict, total=False):
    type: int
    message_id: str
    channel_id: str
    guild_id: str
    fail_if_not_exists: bool


class PartialMessageData(TypedDict):
    type: int
    content: str
    embeds: list[EmbedData]
    attachments: list[AttachmentData]
    timestamp: str
    edited_timestamp: str | None
    flags: int
    mentions: list[UserData]
    mention_roles: list[str]
    stickers: list[StickerData]
    sticker_items: list[PartialStickerData]
    components: list[MessageComponentData]


class MessageSnapshotData(TypedDict):
    message: PartialMessageData


class MessageInteractionMetadataData(TypedDict):
    id: str
    type: int
    user: UserData
    authorizing_integration_owners: dict[str, str]
    original_response_message_id: NotRequired[str]
    target_user: NotRequired[UserData]
    target_message_id: NotRequired[str]


class StickerItemData(TypedDict):
    id: str
    name: str
    format_type: int


class RoleSubscriptionDataData(TypedDict):
    role_subscription_listing_id: str
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool


class ResolvedData(TypedDict, total=False):
    users: dict[str, UserData]
    members: dict[str, PartialMemberData]
    roles: dict[str, RoleData]
    channels: dict[str, PartialChannelData]
    messages: dict[str, PartialMessageData]
    attachments: dict[str, AttachmentData]


class PollMediaData(TypedDict):
    text: NotRequired[str | None]
    emoji: NotRequired[PartialEmojiData | None]


class PollAnswerData(TypedDict):
    answer_id: str
    poll_media: PollMediaData


class PollAnswerCountData(TypedDict):
    id: int
    count: int
    me_voted: bool


class PollResultsData(TypedDict):
    is_finalized: bool
    answer_counts: list[PollAnswerCountData]


class PollData(TypedDict):
    question: PollMediaData
    answers: list[PollAnswerData]
    expiry: str | None
    allow_multiselect: bool
    layout_type: int
    results: NotRequired[PollResultsData]


class MessageCallData(TypedDict):
    participants: list[str]
    ended_timestamp: NotRequired[str | None]


class SharedClientThemeData(TypedDict):
    colors: list[str]
    gradient_angle: int
    base_mix: int
    base_theme: NotRequired[int]


class PartialMemberData(TypedDict):
    nick: NotRequired[str | None]
    avatar: NotRequired[str | None]
    banner: NotRequired[str | None]
    roles: list[str]
    joined_at: NotRequired[str]
    premium_since: NotRequired[str | None]
    flags: int
    pending: NotRequired[bool]
    permissions: NotRequired[str]
    communication_disabled_until: NotRequired[str | None]
    avatar_decoration_data: NotRequired[AvatarDecorationData | None]
    collectibles: NotRequired[CollectiblesData | None]


class MessageData(TypedDict): 
    id: str
    channel_id: str
    author: UserData | WebhookUserData
    content: str
    timestamp: str
    edited_timestamp: str | None
    tts: bool
    mention_everyone: bool
    mentions: list[UserData]
    mention_roles: list[str]
    mention_channels: NotRequired[list[ChannelMentionData]]
    attachments: list[AttachmentData]
    embeds: list[EmbedData]
    reactions: NotRequired[list[ReactionData]]
    nonce: NotRequired[str | int]
    pinned: bool
    webhook_id: NotRequired[str]
    type: int
    activity: NotRequired[MessageActivityData]
    application: NotRequired[PartialApplicationData]
    application_id: NotRequired[str]
    flags: NotRequired[int]
    message_reference: NotRequired[MessageReferenceData]
    message_snapshots: NotRequired[list[MessageSnapshotData]]
    referenced_message: NotRequired[MessageData | None]
    interaction_metadata: NotRequired[MessageInteractionMetadataData]
    thread: NotRequired[ChannelData]
    components: NotRequired[list[MessageComponentData]]
    sticker_items: NotRequired[list[StickerItemData]]
    stickers: NotRequired[list[StickerData]]
    position: NotRequired[int]
    role_subscription_data: NotRequired[RoleSubscriptionDataData]
    resolved: NotRequired[ResolvedData]
    poll: NotRequired[PollData]
    call: NotRequired[MessageCallData]

    lobby_id: NotRequired[str]
    channel: ChannelData


class ChannelMention(Snowflake):
    __slots__ = ("id", "guild_id", "type", "name")

    def __init__(self, data: ChannelMentionData) -> None:
        self.id = int(data["id"])
        self.guild_id = int(data["guild_id"])
        self.type = try_enum(ChannelType, data["type"])
        self.name = data["name"]


class Attachment(Snowflake):
    __slots__ = (
        "id",
        "filename",
        "title",
        "description",
        "content_type",
        "size",
        "url",
        "proxy_url",
        "height",
        "width",
        "thumbhash_placeholder",
        "thumbhash_placeholder_version",
        "is_ephemeral",
        "duration_secs",
        "waveform",
        "flags",
        "clip_participants",
        "clip_created_at",
        "application",
    )

    def __init__(self, data: AttachmentData) -> None:
        self.id = int(data["id"])
        self.filename = data["filename"]
        self.title = data.get("title")
        self.description = data.get("description")
        self.content_type = data.get("content_type")
        self.size = data["size"]
        self.url = data["url"]
        self.proxy_url = data["proxy_url"]
        self.height = data.get("height")
        self.width = data.get("width")
        self.thumbhash_placeholder = data.get("placeholder")
        self.thumbhash_placeholder_version = data.get("placeholder_version")
        self.is_ephemeral = bool(data.get("ephemeral"))
        self.duration_secs = data.get("duration_secs")
        self.waveform = data.get("waveform")
        self.flags = AttachmentFlags(data.get("flags", 0))
        self.clip_participants = [User(user) for user in data.get("clip_participants", [])]
        self.clip_created_at = iso_to_datetime(clip_created_at) if (clip_created_at := data.get("clip_created_at")) else None
        self.application = Application(application) if (application := data.get("application")) else None


class ReactionCountDetails:
    __slots__ = ("super_reactions", "normal_reactions")

    def __init__(self, data: ReactionCountDetailsData) -> None:
        self.super_reactions = data["burst"]
        self.normal_reactions = data["normal"]


class Reaction:
    __slots__ = (
        "count",
        "count_details",
        "me_reacted",
        "me_super_reacted",
        "emoji",
        "super_reaction_colors",
    )

    def __init__(self, data: ReactionData) -> None:
        self.count = data["count"]
        self.count_details = ReactionCountDetails(data["count_details"])
        self.me_reacted = data["me"]
        self.me_super_reacted = data["me_burst"]
        self.emoji = PartialEmoji(data["emoji"])
        self.super_reaction_colors = [Color.from_hex(color) for color in data.get("burst_colors", [])]


class MessageActivity:
    __slots__ = ("type", "party_id")

    def __init__(self, data: MessageActivityData) -> None:
        self.type = try_enum(MessageActivityType, data["type"])
        self.party_id = data.get("party_id")


class MessageReference(Snowflake):
    __slots__ = (
        "type",
        "message_id",
        "channel_id",
        "guild_id"
    )

    def __init__(self, data: MessageReferenceData) -> None:
        self.type = try_enum(MessageReferenceType, reference_type) if (reference_type := data.get("type")) else MessageReferenceType.DEFAULT
        self.message_id = int(message_id) if (message_id := data.get("message_id")) else None
        self.channel_id = int(channel_id) if (channel_id := data.get("channel_id")) else None
        self.guild_id = int(guild_id) if (guild_id := data.get("guild_id")) else None


class PartialMessage:
    __slots__ = (
        "type",
        "content",
        "embeds",
        "attachments",
        "sent_at",
        "edited_at",
        "flags",
        "mentioned_users",
        "mentioned_roles",
        "stickers",
        "sticker_items",
        "components",
    )
    
    def __init__(self, data: PartialMessageData) -> None:
        self.type = try_enum(MessageType, data["type"])
        self.content = data["content"]
        self.embeds = [Embed(embed) for embed in data["embeds"]]
        self.attachments = [Attachment(attachment) for attachment in data["attachments"]]
        self.sent_at = iso_to_datetime(data["timestamp"])
        self.edited_at = iso_to_datetime(edited_timestamp) if (edited_timestamp := data["edited_timestamp"]) else None
        self.flags = MessageFlags(data["flags"])
        self.mentioned_users = [User(user) for user in data["mentions"]]
        self.mentioned_roles = [int(role_id) for role_id in data["mention_roles"]]
        self.stickers = [Sticker(sticker) for sticker in data["stickers"]]
        self.sticker_items = [PartialSticker(partial_sticker) for partial_sticker in data["sticker_items"]]
        self.components: list[MessageComponentType | UnknownComponent] = [resolve_message_component(component) for component in data.get("components", [])]

    def build_components_wrapper(self) -> ComponentsWrapper:
        """Resolves the message's components into a `types.ComponentsWrapper` for accessibility."""
        return ComponentsWrapper._from_message_components(self.components) # pyright: ignore[reportPrivateUsage]


class MessageSnapshot:
    __slots__ = ("message",)

    def __init__(self, data: MessageSnapshotData) -> None:
        self.message = PartialMessage(data["message"])


class InteractionMetadata:
    __slots__ = (
        "id",
        "type",
        "user",
        "integration_guild_id",
        "integration_user_id",
        "original_response_message_id",
        "target_user",
        "target_message_id",
    )

    def __init__(self, data: MessageInteractionMetadataData) -> None:
        self.id = int(data["id"])
        self.type = try_enum(InteractionType, data["type"])
        self.user = User(data["user"])

        authorizing_integration_owners = data["authorizing_integration_owners"]
        self.integration_guild_id = authorizing_integration_owners["0"]
        self.integration_user_id = authorizing_integration_owners["1"]

        self.original_response_message_id = int(og_response_msg_id) if (og_response_msg_id := data.get("original_response_message_id")) else None
        self.target_user = User(target_user) if (target_user := data.get("target_user")) else None
        self.target_message_id = int(target_msg_id) if (target_msg_id := data.get("target_message_id")) else None


class RoleSubscriptionData:
    __slots__ = (
        "role_subscription_listing_id",
        "tier_name",
        "total_months_subscribed",
        "is_renewal"
    )

    def __init__(self, data: RoleSubscriptionDataData) -> None:
        self.role_subscription_listing_id = int(data["role_subscription_listing_id"])
        self.tier_name = data["tier_name"]
        self.total_months_subscribed = data["total_months_subscribed"]
        self.is_renewal = data["is_renewal"]


class PartialMember:
    __slots__ = (
        "nick",
        "avatar",
        "banner",
        "roles",
        "joined_at",
        "boosting_since",
        "flags",
        "is_pending",
        "permissions",
        "timed_out_until",
        "avatar_decoration",
        "collectibles"
    )

    def __init__(self, data: PartialMemberData, member_id: int) -> None:
        self.nick = data.get("nick")
        self.avatar = Asset(avatar, member_id, "avatars") if (avatar := data.get("avatar")) else None
        self.banner = Asset(banner, member_id, "banners") if (banner := data.get("banner")) else None
        self.roles = [int(role_id) for role_id in data["roles"]]
        self.joined_at = iso_to_datetime(joined_at) if (joined_at := data.get("joined_at")) else None
        self.boosting_since = iso_to_datetime(premium_since) if (premium_since := data.get("premium_since")) else None
        self.flags = MemberFlags(data["flags"])
        self.is_pending = data.get("pending", False)
        self.permissions = int(data.get("permissions", 0))
        self.timed_out_until = iso_to_datetime(comms_disabled_until) if (comms_disabled_until := data.get("communication_disabled_until")) else None
        self.avatar_decoration= AvatarDecoration(avatar_decoration) if (avatar_decoration := data.get("avatar_decoration")) else None
        self.collectibles = Collectibles(collectibles) if (collectibles := data.get("collectibles")) else None


class Resolved:
    __slots__ = (
        "users_map",
        "members_map",
        "roles_map",
        "channels_map",
        "messages_map",
        "attachments_map"
    )

    def __init__(self, data: ResolvedData) -> None:
        users_map: dict[int, User] = {}
        for str_id, user in data.get("users", {}).items():
            users_map[int(str_id)] = User(user)
        self.users_map = users_map

        members_map: dict[int, PartialMember] = {}
        for str_id, member in data.get("members", {}).items():
            int_id = int(str_id)
            members_map[int_id] = PartialMember(member, int_id)
        self.members_map = members_map

        roles_map: dict[int, Role] = {}
        for str_id, role in data.get("roles", {}).items():
            roles_map[int(str_id)] = Role(role)
        self.roles_map = roles_map

        channels_map: dict[int, PartialChannel] = {}
        for str_id, channel in data.get("channels", {}).items():
            channels_map[int(str_id)] = PartialChannel(channel)
        self.channels_map = channels_map

        messages_map: dict[int, PartialMessage] = {}
        for str_id, message in data.get("messages", {}).items():
            messages_map[int(str_id)] = PartialMessage(message)
        self.messages_map = messages_map

        attachments_map: dict[int, Attachment] = {}
        for str_id, attachment in data.get("attachments", {}).items():
            attachments_map[int(str_id)] = Attachment(attachment)
        self.attachments_map = attachments_map


class PollMedia:
    __slots__ = ("text", "emoji")

    def __init__(self, data: PollMediaData) -> None:
        self.text = data.get("text")
        self.emoji = PartialEmoji(emoji) if (emoji := data.get("emoji")) else None


class PollAnswer:
    __slots__ = ("answer_id", "poll_media")

    def __init__(self, data: PollAnswerData) -> None:
        self.answer_id: int
        self.poll_media = PollMedia(data["poll_media"])


class PollAnswerCounts:
    __slots__ = ("id", "count", "me_voted")

    def __init__(self, data: PollAnswerCountData) -> None:
        self.id = data["id"]
        self.count = data["count"]
        self.me_voted = data["me_voted"]


class PollResults:
    __slots__ = ("is_finalized", "answer_counts")

    def __init__(self, data: PollResultsData) -> None:
        self.is_finalized = data["is_finalized"]
        self.answer_counts = [PollAnswerCounts(answer_count) for answer_count in data["answer_counts"]]


class Poll:
    __slots__ = (
        "question",
        "answers",
        "ends_at",
        "allows_multiselect",
        "layout_type",
        "results"
    )

    def __init__(self, data: PollData) -> None:
        self.question = PollMedia(data["question"])
        self.answers = [PollAnswer(answer) for answer in data["answers"]]
        self.ends_at = iso_to_datetime(expiry) if (expiry := data["expiry"]) else None
        self.allows_multiselect = data["allow_multiselect"]
        self.layout_type = try_enum(PollLayoutType, data["layout_type"])
        self.results = PollResults(results) if (results := data.get("results")) else None


class MessageCall:
    __slots__ = ("participants", "ended_at")

    def __init__(self, data: MessageCallData) -> None:
        self.participants = data["participants"]
        self.ended_at = iso_to_datetime(ended_ts) if (ended_ts := data.get("ended_timestamp")) else None


class SharedClientTheme:
    __slots__ = (
        "colors",
        "gradient_angle",
        "base_mix",
        "base_theme_type"
    )

    def __init__(self, data: SharedClientThemeData) -> None:
        self.colors = [Color.from_hex(color) for color in data["colors"]]
        self.gradient_angle = data["gradient_angle"]
        self.base_mix = data["base_mix"]
        self.base_theme_type = try_enum(BaseThemeType, base_theme) if (base_theme := data.get("base_theme")) else None


class Message(Snowflake):
    """
    The standard Discord message object, **with 2 additional fields**:

    `lobby_id`: ID of the lobby where the message was created (only present in Linked Channel messages).

    `channel`: Channel object with recipient information.
    """

    __slots__ = (
        "id",
        "channel_id",
        "author",
        "content",
        "sent_at",
        "edited_at",
        "is_tts",
        "mentions_everyone",
        "mentioned_users",
        "mention_roles",
        "mentioned_channels",
        "attachments",
        "embeds",
        "reactions",
        "nonce",
        "pinned",
        "webhook_id",
        "type",
        "activity",
        "application",
        "application_id",
        "flags",
        "message_reference",
        "message_snapshots",
        "referenced_message",
        "interaction_metadata",
        "thread",
        "components",
        "sticker_items",
        "stickers",
        "position",
        "role_subscription_data",
        "resolved",
        "poll",
        "call",
        "shared_client_theme",

        "lobby_id",
        "channel"
    )

    def __init__(self, data: MessageData) -> None:
        self.id = int(data["id"])
        self.channel_id = int(data["channel_id"])
        self.webhook_id = int(webhook_id) if (webhook_id := data.get("webhook_id")) else None

        author = data["author"]
        self.author = WebhookUser(author) if self.webhook_id is None else User(author) # pyright: ignore[reportArgumentType]

        self.content = data["content"]
        self.sent_at = iso_to_datetime(data["timestamp"])
        self.edited_at = iso_to_datetime(edited_timestamp) if (edited_timestamp := data["edited_timestamp"]) else None
        self.is_tts = data["tts"]
        self.mentions_everyone = data["mention_everyone"]
        self.mentioned_users = [User(user) for user in data["mentions"]]
        self.mentioned_roles = [int(role_id) for role_id in data["mention_roles"]]
        self.mentioned_channels = [ChannelMention(channel) for channel in data.get("mention_channels", [])]
        self.attachments = [Attachment(attachment) for attachment in data["attachments"]]
        self.embeds = [Embed(embed) for embed in data["embeds"]]
        self.reactions = [Reaction(reaction) for reaction in data.get("reactions", [])]
        self.nonce = data.get("nonce")
        self.is_pinned = data["pinned"]
        self.type = try_enum(MessageType, data["type"])
        self.activity = MessageActivity(activity) if (activity := data.get("activity")) else None
        self.application = PartialApplication(application) if (application := data.get("application")) else None
        self.application_id = int(application_id) if (application_id := data.get("application_id")) else None
        self.flags = MessageFlags(data.get("flags", 0))
        self.message_reference = MessageReference(reference) if (reference := data.get("message_reference")) else None
        self.message_snapshots = [MessageSnapshot(snapshot) for snapshot in data.get("message_snapshots", [])]
        self.referenced_message = Message(message) if (message := data.get("referenced_message")) else None
        self.interaction_metadata = InteractionMetadata(metadata) if (metadata := data.get("interaction_metadata")) else None
        self.thread = Channel(thread) if (thread := data.get("thread")) else None
        self.components: list[MessageComponentType | UnknownComponent] = [resolve_message_component(component) for component in data.get("components", [])]
        self.sticker_items = [PartialSticker(partial_sticker) for partial_sticker in data.get("sticker_items", [])]
        self.stickers = [Sticker(sticker) for sticker in data.get("stickers", [])]
        self.position = data.get("position")
        self.role_subscription_data = RoleSubscriptionData(role_subscription_data) if (role_subscription_data := data.get("role_subscription_data")) else None
        self.resolved = Resolved(resolved) if (resolved := data.get("resolved")) else None
        self.poll = Poll(poll) if (poll := data.get("poll")) else None
        self.call = MessageCall(call) if (call := data.get("call")) else None
        self.shared_client_theme = SharedClientTheme(theme) if (theme := data.get("shared_client_theme")) else None

        self.lobby_id = int(lobby_id) if (lobby_id := data.get("lobby_id")) else None
        self.channel = Channel(data["channel"])

    def build_components_wrapper(self) -> ComponentsWrapper:
        """Resolves the message's components into a `types.ComponentsWrapper` for accessibility."""
        return ComponentsWrapper._from_message_components(self.components) # pyright: ignore[reportPrivateUsage]
