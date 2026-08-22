from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import IntEnum

from .enums import (
    UnfurledMediaItemFlagsTypes,
    SystemChannelFlagsTypes,
    AttachmentFlagsTypes,
    EmbedMediaFlagsTypes,
    MessageFlagsTypes,
    ChannelFlagsTypes,
    MemberFlagsTypes,
    EmbedFlagsTypes,
    UserFlagsTypes,
    RoleFlagsTypes
)


__all__ = (
    "PublicUserFlags",
    "MessageFlags",
    "RoleFlags",
    "SystemChannelFlags",
    "AttachmentFlags",
    "EmbedMediaFlags",
    "EmbedFlags",
    "UnfurledMediaItemFlags",
    "MemberFlags",
    "ChannelFlags"
)


class BaseFlags:
    __slots__ = ('value',)
    
    def __init__(self, value: int) -> None:
        self.value = value

    def _has_flag(self, bit_enum: IntEnum) -> bool:
        bit = int(bit_enum)
        return bool(self.value & (1 << bit))
    
    def __int__(self) -> int:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.value == other.value

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} value={self.value}>"


class PublicUserFlags(BaseFlags):
    """
    Represents a user's flag bitfield, with a boolean check for each flag + `all` function.

    ---
    Calling `int()` on this will return the flags integer value.

    This class supports equality checks (== and !=) between instances of this class.
    """

    @property
    def staff(self) -> bool:
        """User is a Discord Employee."""
        return self._has_flag(UserFlagsTypes.STAFF)

    @property
    def partner(self) -> bool:
        """User is a Partnered Server Owner."""
        return self._has_flag(UserFlagsTypes.PARTNER)

    @property
    def hypesquad(self) -> bool:
        return self._has_flag(UserFlagsTypes.HYPESQUAD)

    @property
    def bug_hunter_level_1(self) -> bool:
        return self._has_flag(UserFlagsTypes.BUG_HUNTER_LEVEL_1)

    @property
    def hypesquad_bravery(self) -> bool:
        return self._has_flag(UserFlagsTypes.HYPESQUAD_BRAVERY)

    @property
    def hypesquad_brilliance(self) -> bool:
        return self._has_flag(UserFlagsTypes.HYPESQUAD_BRILLIANCE)

    @property
    def hypesquad_balance(self) -> bool:
        return self._has_flag(UserFlagsTypes.HYPESQUAD_BALANCE)

    @property
    def early_nitro_supporter(self) -> bool:
        return self._has_flag(UserFlagsTypes.EARLY_NITRO_SUPPORTER)

    @property
    def team_user(self) -> bool:
        """User is a team."""
        return self._has_flag(UserFlagsTypes.TEAM_USER)

    @property
    def bug_hunter_level_2(self) -> bool:
        return self._has_flag(UserFlagsTypes.BUG_HUNTER_LEVEL_2)

    @property
    def verified_bot(self) -> bool:
        return self._has_flag(UserFlagsTypes.VERIFIED_BOT)

    @property
    def early_verified_developer(self) -> bool:
        return self._has_flag(UserFlagsTypes.EARLY_VERIFIED_DEVELOPER)

    @property
    def certified_moderator(self) -> bool:
        """User is part of the Moderator Programs alumni."""
        return self._has_flag(UserFlagsTypes.CERTIFIED_MODERATOR)

    @property
    def bot_http_interactions(self) -> bool:
        """Bot uses only HTTP interactions and is shown in the online member list."""
        return self._has_flag(UserFlagsTypes.BOT_HTTP_INTERACTIONS)
    
    @property
    def spammer(self) -> bool:
        """User is a flagged Spammer."""
        return self._has_flag(UserFlagsTypes.SPAMMER)

    def all(self) -> list[UserFlagsTypes]:
        """Returns a list of all flags that the user has."""
        return [flag for flag in UserFlagsTypes if self._has_flag(flag)]


