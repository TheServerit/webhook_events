from typing import TypedDict, NotRequired

from .user import UserData, User
from .abc import Snowflake


__all__ = ("Emoji", "PartialEmoji")


class PartialEmojiData(TypedDict):
    id: str | None
    name: str | None
    animated: NotRequired[bool]


class EmojiData(PartialEmojiData, total=False):
    roles: list[str]
    user: UserData
    require_colons: bool
    managed: bool
    available: bool


class PartialEmoji:
    __slots__ = (
        "id",
        "name",
        "animated"
    )

    def __init__(self, data: PartialEmojiData) -> None:
        self.id = int(emoji_id) if (emoji_id := data.get("id")) else None
        self.name = data["name"]
        self.animated = data.get("animated", False)

    @property
    def mention(self) -> str:
        name = self.name or '_' # "_" renders in the client regardless of having no name

        if self.id is None:
            return name
        
        if self.animated:
            return f"<a:{name}:{self.id}>"
        
        return f"<:{name}:{self.id}>"


class Emoji(Snowflake):
    __slots__ = (
        "id",
        "name",
        "roles",
        "user",
        "require_colons",
        "is_managed",
        "is_available",
        "is_animated",
        "url"
    )

    def __init__(self, data: EmojiData) -> None:
        self.id = int(data["id"]) # pyright: ignore[reportArgumentType] | id is not None for full emoji object
        self.name: str = data["name"] # pyright: ignore[reportAttributeAccessIssue] | name is not None for full emoji object
        self.roles = data.get("roles", [])
        self.user = User(user) if (user := data.get("user")) else None
        self.require_colons = data.get("require_colons", False)
        self.is_managed = data.get("managed", False)
        self.is_available = data.get("available", True)
        self.is_animated = data.get("animated", False)

        self.url = f"https://cdn.discordapp.com/emojis/{self.id}.png"

    @property
    def mention(self) -> str:
        """Returns the emoji markdown (<:name:id> format)."""
        animated_str = "a" if self.is_animated else ""
        return f"<:{animated_str}{self.name}:{self.id}>"
    
    def __repr__(self) -> str:
        return f"<Emoji id={self.id} name={self.name!r}>"
