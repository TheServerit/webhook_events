from typing import TypedDict, NotRequired

from .abc import MentionableSnowflake
from .flags import RoleFlags
from .color import Color
from .cdn import Asset


__all__ = (
    "Role",
    "RoleColors",
    "RoleTags"
)


class RoleColorsData(TypedDict):
    primary_color: int
    secondary_color: int | None
    tertiary_color: int | None


class RoleTagsData(TypedDict):
    bot_id: NotRequired[str]
    integration_id: NotRequired[str]
    premium_subscriber: NotRequired[None]
    subscription_listing_id: NotRequired[str]
    available_for_purchase: NotRequired[None]
    guild_connections: NotRequired[None]


class RoleData(TypedDict):
    id: str
    name: str
    colors: RoleColorsData
    hoist: bool
    icon: NotRequired[str | None]
    unicode_emoji: NotRequired[str | None]
    position: int
    permissions: str
    managed: bool
    mentionable: bool
    tags: NotRequired[RoleTagsData]
    flags: int


class RoleColors:
    __slots__ = ("primary", "secondary", "tertiary")

    def __init__(self, data: RoleColorsData) -> None:
        self.primary = Color(data["primary_color"])
        self.secondary = Color(data["secondary_color"]) if data["secondary_color"] is not None else None
        self.tertiary = Color(data["tertiary_color"]) if data["tertiary_color"] is not None else None


class RoleTags:
    __slots__ = (
        "bot_id",
        "integration_id",
        "is_boost_role",
        "subscription_listing_id",
        "is_available_for_purchase",
        "is_linked_role"
    )

    def __init__(self, data: RoleTagsData) -> None:
        self.bot_id = int(bot_id) if (bot_id := data.get("bot_id")) else None
        self.integration_id = int(integration_id) if (integration_id := data.get("integration_id")) else None
        self.is_boost_role = data.get("premium_subscriber") is not None
        self.subscription_listing_id = int(subscription_listing_id) if (subscription_listing_id := data.get("subscription_listing_id")) else None
        self.is_available_for_purchase = data.get("available_for_purchase") is not None
        self.is_linked_role = data.get("guild_connections") is not None


class Role(MentionableSnowflake):
    __slots__ = (
        "id",
        "name",
        "colors",
        "is_hoisted",
        "icon",
        "unicode_emoji",
        "position",
        "permissions",
        "is_managed",
        "is_mentionable",
        "tags",
        "flags"
    )
    
    def __init__(self, data: RoleData) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.colors = RoleColors(data["colors"])
        self.is_hoisted = data["hoist"]
        self.icon = Asset(icon, self.id, "role-icons") if (icon := data.get("icon")) else None
        self.unicode_emoji = data.get("unicode_emoji")
        self.position = data["position"]
        self.permissions = data["permissions"]
        self.is_managed = data["managed"]
        self.is_mentionable = data["mentionable"]
        self.tags = RoleTags(tags) if (tags := data.get("tags")) else None
        self.flags = RoleFlags(data["flags"])

    def __repr__(self) -> str:
        return f"<Role id={self.id} name={self.name!r}>"