class MessageFlags(BaseFlags):
    """
    Represents a message's flag bitfield, with a boolean check for each flag + `all` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def crossposted(self) -> bool:
        """This message has been published to subscribed channels (via Channel Following)."""
        return self._has_flag(MessageFlagsTypes.CROSSPOSTED)

    @property
    def is_crosspost(self) -> bool:
        """This message originated from another channel (via Channel Following)."""
        return self._has_flag(MessageFlagsTypes.IS_CROSSPOST)

    @property
    def suppress_embeds(self) -> bool:
        """Do not include any embeds when serializing this message."""
        return self._has_flag(MessageFlagsTypes.SUPPRESS_EMBEDS)

    @property
    def source_message_deleted(self) -> bool:
        """The source message for this crosspost has been deleted."""
        return self._has_flag(MessageFlagsTypes.SOURCE_MESSAGE_DELETED)

    @property
    def urgent(self) -> bool:
        """This message came from the urgent message system."""
        return self._has_flag(MessageFlagsTypes.URGENT)

    @property
    def has_thread(self) -> bool:
        """This message has an associated thread."""
        return self._has_flag(MessageFlagsTypes.HAS_THREAD)

    @property
    def ephemeral(self) -> bool:
        """This message is only visible to the user who invoked the Interaction."""
        return self._has_flag(MessageFlagsTypes.EPHEMERAL)

    @property
    def loading(self) -> bool:
        """This message is an Interaction Response and the bot is 'thinking'."""
        return self._has_flag(MessageFlagsTypes.LOADING)

    @property
    def failed_to_mention_some_roles_in_thread(self) -> bool:
        """This message failed to mention some roles and add their members to the thread."""
        return self._has_flag(MessageFlagsTypes.FAILED_TO_MENTION_SOME_ROLES_IN_THREAD)

    @property
    def suppress_notifications(self) -> bool:
        """This message will not trigger push or desktop notifications."""
        return self._has_flag(MessageFlagsTypes.SUPPRESS_NOTIFICATIONS)

    @property
    def is_voice_message(self) -> bool:
        """This message is a voice message."""
        return self._has_flag(MessageFlagsTypes.IS_VOICE_MESSAGE)

    @property
    def has_snapshot(self) -> bool:
        """This message has a snapshot (via Message Forwarding)."""
        return self._has_flag(MessageFlagsTypes.HAS_SNAPSHOT)

    @property
    def is_components_v2(self) -> bool:
        """This message uses the new Component V2 system (fully component-driven messages)."""
        return self._has_flag(MessageFlagsTypes.IS_COMPONENTS_V2)

    def all(self) -> list[MessageFlagsTypes]:
        """Returns a list of all flags that the message has."""
        return [flag for flag in MessageFlagsTypes if self._has_flag(flag)]


class RoleFlags(BaseFlags):
    """
    Represents a role's flag bitfield, with a boolean check for each flag + `all` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def in_prompt(self) -> bool: 
        return self._has_flag(RoleFlagsTypes.IN_PROMPT)
    
    def all(self) -> list[RoleFlagsTypes]:
        """Returns a list of all flags that the role has."""
        return [flag for flag in RoleFlagsTypes if self._has_flag(flag)]


class SystemChannelFlags(BaseFlags):
    """
    Represents a guild's system channel's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """
    
    @property
    def suppress_member_join_notifications(self) -> bool:
        return self._has_flag(SystemChannelFlagsTypes.SUPPRESS_MEMBER_JOIN_NOTIFICATIONS)
    
    @property
    def suppress_boost_notifications(self) -> bool:
        return self._has_flag(SystemChannelFlagsTypes.SUPPRESS_BOOST_NOTIFICATIONS)
    
    @property
    def suppress_server_setup_tips(self) -> bool:
        return self._has_flag(SystemChannelFlagsTypes.SUPPRESS_SERVER_SETUP_TIPS)
    
    @property
    def suppress_member_join_notification_replies(self) -> bool:
        """Hide member join sticker reply buttons."""
        return self._has_flag(SystemChannelFlagsTypes.SUPPRESS_MEMBER_JOIN_NOTIFICATION_REPLIES)
    
    @property
    def suppress_role_subscription_purchase_notifications(self) -> bool:
        """Suppress role subscription purchase and renewal notifications."""
        return self._has_flag(SystemChannelFlagsTypes.SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS)
    
    @property
    def suppress_role_subscription_purchase_notification_replies(self) -> bool:
        """Hide role subscription sticker reply buttons."""
        return self._has_flag(SystemChannelFlagsTypes.SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES)
    
    def all(self) -> list[SystemChannelFlagsTypes]:
        """Returns a list of all flags that the system channel has."""
        return [flag for flag in SystemChannelFlagsTypes if self._has_flag(flag)]


class AttachmentFlags(BaseFlags):
    """
    Represents an attachment's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def is_clip(self) -> bool:
        """This attachment is a Clip from a stream."""
        return self._has_flag(AttachmentFlagsTypes.IS_CLIP)
    
    @property
    def is_thumbnail(self) -> bool:
        """This attachment is the thumbnail of a thread in a media channel, displayed in the grid but not on the message."""
        return self._has_flag(AttachmentFlagsTypes.IS_THUMBNAIL)
    
    @property
    def is_remix(self) -> bool:
        """This attachment has been edited using the remix feature on mobile (deprecated)."""
        return self._has_flag(AttachmentFlagsTypes.IS_REMIX)
    
    @property
    def is_spoiler(self) -> bool:
        return self._has_flag(AttachmentFlagsTypes.IS_SPOILER)
    
    @property
    def is_animated(self) -> bool:
        return self._has_flag(AttachmentFlagsTypes.IS_ANIMATED)
    
    def all(self) -> list[AttachmentFlagsTypes]:
        """Returns a list of all flags that the attachment has."""
        return [flag for flag in AttachmentFlagsTypes if self._has_flag(flag)]


class EmbedMediaFlags(BaseFlags):
    """
    Represents an embed's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def is_animated(self) -> bool:
        return self._has_flag(EmbedMediaFlagsTypes.IS_ANIMATED)

    def all(self) -> list[EmbedMediaFlagsTypes]:
        """Returns a list of all flags that the embed has."""
        return [flag for flag in EmbedMediaFlagsTypes if self._has_flag(flag)]


