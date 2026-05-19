from typing import TypedDict, NotRequired

from .enums import try_enum, ChannelType, PermissionOverwriteType, ChannelVideoQualityMode, ChannelSortOrderType, ForumLayoutType
from .abc import MentionableSnowflake
from .user import User, UserData
from .flags import ChannelFlags
from .cdn import Asset

from ..utils import iso_to_datetime


__all__ = (
    "Channel",
    "PartialChannel",
    "ThreadMetadata",
    "PermissionOverwrite",
    "ThreadMember",
    "ForumTag",
    "DefaultReaction"
)


class PartialChannelData(TypedDict):
    id: str
    name: NotRequired[str | None]
    type: int
    permissions: NotRequired[str]
    last_message_id: NotRequired[str | None]
    last_pin_timestamp: NotRequired[str | None]
    nsfw: NotRequired[bool]
    parent_id: NotRequired[str | None]
    guild_id: NotRequired[str]
    flags: NotRequired[int]
    rate_limit_per_user: NotRequired[int]
    topic: NotRequired[str | None]
    position: NotRequired[int]

    thread_metadata: NotRequired[ThreadMetadataData] # Threads will also have the thread_metadata field


class ThreadMetadataData(TypedDict):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: NotRequired[bool]
    create_timestamp: NotRequired[str | None]


class OverwriteData(TypedDict):
    id: str
    type: int
    allow: str
    deny: str


class ThreadMemberData(TypedDict):
    id: str
    user_id: str
    join_timestamp: str
    flags: int


class ForumTagData(TypedDict):
    id: str
    name: str
    moderated: bool
    emoji_id: str | None
    emoji_name: str | None


class DefaultReactionData(TypedDict):
    emoji_id: str | None
    emoji_name: str | None


class ChannelData(PartialChannelData):
    permission_overwrites: NotRequired[list[OverwriteData]]
    bitrate: NotRequired[int]
    user_limit: NotRequired[int]
    recipients: list[UserData]
    icon: NotRequired[str | None]
    owner_id: NotRequired[str]
    application_id: NotRequired[str]
    managed: NotRequired[bool]
    rtc_region: NotRequired[str | None]
    video_quality_mode: NotRequired[int]
    message_count: NotRequired[int]
    member_count: NotRequired[int]
    member: NotRequired[ThreadMemberData]
    default_auto_archive_duration: NotRequired[int]
    total_message_sent: NotRequired[int]
    available_tags: NotRequired[list[ForumTagData]]
    applied_tags: NotRequired[list[str]]
    default_reaction_emoji: NotRequired[DefaultReactionData | None]
    default_thread_rate_limit_per_user: NotRequired[int]
    default_sort_order: NotRequired[int | None]
    default_forum_layout: NotRequired[int]


class ThreadMetadata:
    __slots__ = (
        "is_archived",
        "auto_archive_duration",
        "archive_timestamp",
        "is_locked",
        "is_invitable",
        "create_timestamp"
    )

    def __init__(self, data: ThreadMetadataData) -> None:
        self.is_archived = data["archived"]
        self.auto_archive_duration = data["auto_archive_duration"]
        self.archive_timestamp = data["archive_timestamp"]
        self.is_locked = data["locked"]
        self.is_invitable = data.get("invitable")
        self.create_timestamp = iso_to_datetime(create_ts) if (create_ts := data.get("create_timestamp")) else None


class PermissionOverwrite:
    __slots__ = ("id", "type", "allow", "deny")

    def __init__(self, data: OverwriteData) -> None:
        self.id = int(data["id"])
        self.type = try_enum(PermissionOverwriteType, data["type"])
        self.allow = int(data["allow"])
        self.deny = int(data["deny"])


