from typing import TypedDict, NotRequired

from .flags import EmbedFlags, EmbedMediaFlags
from .enums import try_enum, EmbedType
from .color import Color

from ..utils import iso_to_datetime


__all__ = (
    "Embed",
    "EmbedFooter",
    "EmbedMedia",
    "EmbedProvider",
    "EmbedAuthor",
    "EmbedField"
)


class EmbedFooterData(TypedDict):
    text: str
    icon_url: NotRequired[str]
    proxy_icon_url: NotRequired[str]


class EmbedMediaData(TypedDict):
    url: str
    proxy_url: NotRequired[str]
    height: NotRequired[int]
    width: NotRequired[int]
    content_type: NotRequired[str]
    placeholder: NotRequired[str]
    placeholder_version: NotRequired[int]
    description: NotRequired[str]
    flags: NotRequired[int]


class EmbedProviderData(TypedDict, total=False):
    name: str
    url: str


class EmbedAuthorData(TypedDict):
    name: str
    url: str | None
    icon_url: str | None
    proxy_icon_url: str | None


class EmbedFieldData(TypedDict):
    name: str
    value: str
    inline: NotRequired[bool]


class EmbedData(TypedDict, total=False):
    title: str
    type: str
    description: str
    url: str
    timestamp: str
    color: int
    footer: EmbedFooterData
    image: EmbedMediaData
    thumbnail: EmbedMediaData
    video: EmbedMediaData
    provider: EmbedProviderData
    author: EmbedAuthorData
    fields: list[EmbedFieldData]


class EmbedFooter:
    __slots__ = ("text", "icon_url", "proxy_icon_url")

    def __init__(self, data: EmbedFooterData) -> None:
        self.text = data["text"]
        self.icon_url = data.get("icon_url")
        self.proxy_icon_url = data.get("proxy_icon_url")


class EmbedMedia:
    __slots__ = (
        "url",
        "proxy_url",
        "height",
        "width",
        "content_type",
        "thumbhash_placeholder",
        "thumbhash_placeholder_version",
        "description",
        "flags",
    )

    def __init__(self, data: EmbedMediaData) -> None:
        self.url = data["url"]
        self.proxy_url = data.get("proxy_url")
        self.height = data.get("height")
        self.width = data.get("width")
        self.content_type = data.get("content_type")
        self.thumbhash_placeholder = data.get("placeholder")
        self.thumbhash_placeholder_version = data.get("placeholder_version")
        self.description = data.get("description")
        self.flags = EmbedMediaFlags(flags) if (flags := data.get("flags")) else None


class EmbedProvider:
    __slots__ = ("name", "url")

    def __init__(self, data: EmbedProviderData) -> None:
        self.name = data.get("name")
        self.url = data.get("url")


class EmbedAuthor:
    __slots__ = ("name", "url", "icon_url", "proxy_icon_url")

    def __init__(self, data: EmbedAuthorData) -> None:
        self.name = data["name"]
        self.url = data.get("url")
        self.icon_url = data.get("icon_url")
        self.proxy_icon_url = data.get("proxy_icon_url")


class EmbedField:
    __slots__ = ("name", "value", "is_inline")

    def __init__(self, data: EmbedFieldData) -> None:
        self.name = data["name"]
        self.value = data["value"]
        self.is_inline = data.get("inline")


class Embed:
    __slots__ = (
        "title",
        "type",
        "description",
        "url",
        "timestamp",
        "color",
        "footer",
        "image",
        "thumbnail",
        "video",
        "provider",
        "author",
        "fields",
        "flags",
    )

    def __init__(self, data: EmbedData) -> None:
        self.title = data.get("title")
        self.type = try_enum(EmbedType, embed_type) if (embed_type := data.get("type")) else None
        self.description = data.get("description")
        self.url = data.get("url")
        self.timestamp = iso_to_datetime(timestamp) if (timestamp := data.get("timestamp")) else None
        self.color = Color(color) if (color := data.get("color")) else None
        self.footer = EmbedFooter(footer) if (footer := data.get("footer")) else None
        self.image = EmbedMedia(image) if (image := data.get("image")) else None
        self.thumbnail = EmbedMedia(thumbnail) if (thumbnail := data.get("thumbnail")) else None
        self.video = EmbedMedia(video) if (video := data.get("video")) else None
        self.provider = EmbedProvider(provider) if (provider := data.get("provider")) else None
        self.author = EmbedAuthor(author) if (author := data.get("author")) else None
        self.fields = [EmbedField(field) for field in data.get("fields", [])]
        self.flags = EmbedFlags(flags) if (flags := data.get("flags")) else None

    def __repr__(self) -> str:
        return f"<Embed type={self.type!r} title={self.title!r}>"
