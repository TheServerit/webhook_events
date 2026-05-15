__all__ = ("Color",)


class Color:
    __slots__ = ("r", "g", "b")
    
    """
    A simple class for holding a Discord color value.

    ---
    Calling `int()` on this will return the color integer value (0xRRGGBB).

    Calling `str()` on this will return the color hex string value, without the '#' (e.g. 'FFAABB').

    This class supports equality checks (== and !=). Only works with instances of this class.
    """
    def __init__(self, value: int, /) -> None:
        self.r = (value >> 16) & 0xFF
        self.g = (value >> 8) & 0xFF
        self.b = value & 0xFF

    def to_rgb(self) -> tuple[int, int, int]:
        """Return the color as an RGB tuple."""
        return self.r, self.g, self.b
    
    @classmethod
    def from_hex(cls, hex_value: str, /) -> Color:
        hex_value = hex_value.lstrip("#")

        if len(hex_value) != 6:
            raise ValueError("Hex color must be in RRGGBB format")

        try:
            value = int(hex_value, 16)
        except ValueError:
            raise ValueError("Invalid hex color string")

        return cls(value)

    def __int__(self) -> int:
        return (self.r << 16) | (self.g << 8) | self.b

    def __str__(self) -> str:
        return f"{self.r:02X}{self.g:02X}{self.b:02X}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return (
                self.r == other.r
                and self.g == other.g
                and self.b == other.b
            )
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"<Color r={self.r} g={self.g} b={self.b}>"
