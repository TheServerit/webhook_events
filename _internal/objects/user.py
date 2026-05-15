from typing import TypedDict, NotRequired

from .enums import try_enum, DisplayNameFont, DisplayNameEffect
from .flags import PublicUserFlags
from .abc import MentionableSnowflake
from .color import Color
from .cdn import Asset


__all__ = (
    "User",
    "WebhookUser",
    "Nameplate",
    "Collectibles",
    "PrimaryGuild",
    "DisplayNameStyles"
)


class AvatarDecorationData(TypedDict):
    asset: str
    sku_id: str


class NameplateData(TypedDict):
    sku_id: str
    asset: str
    label: str
    palette: str


class CollectiblesData(TypedDict):
    nameplate: NotRequired[NameplateData]


class PrimaryGuildData(TypedDict):
    identity_guild_id: str | None
    identity_enabled: bool | None
    tag: str | None
    badge: str | None


class DisplayNameStylesData(TypedDict):
    font_id: int
    effect_id: int
    colors: list[int]


class UserData(TypedDict):
    id: str
    username: str
    discriminator: str
    global_name: str | None
    avatar: str | None
    bot: NotRequired[bool]
    system: NotRequired[bool]
    banner: NotRequired[str | None]
    accent_color: NotRequired[int | None]
    public_flags: NotRequired[int]
    avatar_decorator_data: NotRequired[AvatarDecorationData | None]
    collectibles: NotRequired[CollectiblesData | None]
    primary_guild: NotRequired[PrimaryGuildData | None]
    display_name_styles: NotRequired[DisplayNameStylesData | None]


class WebhookUserData(TypedDict):
    id: str
    username: str
    avatar: str


class AvatarDecoration:
    __slots__ = (
        "asset_hash",
        "sku_id",
        "url"
    )

    def __init__(self, data: AvatarDecorationData) -> None:
        self.asset_hash = data["asset"]
        self.sku_id = int(data["sku_id"])
        self.url = Asset(self.asset_hash, None, "avatar-decoration-presets").url


class Nameplate:
    __slots__ = (
        "sku_id",
        "label",
        "palette",
        "url"
    )

    def __init__(self, data: NameplateData) -> None:
        self.sku_id = int(data["sku_id"])
        self.label = data["label"]
        self.palette = data["palette"]

        asset = data["asset"]
        self.url = f"https://cdn.discordapp.com/assets/collectibles/{asset}asset.webm" # Does not use cdn.Asset due to structure difference


class Collectibles:
    __slots__ = ("nameplate",)

    def __init__(self, data: CollectiblesData) -> None:
        self.nameplate = Nameplate(nameplate) if (nameplate := data.get("nameplate")) else None


class PrimaryGuild:
    __slots__ = (
        "identity_guild_id",
        "identity_enabled",
        "tag",
        "badge_asset_hash",
        "badge_url"
    )

    def __init__(self, data: PrimaryGuildData) -> None:
        self.identity_guild_id = int(identity_guild_id) if (identity_guild_id := data["identity_guild_id"]) else None

        self.identity_enabled = bool(data["identity_enabled"])
        self.tag = data["tag"]
        self.badge_asset_hash = data["badge"]

        asset_url = None
        if self.identity_guild_id and self.badge_asset_hash:
            asset_url = Asset(self.badge_asset_hash, self.identity_guild_id, "clan-badges").url

        self.badge_url = asset_url


class DisplayNameStyles:
    __slots__ = (
        "font",
        "effect",
        "colors"
    )

    def __init__(self, data: DisplayNameStylesData) -> None:
        self.font = try_enum(DisplayNameFont, data["font_id"])
        self.effect = try_enum(DisplayNameEffect, data["effect_id"])
        self.colors = [Color(color) for color in data.get("colors", [])]


class WebhookUser(MentionableSnowflake):
    __slots__ = ("id", "username", "avatar")

    def __init__(self, data: WebhookUserData) -> None:
        self.id = int(data["id"])
        self.username = data["username"]
        self.avatar = Asset(avatar, self.id, "avatars") if (avatar := data.get("avatar")) else None


class User(MentionableSnowflake):
    __slots__ = (
        "id",
        "username",
        "discriminator",
        "global_name",
        "avatar",
        "is_bot",
        "is_system",
        "banner",
        "accent_color",
        "public_flags",
        "avatar_decoration",
        "collectibles",
        "primary_guild",
        "display_name_styles"
    )

    def __init__(self, data: UserData) -> None:
        self.id = int(data["id"])
        self.username = data["username"]
        self.discriminator = data["discriminator"]
        self.global_name = data["global_name"]

        self.accent_color = Color(accent_color) if (accent_color := data.get("accent_color")) else None

        self.avatar = Asset(avatar, self.id, "avatars") if (avatar := data["avatar"]) else None
        self.banner = Asset(banner, self.id, "banners") if (banner := data.get("banner")) else None
        self.avatar_decoration = AvatarDecoration(avatar_decoration) if (avatar_decoration := data.get("avatar_decoration")) else None

        self.is_bot = data.get("bot", False)
        self.is_system = data.get("system", False)

        self.public_flags = PublicUserFlags(data.get("public_flags", 0))

        self.collectibles = Collectibles(collectibles) if (collectibles := data.get("collectibles")) else None
        self.primary_guild = PrimaryGuild(primary_guild) if (primary_guild := data.get("primary_guild")) else None
        self.display_name_styles = DisplayNameStyles(display_name_styles) if (display_name_styles := data.get("display_name_styles")) else None

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}#{self.discriminator}>"
