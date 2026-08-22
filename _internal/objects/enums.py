from typing import Any

from enum import IntEnum, StrEnum, Enum


__all__ = (
    "UserFlagsTypes",
    "MessageFlagsTypes",
    "RoleFlagsTypes",
    "SystemChannelFlagsTypes",
    "AttachmentFlagsTypes",
    "EmbedMediaFlagsTypes",
    "MemberFlagsTypes",

    "VerificationLevel",
    "NSFWLevel",
    "ExplicitContentFilterLevel",
    "MFALevel",
    "DefaultMessageNotificationLevel",
    "MessageType",
    "StickerType",
    "StickerFormatType",
    "DisplayNameFont",
    "DisplayNameEffect",
    "EntitlementType",
    "IntegrationType",
    "ChannelType",
    "EmbedType",
    "MessageReferenceType",
    "MessageActivityType",
    "ComponentType",
    "ButtonStyle",
    "SeparatorSpacing",
    "InteractionType",
    "BaseThemeType",
    "PermissionOverwriteType",
    "ChannelVideoQualityMode",
    "ChannelSortOrderType",
    "ForumLayoutType"
)


def create_unknown_value[EnumT: Enum](cls: type[EnumT], val: Any) -> EnumT:
    obj = object.__new__(cls)

    obj._name_ = f"unknown_{val}"
    obj._value_ = val

    return obj


def try_enum[EnumT: Enum](cls: type[EnumT], val: Any) -> EnumT:
    try:
        return cls(val)
    except (KeyError, TypeError, AttributeError, ValueError):
        return create_unknown_value(cls, val)


# Flags:

class UserFlagsTypes(IntEnum):
    STAFF = 0
    PARTNER = 1
    HYPESQUAD = 2
    BUG_HUNTER_LEVEL_1 = 3
    HYPESQUAD_BRAVERY = 6
    HYPESQUAD_BRILLIANCE = 7
    HYPESQUAD_BALANCE = 8
    EARLY_NITRO_SUPPORTER = 9
    TEAM_USER = 10
    BUG_HUNTER_LEVEL_2 = 14
    VERIFIED_BOT = 16
    EARLY_VERIFIED_DEVELOPER = 17
    CERTIFIED_MODERATOR = 18
    BOT_HTTP_INTERACTIONS = 19
    SPAMMER = 20


class MessageFlagsTypes(IntEnum):
    CROSSPOSTED = 0
    IS_CROSSPOST = 1
    SUPPRESS_EMBEDS = 2
    SOURCE_MESSAGE_DELETED = 3
    URGENT = 4
    HAS_THREAD = 5
    EPHEMERAL = 6
    LOADING = 7
    FAILED_TO_MENTION_SOME_ROLES_IN_THREAD = 8
    SUPPRESS_NOTIFICATIONS = 12
    IS_VOICE_MESSAGE = 13
    HAS_SNAPSHOT = 14
    IS_COMPONENTS_V2 = 15


class RoleFlagsTypes(IntEnum):
    IN_PROMPT = 0


class SystemChannelFlagsTypes(IntEnum):
    SUPPRESS_MEMBER_JOIN_NOTIFICATIONS = 0
    SUPPRESS_BOOST_NOTIFICATIONS = 1
    SUPPRESS_SERVER_SETUP_TIPS = 2
    SUPPRESS_MEMBER_JOIN_NOTIFICATION_REPLIES = 3
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 4
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 5    


class AttachmentFlagsTypes(IntEnum):
    IS_CLIP = 0
    IS_THUMBNAIL = 1
    IS_REMIX = 2
    IS_SPOILER = 3
    IS_ANIMATED = 5


class EmbedMediaFlagsTypes(IntEnum):
    IS_ANIMATED = 5


class EmbedFlagsTypes(IntEnum):
    IS_CONTENT_INVENTORY_ENTRY = 5


class UnfurledMediaItemFlagsTypes(IntEnum):
    IS_ANIMATED = 0


# Guild:

