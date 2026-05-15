from typing import TYPE_CHECKING
from abc import ABC

from ..utils import snowflake_to_datetime

if TYPE_CHECKING:
    from datetime import datetime


MENTION_TYPES = {
    "role": '@&',
    "user": '@',
    "channel": '#'
}


class Snowflake(ABC):
    if TYPE_CHECKING:
        id: int

    @property
    def created_at(self) -> datetime:
        """
        The time when the object was created by Discord.

        *Note: this is not the same as `message.sent_at`.*
        """
        return snowflake_to_datetime(self.id)


class MentionableSnowflake(ABC):
    if TYPE_CHECKING:
        id: int
        
    @property
    def mention(self) -> str:
        return f"<{MENTION_TYPES[self.__class__.__name__.lower()]}{self.id}>"
    
    @property
    def created_at(self) -> datetime:
        """
        The time when the object was created by Discord.

        *Note: this is not the same as `message.sent_at`.*
        """
        return snowflake_to_datetime(self.id)
