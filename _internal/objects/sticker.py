from typing import TypedDict, NotRequired

from .enums import try_enum, StickerType, StickerFormatType
from .user import UserData, User
from .abc import Snowflake


__all__ = ("Sticker", "PartialSticker")


class StickerData(TypedDict):
    id: str
    pack_id: NotRequired[str]
    name: str
    description: str | None
    tags: str
    type: int
    format_type: int
    available: NotRequired[bool]
    guild_id: NotRequired[str]
    user: NotRequired[UserData]
    sort_value: NotRequired[int]


class PartialStickerData(TypedDict):
    id: str
    name: str
    format_type: int


class PartialSticker:
    __slots__ = ("id", "name", "format", "url")
    
    def __init__(self, data: PartialStickerData) -> None:
        self.id = int(data["id"])
        self.name = data["name"]
        self.format = try_enum(StickerFormatType, data["format_type"])

        self.url = f"https://media.discordapp.net/stickers/{self.id}.png"


class Sticker(Snowflake):
    __slots__ = (
        "id",
        "pack_id",
        "name",
        "description",
        "tags",
        "type",
        "format",
        "is_available",
        "guild_id",
        "user",
        "sort_value",
        "url"
    )
    
    def __init__(self, data: StickerData) -> None:
        self.id = int(data["id"])
        self.pack_id = int(pack_id) if (pack_id := data.get("pack_id")) else None
        self.name = data["name"]
        self.description = data["description"]
        self.tags = data["tags"]
        self.type = try_enum(StickerType, data["type"])
        self.format = try_enum(StickerFormatType, data["format_type"])
        self.is_available = data.get("available", True)
        self.guild_id = int(guild_id) if (guild_id := data.get("guild_id")) else None
        self.user = User(user) if (user := data.get("user")) else None
        self.sort_value = data.get("sort_value")

        self.url = f"https://media.discordapp.net/stickers/{self.id}.png"

    def __repr__(self) -> str:
        return f"<Sticker id={self.id} name={self.name!r}>"