class VerificationLevel(IntEnum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    VERY_HIGH = 4


class NSFWLevel(IntEnum):
    DEFAULT = 0
    EXPLICIT = 1
    SAFE = 2
    AGE_RESTRICTED = 3


class DefaultMessageNotificationLevel(IntEnum):
    ALL_MESSAGES = 0
    ONLY_MENTIONS = 1


class ExplicitContentFilterLevel(IntEnum):
    DISABLED = 0
    MEMBERS_WITHOUT_ROLES = 1
    ALL_MEMBERS = 2


class MFALevel(IntEnum):
    NONE = 0
    ELEVATED = 1


# Message:

class MessageType(IntEnum):
    DEFAULT = 0
    RECIPIENT_ADD = 1
    RECIPIENT_REMOVE = 2
    CALL = 3
    CHANNEL_NAME_CHANGE = 4
    CHANNEL_ICON_CHANGE = 5
    CHANNEL_PINNED_MESSAGE = 6
    USER_JOIN = 7
    GUILD_BOOST = 8
    GUILD_BOOST_TIER_1 = 9
    GUILD_BOOST_TIER_2 = 10
    GUILD_BOOST_TIER_3 = 11
    CHANNEL_FOLLOW_ADD = 12
    GUILD_DISCOVERY_DISQUALIFIED = 14
    GUILD_DISCOVERY_REQUALIFIED = 15
    GUILD_DISCOVERY_GRACE_PERIOD_INITIAL_WARNING = 16
    GUILD_DISCOVERY_GRACE_PERIOD_FINAL_WARNING = 17
    THREAD_CREATED = 18
    REPLY = 19
    CHAT_INPUT_COMMAND = 20
    THREAD_STARTER_MESSAGE = 21
    GUILD_INVITE_REMINDER = 22
    CONTEXT_MENU_COMMAND = 23
    AUTO_MODERATION_ACTION = 24
    ROLE_SUBSCRIPTION_PURCHASE = 25
    INTERACTION_PREMIUM_UPSELL = 26
    STAGE_START = 27
    STAGE_END = 28
    STAGE_SPEAKER = 29
    STAGE_TOPIC = 31
    GUILD_APPLICATION_PREMIUM_SUBSCRIPTION = 32
    GUILD_INCIDENT_ALERT_MODE_ENABLED = 36
    GUILD_INCIDENT_ALERT_MODE_DISABLED = 37
    GUILD_INCIDENT_REPORT_RAID = 38
    GUILD_INCIDENT_REPORT_FALSE_ALARM = 39
    PURCHASE_NOTIFICATION = 44
    POLL_RESULT = 46


class MessageActivityType(IntEnum):
    JOIN = 1
    SPECTATE = 2
    LISTEN = 3
    JOIN_REQUEST = 5


class MessageReferenceType(IntEnum):
    DEFAULT = 0
    FORWARD = 1



class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class PollLayoutType(IntEnum):
    DEFAULT = 1


class BaseThemeType(IntEnum):
    UNSET = 0
    DARK = 1
    LIGHT = 2
    DARKER = 3
    MIDNIGHT = 4


class MemberFlagsTypes(IntEnum):
    DID_REJOIN = 0
    COMPLETED_ONBOARDING = 1
    BYPASSES_VERIFICATION = 2
    STARTED_ONBOARDING = 3
    IS_GUEST = 4
    STARTED_HOME_ACTIONS = 5
    COMPLETED_HOME_ACTIONS = 6
    AUTOMOD_QUARANTINED_USERNAME = 7
    DM_SETTINGS_UPSELL_ACKNOWLEDGED = 9
    AUTOMOD_QUARANTINED_GUILD_TAG = 10


# Sticker:

class StickerType(IntEnum):
    STANDARD = 1
    GUILD = 2


class StickerFormatType(IntEnum):
    PNG = 1
    APNG = 2
    LOTTIE = 3
    GIF = 4


# User:

class DisplayNameFont(IntEnum):
    GG_SANS = 11
    TEMPO = 12
    SAKURA = 3
    JELLYBEAN = 4
    MODERN = 6
    MEDIEVAL = 7
    EIGHT_BIT = 8
    VAMPYRE = 10
    MONKEY_BARS = 13
    MAINFRAME = 14
    HEADBANG = 15
    JOURNAL = 16


class DisplayNameEffect(IntEnum):
    SOLID = 1
    GRADIENT = 2
    NEON = 3
    TOON = 4
    POP = 5
    PRISM = 7
    GUMMY = 8


# Events:

class EntitlementType(IntEnum):
    PURCHASE = 1
    PREMIUM_SUBSCRIPTION = 2
    DEVELOPER_GIFT = 3
    TEST_MODE_PURCHASE = 4
    FREE_PURCHASE = 5
    USER_GIFT = 6
    PREMIUM_PURCHASE = 7
    APPLICATION_SUBSCRIPTION = 8


class IntegrationType(IntEnum):
    GUILD = 0
    USER = 1


# Channel:

class ChannelType(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_ANNOUNCEMENT = 5
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15
    GUILD_MEDIA = 16


class ChannelFlagsTypes(IntEnum):
    PINNED = 1
    REQUIRE_TAG = 4
    HIDE_MEDIA_DOWNLOAD_OPTIONS = 15
    CHANNEL_OBFUSCATED = 17
    IS_SPOILER_CHANNEL = 21


class PermissionOverwriteType(IntEnum):
    ROLE = 0
    MEMBER = 1


class ChannelVideoQualityMode(IntEnum):
    AUTO = 1
    FULL = 2


class ChannelSortOrderType(IntEnum):
    LATEST_ACTIVITY = 0
    CREATION_DATE = 1


class ForumLayoutType(IntEnum):
    NOT_SET = 0
    LIST_VIEW = 1
    GALLERY_VIEW = 2


# Embed:

class EmbedType(StrEnum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"
    POLL_RESULT = "poll_result"


# Components:

class ComponentType(IntEnum):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8
    SECTION = 9
    TEXT_DISPLAY = 10
    THUMBNAIL = 11
    MEDIA_GALLERY = 12
    FILE = 13
    SEPARATOR = 14
    CONTAINER = 17


class ButtonStyle(IntEnum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5
    PREMIUM = 6

    # Aliases:
    BLURPLE = 1
    GRAY = 2
    GREEN = 3
    RED = 4
    URL = 5


class SeparatorSpacing(IntEnum):
    SMALL = 1
    LARGE = 2