class EmbedFlags(BaseFlags):
    """
    Represents an embed's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def is_content_inventory_entry(self) -> bool:
        """This embed is a fallback for a reply to an activity card."""
        return self._has_flag(EmbedFlagsTypes.IS_CONTENT_INVENTORY_ENTRY)

    def all(self) -> list[EmbedFlagsTypes]:
        """Returns a list of all flags that the embed has."""
        return [flag for flag in EmbedFlagsTypes if self._has_flag(flag)]


class UnfurledMediaItemFlags(BaseFlags):
    """
    Represents an unfurled URL's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def is_animated(self) -> bool:
        return self._has_flag(UnfurledMediaItemFlagsTypes.IS_ANIMATED)

    def all(self) -> list[UnfurledMediaItemFlagsTypes]:
        """Returns a list of all flags that the unfurled URL has."""
        return [flag for flag in UnfurledMediaItemFlagsTypes if self._has_flag(flag)]


class MemberFlags(BaseFlags):
    """
    Represents a member's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def did_rejoin(self) -> bool:
        return self._has_flag(MemberFlagsTypes.DID_REJOIN)
    
    @property
    def completed_onboarding(self) -> bool:
        return self._has_flag(MemberFlagsTypes.COMPLETED_ONBOARDING)
    
    @property
    def bypasses_verification(self) -> bool:
        """Member is exempt from guild verification requirements."""
        return self._has_flag(MemberFlagsTypes.BYPASSES_VERIFICATION)
    
    @property
    def started_onboarding(self) -> bool:
        return self._has_flag(MemberFlagsTypes.STARTED_ONBOARDING)
    
    @property
    def is_guest(self) -> bool:
        """Member is a guest and can only access the voice channel they were invited to."""
        return self._has_flag(MemberFlagsTypes.IS_GUEST)
    
    @property
    def started_home_actions(self) -> bool:
        """Member has started Server Guide new member actions."""
        return self._has_flag(MemberFlagsTypes.STARTED_HOME_ACTIONS)
    
    @property
    def completed_home_actions(self) -> bool:
        """Member has completed Server Guide new member actions."""
        return self._has_flag(MemberFlagsTypes.COMPLETED_HOME_ACTIONS)
    
    @property
    def automod_quarantined_username(self) -> bool:
        """Member's username, display name, or nickname is blocked by AutoMod."""
        return self._has_flag(MemberFlagsTypes.AUTOMOD_QUARANTINED_USERNAME)
    
    @property
    def dm_settings_upsell_acknowledged(self) -> bool:
        """Member has dismissed the DM settings upsell."""
        return self._has_flag(MemberFlagsTypes.DM_SETTINGS_UPSELL_ACKNOWLEDGED)
    
    @property
    def automod_quarantined_guild_tag(self) -> bool:
        """Member’s guild tag is blocked by AutoMod."""
        return self._has_flag(MemberFlagsTypes.AUTOMOD_QUARANTINED_GUILD_TAG)

    def all(self) -> list[MemberFlagsTypes]:
        """Returns a list of all flags that the member has."""
        return [flag for flag in MemberFlagsTypes if self._has_flag(flag)]


class ChannelFlags(BaseFlags):
    """
    Represents a channel's flag bitfield, with a boolean check for each flag + `all()` function.

    ---
    Calling `int()` on this returns the integer value of the flags.

    Supports equality checks (== and !=) between instances of this class.
    """

    @property
    def pinned(self) -> bool:
        """This thread is pinned to the top of its parent `GUILD_FORUM` or `GUILD_MEDIA` channel."""
        return self._has_flag(ChannelFlagsTypes.PINNED)
    
    @property
    def require_tag(self) -> bool:
        """Whether a tag is required to be specified when creating a thread in a `GUILD_FORUM` or a `GUILD_MEDIA` channel. Tags are specified in the `.applied_tags`"""
        return self._has_flag(ChannelFlagsTypes.REQUIRE_TAG)
    
    @property
    def hide_media_download_options(self) -> bool:
        """When set hides the embedded media download options. Available only for media channels."""
        return self._has_flag(ChannelFlagsTypes.HIDE_MEDIA_DOWNLOAD_OPTIONS)

    @property
    def obfuscated(self) -> bool:
        return self._has_flag(ChannelFlagsTypes.CHANNEL_OBFUSCATED)

    @property
    def spoiler(self) -> bool:
        return self._has_flag(ChannelFlagsTypes.IS_SPOILER_CHANNEL)

    def all(self) -> list[ChannelFlagsTypes]:
        """Returns a list of all flags that the channel has."""
        return [flag for flag in ChannelFlagsTypes if self._has_flag(flag)]
