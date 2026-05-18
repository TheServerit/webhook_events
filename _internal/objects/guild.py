from typing import TypedDict, NotRequired, Literal

from .enums import try_enum, VerificationLevel, NSFWLevel, ExplicitContentFilterLevel, MFALevel, DefaultMessageNotificationLevel
from .sticker import Sticker, StickerData
from .flags import SystemChannelFlags
from .emoji import Emoji, EmojiData
from .role import Role, RoleData
from .cdn import Asset

from ..utils import iso_to_datetime


__all__ = (
    "Guild",
    "WelcomeScreen",
    "WelcomeChannel",
    "IncidentsData"
)


class WelcomeChannelData(TypedDict):
    channel_id: str
    description: str
    emoji_id: str | None
    emoji_name: str | None


class WelcomeScreenData(TypedDict):
    description: str | None
    welcome_channels: list[WelcomeChannelData]


class WelcomeChannel:
    __slots__ = (
        "channel_id",
        "description",
        "emoji_id",
        "emoji_name"
    )

    def __init__(self, data: WelcomeChannelData) -> None:
        self.channel_id = int(data["channel_id"])
        self.description = data["description"]
        self.emoji_id = int(data["emoji_id"]) if data["emoji_id"] is not None else None
        self.emoji_name = data["emoji_name"]


class WelcomeScreen:
    __slots__ = (
        "description",
        "welcome_channels"
    )

    def __init__(self, data: WelcomeScreenData) -> None:
        self.description = data["description"]
        self.welcome_channels = [WelcomeChannel(channel) for channel in data["welcome_channels"]]


class IncidentsDataData(TypedDict):
    invites_disabled_until: str | None
    dms_disabled_until: str | None
    dm_spam_detected_at: NotRequired[str | None]
    raid_detected_at: NotRequired[str | None]


class IncidentsData:
    __slots__ = (
        "invites_disabled_until",
        "dms_disabled_until",
        "dm_spam_detected_at",
        "raid_detected_at"
    )
    
    def __init__(self, data: IncidentsDataData) -> None:
        self.invites_disabled_until = iso_to_datetime(data["invites_disabled_until"]) if data["invites_disabled_until"] is not None else None
        self.dms_disabled_until = iso_to_datetime(data["dms_disabled_until"]) if data["dms_disabled_until"] is not None else None
        self.dm_spam_detected_at = iso_to_datetime(dm_spam_detected_at) if (dm_spam_detected_at := data.get("dm_spam_detected_at")) else None
        self.raid_detected_at = iso_to_datetime(raid_detected_at) if (raid_detected_at := data.get("raid_detected_at")) else None


type GuildFeatures = Literal[
    "ANIMATED_BANNER",
    "ANIMATED_ICON",
    "APPLICATION_COMMAND_PERMISSIONS_V2",
    "AUTO_MODERATION",
    "BANNER",
    "COMMUNITY",
    "CREATOR_MONETIZABLE_PROVISIONAL",
    "CREATOR_STORE_PAGE",
    "DEVELOPER_SUPPORT_SERVER",
    "DISCOVERABLE",
    "FEATURABLE",
    "INVITES_DISABLED",
    "INVITE_SPLASH",
    "MEMBER_VERIFICATION_GATE_ENABLED",
    "MORE_SOUNDBOARD",
    "MORE_STICKERS",
    "NEWS",
    "PARTNERED",
    "PREVIEW_ENABLED",
    "RAID_ALERTS_DISABLED",
    "ROLE_ICONS",
    "ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE",
    "ROLE_SUBSCRIPTIONS_ENABLED",
    "SOUNDBOARD",
    "TICKETED_EVENTS_ENABLED",
    "VANITY_URL",
    "VERIFIED",
    "VIP_REGIONS",
    "WELCOME_SCREEN_ENABLED",
    "GUESTS_ENABLED",
    "GUILD_TAGS",
    "ENHANCED_ROLE_COLORS"
]


class GuildData(TypedDict):
    id: str
    name: str
    icon: NotRequired[str | None]
    splash: NotRequired[str | None]
    discovery_splash: NotRequired[str | None]
    owner_id: str
    afk_channel_id: str | None
    afk_timeout: int
    widget_enabled: NotRequired[bool]
    widget_channel_id: NotRequired[str | None]
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: list[RoleData]
    emojis: list[EmojiData]
    features: list[GuildFeatures]
    mfa_level: int
    application_id: str | None
    system_channel_id: str | None
    system_channel_flags: int
    rules_channel_id: str | None
    max_presences: NotRequired[int | None]
    max_members: NotRequired[int]
    vanity_url_code: str | None
    description: str | None
    banner: str | None
    premium_tier: int
    premium_subscription_count: NotRequired[int]
    preferred_locale: str
    public_updates_channel_id: str | None
    max_video_channel_users: NotRequired[int]
    max_stage_video_channel_users: NotRequired[int]
    welcome_screen: NotRequired[WelcomeScreenData]
    nsfw_level: int
    stickers: NotRequired[list[StickerData]]
    premium_progress_bar_enabled: bool
    safety_alerts_channel_id: str | None
    incidents_data: IncidentsDataData | None


