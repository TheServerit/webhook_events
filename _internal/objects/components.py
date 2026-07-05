from typing import TypedDict, NotRequired, Literal, TYPE_CHECKING

from .enums import try_enum, ComponentType, ButtonStyle, ChannelType, SeparatorSpacing
from .emoji import PartialEmoji, PartialEmojiData
from .flags import UnfurledMediaItemFlags
from .color import Color

if TYPE_CHECKING:
    from collections.abc import Iterator


__all__ = (
    "UnknownComponent",
    "ComponentsWrapper",
    "StringSelect",
    "UserSelect",
    "RoleSelect",
    "MentionableSelect",
    "ChannelSelect",
    "ActionRow",
    "Button",
    "Section",
    "TextDisplay",
    "UnfurledMediaItem",
    "Thumbnail",
    "MediaGalleryItem",
    "MediaGallery",
    "FileComponent",
    "Separator",
    "Container",
    "MessageComponentType"
)


type ComponentData = (
    ActionRowData |
    ActionRowChildTypeData |
    SectionData |
    SectionChildTypeData |
    SectionAccessoryTypeData |
    MediaGalleryData |
    FileComponentData |
    SeparatorData |
    ContainerData
)

type Select = StringSelect | UserSelect | RoleSelect | MentionableSelect | ChannelSelect
type SelectTypeData = StringSelectData | UserSelectData | RoleSelectData | MentionableSelectData | ChannelSelectData
type DefaultValueSelectTypeData = UserSelectData | RoleSelectData | MentionableSelectData | ChannelSelectData

type ActionRowChildType = Button | Select
type ActionRowChildTypeData = ButtonData | SelectTypeData

type SectionChildType = TextDisplay
type SectionAccessoryType = Button | Thumbnail
type SectionChildTypeData = TextDisplayData
type SectionAccessoryTypeData = ButtonData | ThumbnailData

type ContainerChildType = ActionRow | TextDisplay | Section | MediaGallery | Separator | FileComponent
type ContainerChildTypeData = ActionRowData | TextDisplayData | SectionData | MediaGalleryData | SeparatorData | FileComponentData

type ContainerChildData = (
    ActionRowData |
    TextDisplayData |
    MediaGalleryData |
    FileComponentData |
    SectionData |
    SelectTypeData |
    SeparatorData
)


type MessageComponentType = (
    ActionRowChildType |
    SectionChildType |
    ActionRow |
    Section |
    MediaGallery |
    FileComponent |
    Container
)

type MessageComponentData = (
    ActionRowChildTypeData |
    TextDisplayData |
    SectionData |
    ActionRowData |
    MediaGalleryData |
    FileComponentData |
    ContainerData
)


class ActionRowData(TypedDict):
    type: Literal[1]
    id: NotRequired[int]
    components: list[ActionRowChildTypeData]


class ButtonData(TypedDict):
    type: Literal[2]
    id: NotRequired[int]
    style: int
    label: NotRequired[str]
    emoji: NotRequired[PartialEmojiData]
    custom_id: NotRequired[str]
    sku_id: NotRequired[str]
    url: NotRequired[str]
    disabled: NotRequired[bool]


class SelectOptionData(TypedDict):
    label: str
    value: str
    description: NotRequired[str]
    emoji: NotRequired[PartialEmojiData]
    default: NotRequired[bool]


class BaseSelectData(TypedDict):
    id: NotRequired[int]
    custom_id: str
    placeholder: NotRequired[str]
    min_values: NotRequired[int]
    max_values: NotRequired[int]
    required: NotRequired[bool]
    disabled: NotRequired[bool]


class StringSelectData(BaseSelectData):
    type: Literal[3]
    options: list[SelectOptionData]


class DefaultValueData(TypedDict):
    id: str
    type: str


class DefaultValueSelectData(BaseSelectData):
    default_values: NotRequired[list[DefaultValueData]]


class UserSelectData(DefaultValueSelectData):
    type: Literal[5]