class PartialChannel(MentionableSnowflake):
    __slots__ = (
        "id",
        "name",
        "type",
        "permissions",
        "last_message_id",
        "last_pin_timestamp",
        "is_nsfw",
        "parent_id",
        "guild_id",
        "flags",
        "rate_limit_per_user",
        "topic",
        "position",
        "thread_metadata"
    )

    def __init__(self, data: PartialChannelData) -> None:
        self.id = int(data["id"])
        self.name = data.get("name")
        self.type = try_enum(ChannelType, data["type"])
        self.permissions = int(data.get("permissions", 0))
        self.last_message_id = int(last_id) if (last_id := data.get("last_message_id")) else None
        self.last_pin_timestamp = iso_to_datetime(last_pin_ts) if (last_pin_ts := data.get("last_pin_timestamp")) else None
        self.is_nsfw = data.get("nsfw", False) or False
        self.parent_id = int(parent_id) if (parent_id := data.get("parent_id")) else None
        self.guild_id = int(guild_id) if (guild_id := data.get("guild_id")) else None
        self.flags = ChannelFlags(data.get("flags", 0))
        self.rate_limit_per_user = data.get("rate_limit_per_user")
        self.topic = data.get("topic")
        self.position = data.get("position")
        self.thread_metadata = ThreadMetadata(metadata) if (metadata := data.get("thread_metadata")) else None


class ThreadMember:
    __slots__ = ("id", "user_id", "join_timestamp", "flags")

    def __init__(self, data: ThreadMemberData) -> None:
        self.id = int(data["id"])
        self.user_id = int(data["user_id"])
        self.join_timestamp = iso_to_datetime(data["join_timestamp"])
        self.flags = data["flags"]


class ForumTag:
    __slots__ = (
        "id",
        "name",
        "is_moderated",
        "emoji_id",
        "emoji_name"
    )

    def __init__(self, data: ForumTagData) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.is_moderated = data["moderated"]
        self.emoji_id = int(data["emoji_id"]) if data["emoji_id"] is not None else None
        self.emoji_name = data["emoji_name"]


class DefaultReaction:
    __slots__ = ("emoji_id", "emoji_name")

    def __init__(self, data: DefaultReactionData) -> None:
        self.emoji_id = int(data["emoji_id"]) if data["emoji_id"] is not None else None
        self.emoji_name = data["emoji_name"]


class Channel(PartialChannel):
    __slots__ = (
        "permission_overwrites",
        "bitrate",
        "user_limit",
        "recipients",
        "icon",
        "owner_id",
        "application_id",
        "is_managed",
        "rtc_region",
        "video_quality_mode",
        "message_count",
        "member_count",
        "member",
        "default_auto_archive_duration",
        "total_message_sent",
        "available_tags",
        "applied_tags",
        "default_reaction_emoji",
        "default_thread_rate_limit_per_user",
        "default_sort_order",
        "default_forum_layout",
    )

    def __init__(self, data: ChannelData) -> None:
        super().__init__(data)
        self.permission_overwrites = [PermissionOverwrite(overwrite) for overwrite in data.get("permission_overwrites", [])]
        self.bitrate = data.get("bitrate")
        self.user_limit = data.get("user_limit")
        self.recipients = [User(user) for user in data["recipients"]]
        self.icon = Asset(icon, None, None) if (icon := data.get("icon")) else None
        self.owner_id = int(owner_id) if (owner_id := data.get("owner_id")) else None
        self.application_id = int(application_id) if (application_id := data.get("application_id")) else None
        self.is_managed = data.get("managed")
        self.rtc_region = data.get("rtc_region")
        self.video_quality_mode = try_enum(ChannelVideoQualityMode, mode) if (mode := data.get("video_quality_mode")) else None
        self.message_count = data.get("message_count")
        self.member_count = data.get("member_count")
        self.member = ThreadMember(member) if (member := data.get("member")) else None
        self.default_auto_archive_duration = data.get("default_auto_archive_duration")
        self.total_message_sent = data.get("total_message_sent")
        self.available_tags = [ForumTag(tag) for tag in data.get("available_tags", [])]
        self.applied_tags = [int(tag) for tag in data.get("applied_tags", [])]
        self.default_reaction_emoji = DefaultReaction(emoji) if (emoji := data.get("default_reaction_emoji")) else None
        self.default_thread_rate_limit_per_user = data.get("default_thread_rate_limit_per_user")
        self.default_sort_order = try_enum(ChannelSortOrderType, sort_order) if (sort_order := data.get("default_sort_order")) else None
        self.default_forum_layout = try_enum(ForumLayoutType, layout) if (layout := data.get("default_forum_layout")) else None
    
    def __repr__(self) -> str:
        return f"<Channel id={self.id} name={self.name!r}>"