class Guild:
    __slots__ = (
        "id",
        "name",
        "icon",
        "splash",
        "discovery_splash",
        "owner_id",
        "afk_channel_id",
        "afk_timeout",
        "widget_enabled",
        "widget_channel_id",
        "verification_level",
        "default_message_notifications_level",
        "explicit_content_filter_level",
        "stickers",
        "roles",
        "emojis",
        "features",
        "mfa_level",
        "nsfw_level",
        "safety_alerts_channel_id",
        "system_channel_id",
        "system_channel_flags",
        "rules_channel_id",
        "public_updates_channel_id",
        "preferred_locale",
        "vanity_url_code",
        "description",
        "banner",
        "boost_progress_bar_enabled",
        "boost_level",
        "boost_count",
        "max_video_channel_users",
        "max_stage_video_channel_users",
        "max_presences",
        "max_members",
        "welcome_screen",
        "incidents_data"
    )

    def __init__(self, data: GuildData) -> None:
        self.id = int(data["id"])
        self.name = data["name"]

        self.icon = Asset(icon, self.id, "icons") if (icon := data.get("icon")) else None
        self.splash = Asset(splash, self.id, "splashes") if (splash := data.get("splash")) else None
        self.discovery_splash = Asset(discovery_splash, self.id, "discovery-splashes") if (discovery_splash := data.get("discovery_splash")) else None
        
        self.owner_id = int(data["owner_id"])
        self.afk_channel_id = int(data["afk_channel_id"]) if data["afk_channel_id"] is not None else None
        self.afk_timeout = int(data["afk_timeout"])
        self.widget_enabled = data.get("widget_enabled", False)
        self.widget_channel_id = int(widget_channel_id) if (widget_channel_id := data.get("widget_channel_id")) else None

        self.verification_level = try_enum(VerificationLevel, data["verification_level"])
        self.default_message_notifications_level = try_enum(DefaultMessageNotificationLevel, data["default_message_notifications"])
        self.explicit_content_filter_level = try_enum(ExplicitContentFilterLevel, data["explicit_content_filter"])

        self.stickers = [Sticker(sticker) for sticker in stickers] if (stickers := data.get("stickers")) else []
        self.roles = [Role(role) for role in data["roles"]]
        self.emojis = [Emoji(emoji) for emoji in data["emojis"]]
        self.features = data["features"]
        self.mfa_level = try_enum(MFALevel, data["mfa_level"])
        self.nsfw_level = try_enum(NSFWLevel, data["nsfw_level"])

        self.safety_alerts_channel_id = int(data["safety_alerts_channel_id"]) if data["safety_alerts_channel_id"] is not None else None
        self.system_channel_id = int(data["system_channel_id"]) if data["system_channel_id"] is not None else None
        self.system_channel_flags = SystemChannelFlags(data["system_channel_flags"])
        self.rules_channel_id = int(data["rules_channel_id"]) if data["rules_channel_id"] is not None else None
        self.public_updates_channel_id = int(data["public_updates_channel_id"]) if data["public_updates_channel_id"] is not None else None

        self.preferred_locale = data["preferred_locale"]
        self.vanity_url_code = data["vanity_url_code"]
        self.description = data["description"]
        self.banner = Asset(data["banner"], self.id, "banners") if data["banner"] is not None else None

        self.boost_progress_bar_enabled = data["premium_progress_bar_enabled"]
        self.boost_level = data["premium_tier"]
        self.boost_count = data.get("premium_subscription_count", 0)

        self.max_video_channel_users = data.get("max_video_channel_users")
        self.max_stage_video_channel_users = data.get("max_stage_video_channel_users")
        self.max_presences = data.get("max_presences")
        self.max_members = data.get("max_members")

        self.welcome_screen = WelcomeScreen(welcome_screen) if (welcome_screen := data.get("welcome_screen")) else None
        self.incidents_data = IncidentsData(data["incidents_data"]) if data["incidents_data"] is not None else None

    def __repr__(self) -> str:
        return f"<Guild id={self.id} name={self.name!r}>"
