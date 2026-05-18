from typing import Any, TypedDict, NotRequired

from .objects.message import Message, MessageData, MessageActivity, MessageActivityData
from .objects.enums import try_enum, MessageType, EntitlementType, IntegrationType
from .objects.application import PartialApplication, PartialApplicationData
from .objects.channel import Channel, ChannelData
from .objects.guild import Guild, GuildData
from .objects.user import User, UserData
from .objects.flags import MessageFlags

from .utils import iso_to_datetime


__all__ = (
    "ApplicationAuthorized",
    "ApplicationDeauthorized",
    "EntitlementCreate",
    "EntitlementUpdate",
    "EntitlementDelete",
    "LobbyMessageCreate",
    "LobbyMessageUpdate",
    "LobbyMessageDelete",
    "GameDirectMessageCreate",
    "GameDirectMessageUpdate",
    "GameDirectMessageDelete"
)


class EventData(TypedDict): ...


class ApplicationAuthorizedData(EventData):
    integration_type: NotRequired[int]
    user: UserData
    scopes: list[str]
    guild: NotRequired[GuildData]


class ApplicationDeauthorizedData(EventData):
    user: UserData


class EntitlementData(EventData):
    id: str
    sku_id: str
    application_id: str
    user_id: NotRequired[str]
    type: int
    deleted: bool
    starts_at: str | None
    ends_at: str | None
    guild_id: NotRequired[str]
    consumed: NotRequired[bool]


class LobbyMessageData(EventData):
    id: str
    type: int
    content: str
    lobby_id: str
    channel_id: str
    author: UserData
    metadata: NotRequired[dict[str, Any]]
    flags: int
    application_id: NotRequired[str]


class LobbyMessageUpdateData(LobbyMessageData):
    edited_timestamp: str
    timestamp: str


class LobbyMessageDeleteData(EventData):
    id: str
    lobby_id: str


class PassthroughMessageData(EventData):
    id: str
    type: int
    content: str
    author: UserData
    flags: int
    application_id: str
    channel: ChannelData
    activity: NotRequired[MessageActivityData]
    application: NotRequired[PartialApplicationData]


class PassthroughMessage:
    """
    **Passthrough Messages:**

    When both users in a direct message are provisional accounts,
    messages become "passthrough messages" that are only visible
    in-game and use a specialized structure.
    """
    __slots__ = (
        "id",
        "type",
        "content",
        "author",
        "flags",
        "application_id",
        "channel",
        "activity",
        "application"
    )

    def __init__(self, data: PassthroughMessageData) -> None:
        self.id = data["id"]
        self.type = try_enum(MessageType, data["type"])
        self.content = data["content"]
        self.author = User(data["author"])
        self.flags = MessageFlags(data["flags"])
        self.application_id = data["application_id"]
        self.channel = Channel(data["channel"])
        self.activity = MessageActivity(activity) if (activity := data.get("activity")) else None
        self.application = PartialApplication(application) if (application := data.get("application")) else None


class Event:
    def __init__(self, data: EventData) -> None: ...


class BaseLobbyMessage:
    __slots__ = (
        "id",
        "type",
        "content",
        "lobby_id",
        "channel_id",
        "author",
        "metadata",
        "flags",
        "application_id"
    )

    def __init__(self, data: LobbyMessageData | LobbyMessageUpdateData) -> None:
        self.id = int(data["id"])
        self.type = try_enum(MessageType, data["type"])
        self.content = data["content"]
        self.lobby_id = int(data["lobby_id"])
        self.channel_id = int(data["channel_id"])
        self.author = User(data["author"])
        self.metadata = data.get("metadata")
        self.flags = MessageFlags(data["flags"])
        self.application_id = int(application_id) if (application_id := data.get("application_id")) else None


class BaseDirectMessage:
    __slots__ = ("message",)

    def __init__(self, data: MessageData | PassthroughMessageData) -> None:
        if "application_id" in data and "embeds" not in data: # manipulate fields to determine message type
            self.message = PassthroughMessage(data)
        else:
            self.message = Message(data)

    def is_passthrough(self) -> bool:
        """Checks whether the message is a passthrough message (`types.PassthroughMessage`). If not, it is a regular message (`types.Message`)."""
        return isinstance(self.message, PassthroughMessage)


class ApplicationAuthorized(Event):
    """`APPLICATION_AUTHORIZED` is sent when the app is added to a server or user account."""

    __slots__ = (
        "user",
        "scopes",
        "guild",
        "integration_type"
    )

    def __init__(self, data: ApplicationAuthorizedData) -> None:
        self.user = User(data["user"])
        self.scopes = data["scopes"]
        self.guild = Guild(guild) if (guild := data.get("guild")) else None
        self.integration_type = try_enum(IntegrationType, integration_type) if (integration_type := data.get("integration_type")) else None

    @property
    def is_user_install(self) -> bool:
        return self.integration_type == IntegrationType.USER or (self.integration_type is None and self.guild is None)
    
    @property
    def is_guild_install(self) -> bool:
        return self.integration_type == IntegrationType.GUILD or (self.integration_type is None and self.guild is not None)