class RoleSelectData(DefaultValueSelectData):
    type: Literal[6]


class MentionableSelectData(DefaultValueSelectData):
    type: Literal[7]


class ChannelSelectData(DefaultValueSelectData):
    type: Literal[8]
    channel_types: NotRequired[list[int]]


class SectionData(TypedDict):
    type: Literal[9]
    id: NotRequired[int]
    components: list[SectionChildTypeData]
    accessory: list[SectionAccessoryTypeData]


class TextDisplayData(TypedDict):
    type: Literal[10]
    id: NotRequired[int]
    content: str


class UnfurledMediaItemData(TypedDict):
    url: str
    proxy_url: NotRequired[str]
    height: NotRequired[int | None]
    width: NotRequired[int | None]
    placeholder: NotRequired[str]
    placeholder_version: NotRequired[int]
    content_type: NotRequired[str]
    flags: NotRequired[int]
    attachment_id: NotRequired[str]


class ThumbnailData(TypedDict):
    type: Literal[11]
    id: NotRequired[int]
    media: UnfurledMediaItemData
    description: NotRequired[str | None]
    spoiler: NotRequired[bool]


class MediaGalleryItemData(TypedDict):
    media: UnfurledMediaItemData
    description: NotRequired[str | None]
    spoiler: NotRequired[bool]


class MediaGalleryData(TypedDict):
    type: Literal[12]
    id: NotRequired[int]
    items: list[MediaGalleryItemData]


class FileComponentData(TypedDict):
    type: Literal[13]
    id: NotRequired[int]
    file: UnfurledMediaItemData
    spoiler: NotRequired[bool]
    name: NotRequired[str]
    size: NotRequired[int]


class SeparatorData(TypedDict):
    type: Literal[14]
    id: NotRequired[int]
    divider: NotRequired[bool]
    spacing: NotRequired[int]


class ContainerData(TypedDict):
    type: Literal[17]
    id: NotRequired[int]
    components: list[ContainerChildData]
    accent_color: NotRequired[int]
    spoiler: NotRequired[bool]


class BaseComponent:
    __slots__ = ("type", "id")

    def __init__(self, data: ComponentData) -> None:
        self.type = try_enum(ComponentType, data["type"])
        self.id = data.get("id")

    def is_v2(self) -> bool:
        """Whether this component is part of Components V2."""
        return self.type.value in (1, 9, 10, 11, 12, 13, 14, 17)

    def __repr__(self) -> str:
        return f"<Component type={self.type!r} id={self.id!r}>"
    

class UnknownComponent:
    __slots__ = ("type", "id")

    def __init__(self, data: MessageComponentData) -> None:
        self.type = try_enum(ComponentType, data["type"])
        self.id = data.get("id")

    def is_v2(self) -> bool:
        return self.type.value in (1, 9, 10, 11, 12, 13, 14, 17)

    def __repr__(self) -> str:
        return f"<UnknownComponent type={self.type!r} id={self.id!r}>"


def resolve_message_component(data: MessageComponentData) -> MessageComponentType | UnknownComponent:
    match data["type"]:
        case 1:
            return ActionRow(data)
        case 2:
            return Button(data)
        case 3:
            return StringSelect(data)
        case 5:
            return UserSelect(data)
        case 6:
            return RoleSelect(data)
        case 7:
            return MentionableSelect(data)
        case 8:
            return ChannelSelect(data)
        case 9:
            return Section(data)
        case 10:
            return TextDisplay(data)
        case 12:
            return MediaGallery(data)
        case 13:
            return FileComponent(data)
        case 17:
            return Container(data)
        case _:
            return UnknownComponent(data)
        

def is_supported_component(data: ComponentData) -> bool:
    return data["type"] in (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17)
        

def resolve_action_row_component(data: ActionRowChildTypeData) -> ActionRowChildType:
    match data["type"]:
        case 2:
            return Button(data)
        case 3:
            return StringSelect(data)
        case 5:
            return UserSelect(data)
        case 6:
            return RoleSelect(data)
        case 7:
            return MentionableSelect(data)
        case 8:
            return ChannelSelect(data)
        case _:
            raise NotImplementedError


