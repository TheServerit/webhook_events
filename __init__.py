"""
### Made by [TheServerit](https://github.com/TheServerit)

FULL WEBHOOK EVENTS DOCUMENTATION: https://discord.com/developers/docs/events/webhook-events
"""

from ._internal.handler import Application, start_listening
from . import events

__all__ = ["Application", "events", "start_listening"]