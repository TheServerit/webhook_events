from collections.abc import Callable, Coroutine
from typing import TypeVar

from fastapi import FastAPI, Request, Response
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from .utils import iso_to_datetime
from .. import events

from datetime import datetime
import logging
import inspect
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [\033[92m%(levelname)s\033[0m] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


AnyEvent = TypeVar("AnyEvent", bound=events._AnyEvent)
"""An event object from the `events` module."""

HandlerFunc = Callable[[AnyEvent, datetime], Coroutine[None, None, None]]
"""
A coroutine function (`async def`) with no returns (returns `None`) that takes
two arguments in this order: an event object and a `datetime.datetime` object.
"""

HandlerFuncDecorator = Callable[[HandlerFunc[AnyEvent]], HandlerFunc[AnyEvent]]
"""A decorator that takes `HandlerFunc` and returns `HandlerFunc`."""

 
class Application:
    """
    An application object to handle webhook events for. Used in `start_listening`.

    ---
    Args:
        url_path (str):
            The URL path to the webhook endpoint that you have specified on *your application's Developer Portal page -> 'Webhooks'*.

            For example, if your endpoint is *`https://quackbots.xyz/webhook1`*, then `url_path` should be *`/webhook1`* (it depends on your server/file configuration).
        verify_key (str):
            Your application's public key, used to verify Discord's request signature.
            You can find this on *your application's Developer Portal page -> 'General Information'*.
    """
    def __init__(self, url_path: str, verify_key: str):
        self.url_path = url_path
        self.verify_key = verify_key
        self._event_handlers: dict[str, HandlerFunc] = {}
        self._EVENTS_MAP = {
            "APPLICATION_AUTHORIZED": events.ApplicationAuthorized,
            "APPLICATION_DEAUTHORIZED": events.ApplicationDeauthorized,
            "ENTITLEMENT_CREATE": events.EntitlementCreate,
            "LOBBY_MESSAGE_CREATE": events.LobbyMessageCreate,
            "LOBBY_MESSAGE_UPDATE": events.LobbyMessageUpdate,
            "LOBBY_MESSAGE_DELETE": events.LobbyMessageDelete,
            "GAME_DIRECT_MESSAGE_CREATE": events.GameDirectMessageCreate,
            "GAME_DIRECT_MESSAGE_UPDATE": events.GameDirectMessageUpdate,
            "GAME_DIRECT_MESSAGE_DELETE": events.GameDirectMessageDelete
        }

    def on_event(self, event_type: type[AnyEvent], /) -> HandlerFuncDecorator[AnyEvent]:
        """

        A decorator for registering a function to call when an event of the specified type is received.

        This decorator takes a single positional argument:
        an event object (class variable) of your choice (e.g. `events.ApplicationAuthorized`).

        ---

        The function you use with this decorator must be a coroutine function (`async def`) that takes two arguments, in this order:
        - An event object (e.g. `events.ApplicationAuthorized`) identical to the one passed to the decorator.
        - A `datetime.datetime` object, representing the time when the event occurred.

        ---
        Example usage:

        ```
        from webhook events import Application, events
        from datetime import datetime

        app = Application(...) # Implement your application object

        @app.on_event(events.ApplicationAuthorized)
        async def my_handler_function(event: events.ApplicationAuthorized, time: datetime):
            ...
        ```
        """
        if not (isinstance(event_type, type) and issubclass(event_type, events._AnyEvent)):
            raise TypeError(f"Expected an event object (class variable), got '{type(event_type).__name__}'.")
        
        def decorator(func: HandlerFunc[AnyEvent]) -> HandlerFunc[AnyEvent]:
            if not inspect.iscoroutinefunction(func):
                raise TypeError(f"Expected a coroutine function (async def), got '{type(func).__name__}'.")
            
            sig = inspect.signature(func)
            params = sig.parameters
            if len(params) != 2:
                raise TypeError(f"Expected 2 arguments, got {len(params)}.")
            
            if func in self._event_handlers.values():
                raise RuntimeError(f"Function '{func.__name__}' is already registered. Decorator-stacking is not supported.")

            reversed_map = {v: k for k, v in self._EVENTS_MAP.items()} # Reverse from {event_type: event_obj} to {event_obj: event_type}
            self._event_handlers[reversed_map[event_type]] = func
            return func

        return decorator

    async def _dispatch_event(self, event_type: str, event_data: dict, timestamp: datetime) -> None:
        """If an event handler is registered for the event type received, call the handler function with the needed arguments."""
        handler = self._event_handlers.get(event_type)
        if handler:
            event_cls = self._EVENTS_MAP[event_type]
            event = event_cls(event_data)
            await handler(event, timestamp)


def start_listening(host: str, port: int, applications: list[Application], basic_log: bool = True) -> None:
    """
    Starts listening for webhook events for the endpoints of the given application/s.

    *Note: `WARNING`, `ERROR` and `CRITICAL` logs are enabled for `uvicorn` (the library who runs the server).*

    ---
    Args:
        host (str): The host to run the application on (e.g. `0.0.0.0`)
        port (int): The port to run the application on.
        applications (list[Application]):  
            A list of `Application` objects to handle webhook events for.
        basic_log (bool): Whether to log the following:
            (info) Received a PING.
            (info) Received an event.
            (warning) Signature verification failed.
            (warning) Received an event without data (should never happen).
            
    ---
    Example usage:

    ```
    from webhook_events import Application, start_listening
    from datetime import datetime

    app1 = Application(...) # Implement your application object

    # Implement your event handlers

    start_listening(host="0.0.0.0", port=8080, applications=[app1])
    ```
    """

    app = FastAPI()

    async def handle_request(request: Request, application: Application) -> Response | None:

        verify_key = VerifyKey(bytes.fromhex(application.verify_key))

        body = await request.body()
        body_str = body.decode("utf-8")

        req_signature = request.headers.get("X-Signature-Ed25519", "")
        req_timestamp = request.headers.get("X-Signature-Timestamp", "")

        if req_signature and req_timestamp:
            try:
                verify_key.verify(f'{req_timestamp}{body_str}'.encode(), bytes.fromhex(req_signature))
            except BadSignatureError:
                if basic_log:
                    logging.warning(f"[{application.url_path}] Failed to verify Discord's request signature (invalid signature). Signature:\n{req_signature}")

                return Response(status_code=401, content="invalid request signature")
        else:
            if basic_log:
                logging.warning(f"[{application.url_path}] Failed to verify Discord's request signature (either signature or timestamp is missing).")

            return Response(status_code=401, content="invalid request signature")
        
        payload = json.loads(body_str)

        if payload["type"] == 0:
            if basic_log:
                logging.info(f"[{application.url_path}] Received a PING.")
            
            return Response(status_code=204, headers={"Content-Type": "application/json"})
        
        else:
            event: dict = payload["event"]
            event_type: str = event["type"]
            data = event.get("data", {})

            if not data:
                if basic_log:
                    logging.warning(f"[{application.url_path}] Ignoring an event without data: {event_type}")
            else:
                timestamp = iso_to_datetime(event["timestamp"])
                await application._dispatch_event(event_type=event_type, event_data=data, timestamp=timestamp)

                if basic_log:
                    logging.info(f"[{application.url_path}] Received an event: {event_type}")

        return Response(status_code=204)
        
    for application in applications:
        async def listener(request: Request, app_instance=application):
            return await handle_request(request, app_instance)
        app.add_api_route(application.url_path, listener, methods=["POST"])
        
    logging.info(f"Started. (Press CTRL+C to quit)")

    import uvicorn
    uvicorn.run(app=app, host=host, port=port, log_level="warning")