def resolve_section_component(data: SectionChildTypeData) -> SectionChildType:
    match data["type"]:
        case 10:
            return TextDisplay(data)
        case _:
            raise NotImplementedError
        

def resolve_accessory_component(data: SectionAccessoryTypeData) -> SectionAccessoryType:
    match data["type"]:
        case 2:
            return Button(data)
        case 11:
            return Thumbnail(data)
        case _:
            raise NotImplementedError
        

def resolve_container_component(data: ContainerChildData) -> ContainerChildType:
    match data["type"]:
        case 1:
            return ActionRow(data)
        case 10:
            return TextDisplay(data)
        case 9:
            return Section(data)
        case 12:
            return MediaGallery(data)
        case 13:
            return FileComponent(data)
        case 14:
            return Separator(data)
        case _:
            raise NotImplementedError


class ActionRow(BaseComponent):
    __slots__ = ("children",)

    def __init__(self, data: ActionRowData) -> None:
        super().__init__(data)
        self.children = [resolve_action_row_component(component) for component in data["components"] if is_supported_component(component)]


class Button(BaseComponent):
    __slots__ = (
        "style",
        "label",
        "emoji",
        "custom_id",
        "sku_id",
        "url",
        "is_disabled"
    )

    def __init__(self, data: ButtonData) -> None:
        self.style = try_enum(ButtonStyle, data["style"])
        self.label = data.get("label")
        self.emoji = PartialEmoji(emoji) if (emoji := data.get("emoji")) else None
        self.custom_id = data.get("custom_id")
        self.sku_id = data.get("sku_id")
        self.url = data.get("url")
        self.is_disabled = data.get("disabled", False)
        

class SelectOption:
    __slots__ = (
        "label",
        "value",
        "description",
        "emoji",
        "default"
    )

    def __init__(self, data: SelectOptionData) -> None:
        self.label = data["label"]
        self.value = data["value"]
        self.description = data.get("description")
        self.emoji = PartialEmoji(emoji) if (emoji := data.get("emoji")) else None
        self.default = data.get("default", False)


class BaseSelect(BaseComponent):
    __slots__ = (
        "custom_id",
        "placeholder",
        "min_values",
        "max_values",
        "is_required",
        "is_disabled"
    )

    def __init__(self, data: SelectTypeData) -> None:
        super().__init__(data)
        self.custom_id = data["custom_id"]
        self.placeholder = data.get("placeholder")
        self.min_values = data.get("min_values")
        self.max_values = data.get("max_values")
        self.is_required = data.get("required", False)
        self.is_disabled = data.get("disabled", False)


class DefaultValueSelect(BaseSelect):
    __slots__ = ("default_values",)

    def __init__(self, data: DefaultValueSelectTypeData) -> None:
        super().__init__(data)
        self.default_values = data.get("default_values")


class StringSelect(BaseSelect):
    __slots__ = ("options",)

    def __init__(self, data: StringSelectData) -> None:
        super().__init__(data)
        self.options = [SelectOption(option) for option in data["options"]]


class UserSelect(DefaultValueSelect):
    __slots__ = ()

    if TYPE_CHECKING:
        def __init__(self, data: UserSelectData) -> None: ...


class RoleSelect(DefaultValueSelect):
    __slots__ = ()

    if TYPE_CHECKING:
        def __init__(self, data: RoleSelectData) -> None: ...


class MentionableSelect(DefaultValueSelect):
    __slots__ = ()
    
    if TYPE_CHECKING:
        def __init__(self, data: MentionableSelectData) -> None: ...


class ChannelSelect(DefaultValueSelect):
    __slots__ = ("channel_types",)
    
    def __init__(self, data: ChannelSelectData) -> None:
        super().__init__(data)
        self.channel_types = [try_enum(ChannelType, channel_type) for channel_type in data.get("channel_types", [])]


