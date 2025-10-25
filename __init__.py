"""
### A Python wrapper for Discord's [Webhook Events](https://discord.com/developers/docs/events/webhook-events#webhook-events).

Copyright: 2025-present [TheServerit](https://github.com/TheServerit)
Licensed under MIT, see LICENSE for more details.
"""

from ._internal.handler import Application, start_listening
from . import events

__all__ = ["Application", "events", "start_listening"]