class ApplicationDeauthorized(Event):
    """`APPLICATION_DEAUTHORIZED` is sent when the app is deauthorized by a user."""

    __slots__ = ("user",)

    def __init__(self, data: ApplicationDeauthorizedData) -> None:
        self.user = User(data["user"])


class BaseEntitlement(Event):
    __slots__ = (
        "id",
        "sku_id",
        "application_id",
        "user_id",
        "type",
        "deleted",
        "starts_at",
        "ends_at",
        "guild_id",
        "consumed"
    )

    def __init__(self, data: EntitlementData) -> None:
        self.id = int(data["id"])
        self.sku_id = int(data["sku_id"])
        self.application_id = int(data["application_id"])
        self.user_id = int(user_id) if (user_id := data.get("user_id")) else None
        self.type = try_enum(EntitlementType, data["type"])
        self.deleted = data["deleted"]
        self.starts_at = iso_to_datetime(data["starts_at"]) if data["starts_at"] is not None else None
        self.ends_at = iso_to_datetime(data["ends_at"]) if data["ends_at"] is not None else None
        self.guild_id = int(guild_id) if (guild_id := data.get("guild_id")) else None
        self.consumed = bool(data.get("consumed"))


class EntitlementCreate(BaseEntitlement):
    """
    Represents the created entitlement object.

    `ENTITLEMENT_CREATE` is sent when an entitlement is created when a user purchases or is otherwise granted one of your app's SKUs.
    """


class EntitlementUpdate(BaseEntitlement):
    """
    Represents the updated entitlement object.

    `ENTITLEMENT_UPDATE` is sent when an entitlement is updated.
    """


class EntitlementDelete(BaseEntitlement):
    """
    Represents the deleted entitlement object.

    `ENTITLEMENT_DELETE` is sent when an entitlement is deleted.
    """


class LobbyMessageCreate(BaseLobbyMessage, Event):
    """
    Represents the created lobby message object.

    `LOBBY_MESSAGE_CREATE` is sent when a message is created in a lobby.
    """


class LobbyMessageUpdate(BaseLobbyMessage, Event):
    """
    Represents the updated lobby message object, with additional `created_at` and `edited_at` timestamps.

    `LOBBY_MESSAGE_UPDATE` is sent when a message is updated in a lobby.
    """

    __slots__ = ("edited_at", "created_at")

    def __init__(self, data: LobbyMessageUpdateData) -> None:
        super().__init__(data)
        self.edited_at = iso_to_datetime(data["edited_timestamp"])
        self.created_at = iso_to_datetime(data["timestamp"])


class LobbyMessageDelete(Event):
    """`LOBBY_MESSAGE_DELETE` is sent when a message is deleted from a lobby."""

    __slots__ = ("message_id", "lobby_id")

    def __init__(self, data: LobbyMessageDeleteData) -> None:
        self.message_id = int(data["id"])
        self.lobby_id = int(data["lobby_id"])


class GameDirectMessageCreate(BaseDirectMessage, Event):
    """
    `GAME_DIRECT_MESSAGE_CREATE` is sent when a direct message is created while at least one user has an active Social SDK session.

    Access the message using `.message`, which can be either a regular message (`types.Message`) or a *passthrough message* (`types.PassthroughMessage`):

    > *When both users in a direct message are provisional accounts, messages become "Passthrough Messages" that are only visible in-game and use a specialized structure.*
    
    For your convenience, you can check whether the message is a passthrough message using `.is_passthrough()`.
    """


class GameDirectMessageUpdate(BaseDirectMessage, Event):
    """
    `GAME_DIRECT_MESSAGE_UPDATE` is sent when a direct message is updated while at least one user has an active Social SDK session.

    Access the message using `.message`, which can be either a regular message (`types.Message`) or a *passthrough message* (`types.PassthroughMessage`):

    > *When both users in a direct message are provisional accounts, messages become "Passthrough Messages" that are only visible in-game and use a specialized structure.*
    
    For your convenience, you can check whether the message is a passthrough message using `.is_passthrough()`.
    """


class GameDirectMessageDelete(BaseDirectMessage, Event):
    """
    `GAME_DIRECT_MESSAGE_DELETE` is sent when a direct message is deleted while at least one user has an active Social SDK session.

    Access the message using `.message`, which can be either a regular message (`types.Message`) or a *passthrough message* (`types.PassthroughMessage`):

    > *When both users in a direct message are provisional accounts, messages become "Passthrough Messages" that are only visible in-game and use a specialized structure.*
    
    For your convenience, you can check whether the message is a passthrough message using `.is_passthrough()`.
    """
