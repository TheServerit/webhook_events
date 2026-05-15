from typing import TypedDict, NotRequired

from .user import User, UserData


__all__ = (
    "Application",
    "PartialApplication",
    "ApplicationInstallParams",
    "ApplicationIntegrationType"
)


class PartialApplicationData(TypedDict):
    id: str
    name: str
    icon: str | None
    description: str
    cover_image: NotRequired[str]
    bot: NotRequired[UserData]
    is_monetized: bool
    is_verified: bool
    is_discoverable: bool


class InstallParamsData(TypedDict):
    scopes: list[str]
    permissions: str


class ApplicationIntegrationTypeData(TypedDict):
    oauth2_install_params: NotRequired[InstallParamsData]


class ApplicationData(PartialApplicationData):
    rpc_origins: NotRequired[list[str]]
    bot_public: bool
    bot_require_code_grant: bool
    terms_of_service_url: NotRequired[str]
    privacy_policy_url: NotRequired[str]
    verify_key: str
    primary_sku_id: NotRequired[str]
    #flags: NotRequired[int] Either nonexistent or 0 for possible contexts (clip data, activity launch message)
    integration_types_config: NotRequired[ApplicationIntegrationTypeData]


class PartialApplication:
    __slots__ = (
        "id",
        "name",
        "icon",
        "description",
        "cover_image",
        "bot",
        "is_monetized",
        "is_verified",
        "is_discoverable"
    )

    def __init__(self, data: PartialApplicationData) -> None:
        self.id = data["id"]
        self.name = data["name"]
        self.icon = data["icon"]
        self.description = data["description"]
        self.cover_image = data.get("cover_image")
        self.bot = User(bot) if (bot := data.get("bot")) else None
        self.is_monetized = data["is_monetized"]
        self.is_verified = data["is_verified"]
        self.is_discoverable = data["is_discoverable"]


class ApplicationInstallParams:
    __slots__ = ("scopes", "permissions")

    def __init__(self, data: InstallParamsData) -> None:
        self.scopes = data["scopes"]
        self.permissions = data["permissions"]


class ApplicationIntegrationType:
    __slots__ = ("oauth2_install_params",)

    def __init__(self, data: ApplicationIntegrationTypeData) -> None:
        self.oauth2_install_params = ApplicationInstallParams(params) if (params := data.get("oauth2_install_params")) else None


class Application(PartialApplication):
    __slots__ = (
        "rpc_origins",
        "is_public",
        "bot_requires_code_grant",
        "terms_of_service_url",
        "privacy_policy_url",
        "verify_key",
        "primary_sku_id",
        "integration_types_config",
    )

    def __init__(self, data: ApplicationData) -> None:
        super().__init__(data)
        self.rpc_origins = data.get("rpc_origins")
        self.is_public = data["bot_public"]
        self.bot_requires_code_grant = data["bot_require_code_grant"]
        self.terms_of_service_url = data.get("terms_of_service_url")
        self.privacy_policy_url = data.get("privacy_policy_url")
        self.verify_key = data["verify_key"]
        self.primary_sku_id = int(sku_id) if (sku_id := data.get("primary_sku_id")) else None
        self.integration_types_config = ApplicationIntegrationType(config) if (config := data.get("integration_types_config")) else None

    def __repr__(self) -> str:
        return f"<Application id={self.id} name={self.name!r}>"