class Section(BaseComponent):
    __slots__ = ("children", "accessory")

    def __init__(self, data: SectionData) -> None:
        super().__init__(data)
        self.children = [resolve_section_component(component) for component in data["components"] if is_supported_component(component)]
        self.accessory = [resolve_accessory_component(component) for component in data["accessory"] if is_supported_component(component)]


class TextDisplay(BaseComponent):
    __slots__ = ("content",)

    def __init__(self, data: TextDisplayData) -> None:
        super().__init__(data)
        self.content = data["content"]


class UnfurledMediaItem:
    __slots__ = (
        "url",
        "proxy_url",
        "height",
        "width",
        "thumbhash_placeholder",
        "thumbhash_placeholder_version",
        "content_type",
        "flags",
        "attachment_id"
    )

    def __init__(self, data: UnfurledMediaItemData) -> None:
        self.url = data["url"]
        self.proxy_url = data.get("proxy_url")
        self.height = data.get("height")
        self.width = data.get("width")
        self.thumbhash_placeholder = data.get("placeholder")
        self.thumbhash_placeholder_version = data.get("placeholder_version")
        self.content_type = data.get("content_type")
        self.flags = UnfurledMediaItemFlags(flags) if (flags := data.get("flags")) else None
        self.attachment_id = int(attachment_id) if (attachment_id := data.get("attachment_id")) else None


class Thumbnail(BaseComponent):
    __slots__ = ("media", "description", "spoiler")

    def __init__(self, data: ThumbnailData) -> None:
        super().__init__(data)
        self.media = UnfurledMediaItem(data["media"])
        self.description = data.get("description")
        self.spoiler = data.get("spoiler", False)


class MediaGalleryItem:
    __slots__ = ("media", "description", "spoiler")

    def __init__(self, data: MediaGalleryItemData) -> None:
        self.media = UnfurledMediaItem(data["media"])
        self.description = data.get("description")
        self.spoiler = data.get("spoiler", False)


class MediaGallery(BaseComponent):
    __slots__ = ("items",)

    def __init__(self, data: MediaGalleryData):
        super().__init__(data)
        self.items = [MediaGalleryItem(item) for item in data["items"]]


class FileComponent(BaseComponent):
    __slots__ = ("file", "spoiler", "name", "size")

    def __init__(self, data: FileComponentData) -> None:
        super().__init__(data)
        self.file = UnfurledMediaItem(data["file"])
        self.spoiler = data.get("spoiler", False)
        self.name = data.get("name")
        self.size = data.get("size")


class Separator(BaseComponent):
    __slots__ = ("is_visible", "spacing")

    def __init__(self, data: SeparatorData) -> None:
        super().__init__(data)
        self.is_visible = data.get("divider", False)
        self.spacing = SeparatorSpacing(spacing) if (spacing := data.get("spacing")) else SeparatorSpacing.SMALL


class Container(BaseComponent):
    __slots__ = ("children", "accent_color", "spoiler")

    def __init__(self, data: ContainerData) -> None:
        super().__init__(data)
        self.children = [resolve_container_component(component) for component in data["components"] if is_supported_component(component)]
        self.accent_color = Color(accent_color) if (accent_color := data.get("accent_color")) else None
        self.spoiler = data.get("spoiler", False)


class ComponentsWrapper:
    __slots__ = ("children",)

    def __init__(self) -> None:
        self.children: list[MessageComponentType] = []

    def walk_children(self) -> Iterator[BaseComponent]:
        """Iterates recursively through all children components."""
        for child in self.children:
            yield child

            if hasattr(child, "walk_children"):
                yield from child.walk_children() # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]

    def is_components_v2(self) -> bool:
        """Whether this wrapper contains components that are part of Components V2."""
        return any(child.is_v2() for child in self.walk_children())
    
    @classmethod
    def _from_message_components(cls, components: list[MessageComponentType | UnknownComponent]) -> ComponentsWrapper:
        new = cls()

        new_components = [c for c in components if not isinstance(c, UnknownComponent)]
        new.children = new_components

        return new
