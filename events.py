"""This module contains all event objects."""

from ._internal.utils import iso_to_datetime as _iso_to_datetime
from typing import Any as _Any

__all__ = [
    "ApplicationAuthorized",
    "ApplicationDeauthorized",
    "EntitlementCreate",
    "LobbyMessageCreate",
    "LobbyMessageUpdate",
    "LobbyMessageDelete",
    "GameDirectMessageCreate",
    "GameDirectMessageUpdate",
    "GameDirectMessageDelete"
]


class _AnyEvent:
    def __init__(self, _: dict[str, _Any]) -> None:
        pass # Overridden by subclasses


class _BaseLobbyMessage:
    def __init__(self, data: dict[str, _Any]) -> None:
        self.id = int(data["id"])
        self.type: int = data["type"]
        self.content: str = data["content"]
        self.lobby_id = int(data["lobby_id"])
        self.channel_id = int(data["channel_id"])
        self.author: dict[str, _Any] = data["author"]
        self.metadata: dict[str, _Any] | None = data.get("metadata")
        self.flags: int = data["flags"]
        self.application_id = int(data["application_id"]) if data.get("application_id") else None

class _BaseDirectMessage:
    def __init__(self, data: dict[str, _Any]) -> None:
        self.message_data = data
        """Either a passthrough message or a regular message. Unparsed due to complexity."""

    def is_passthrough(self) -> bool:
        """
        Checks whether the message is a passthrough message. If `False`, it is a regular message (with 2 additional fields: `lobby_id` and `channel`).
        
        ***Passthrough Message:**
        When both users in a direct message are provisional accounts,
        messages become "passthrough messages" that are only visible
        in-game and use a specialized structure.*
        """
        return "recipient_id" in self.message_data # A field unique to passthrough messages


class ApplicationAuthorized(_AnyEvent):
    """`APPLICATION_AUTHORIZED` is sent when the app is added to a server or user account."""
    def __init__(self, data: dict[str, _Any]) -> None:
        _integration_type = data.get("integration_type")
        self.is_guild_install = _integration_type == 0
        self.is_user_install = _integration_type == 1
        self.user: dict[str, _Any] = data["user"]
        self.scopes: list[str] = data["scopes"]
        self.guild: dict[str, _Any] | None = data.get("guild")

class ApplicationDeauthorized(_AnyEvent):
    """`APPLICATION_DEAUTHORIZED` is sent when the app is deauthorized by a user."""
    def __init__(self, data: dict[str, _Any]) -> None:
        self.user: dict[str, _Any] = data["user"]


class EntitlementCreate(_AnyEvent):
    """
    Represents the created entitlement object.

    `ENTITLEMENT_CREATE` is sent when an [entitlement](https://discord.com/developers/docs/resources/entitlement)
    is created when a user purchases or is otherwise granted one of your app's SKUs.
    Refer to the [Monetization documentation](https://discord.com/developers/docs/monetization/overview) for details.
    """
    def __init__(self, data: dict[str, _Any]) -> None:
        self.id = int(data["id"])
        self.sku_id = int(data["sku_id"])
        self.application_id = int(data["application_id"])
        self.user_id = int(data["user_id"]) if data.get("user_id") else None
        self.type: int = data["type"]
        self.deleted: bool = data["deleted"]
        self.starts_at = _iso_to_datetime(data["starts_at"]) if data.get("starts_at") else None
        self.ends_at = _iso_to_datetime(data["ends_at"]) if data.get("ends_at") else None
        self.guild_id = int(data["guild_id"]) if data.get("guild_id") else None
        self.consumed: bool | None = data.get("consumed")


class LobbyMessageCreate(_AnyEvent, _BaseLobbyMessage):
    """
    Represents the created lobby message object.

    `LOBBY_MESSAGE_CREATE` is sent when a message is created in a lobby.
    """

class LobbyMessageUpdate(_AnyEvent, _BaseLobbyMessage):
    """
    Represents the updated lobby message object.

    `LOBBY_MESSAGE_UPDATE` is sent when a message is updated in a lobby.
    """
    def __init__(self, data: dict[str, _Any]) -> None:
        super().__init__(data)
        self.edited_at = _iso_to_datetime(data["edited_timestamp"])
        self.created_at = _iso_to_datetime(data["timestamp"])

class LobbyMessageDelete(_AnyEvent):
    """`LOBBY_MESSAGE_DELETE` is sent when a message is deleted from a lobby."""
    def __init__(self, data: dict[str, _Any]) -> None:
        self.message_id = int(data["id"])
        self.lobby_id = int(data["lobby_id"])


class GameDirectMessageCreate(_AnyEvent, _BaseDirectMessage):
    """
    Represents the created direct message object.

    `GAME_DIRECT_MESSAGE_CREATE` is sent when a direct message is created while at least one user has an active Social SDK session.
    """
class GameDirectMessageUpdate(_AnyEvent, _BaseDirectMessage):
    """
    Represents the updated direct message object.

    `GAME_DIRECT_MESSAGE_UPDATE` is sent when a direct message is updated while at least one user has an active Social SDK session.
    """
class GameDirectMessageDelete(_AnyEvent, _BaseDirectMessage):
    """
    Represents the deleted direct message object.

    `GAME_DIRECT_MESSAGE_DELETE` is sent when a direct message is deleted while at least one user has an active Social SDK session.
    """


del _Any, _iso_to_datetime, _BaseDirectMessage, _BaseLobbyMessage # Disallow usage to prevent confusion