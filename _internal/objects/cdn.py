from typing import Literal


__all__ = ("Asset",)


type CDNPath = Literal[
    "icons",
    "avatars",
    "banners",
    "clan-badges",
    "avatar-decoration-presets",
    "splashes",
    "discovery-splashes",
    "role-icons"
]


class Asset:
    __slots__ = ("asset_hash", "url")
    
    def __init__(self, asset_hash: str, obj_id: int | None, cdn_path: CDNPath | None) -> None:
        self.asset_hash = asset_hash

        format = 'gif' if self.is_animated() else 'png'

        id_part = None
        if obj_id is not None:
            id_part = f'{obj_id}/'

        if cdn_path is None:
            self.url = f"https://discord.com/assets/{self.asset_hash}.{format}"
        else:
            self.url = f"https://cdn.discordapp.com/{cdn_path}/{id_part}{self.asset_hash}.{format}"

    def is_animated(self) -> bool:
        return self.asset_hash.startswith('a_')

    def __repr__(self) -> str:
        return f"<Asset hash={self.asset_hash}>"
