from typing import Any, TypedDict, NotRequired, Literal
from collections.abc import Callable, Coroutine

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from datetime import datetime
import logging
import inspect
import json

import uvicorn

from .utils import iso_to_datetime
from . import events


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [\033[92m%(levelname)s\033[0m] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


EventName = Literal[
    "APPLICATION_AUTHORIZED",
    "APPLICATION_DEAUTHORIZED",
    "ENTITLEMENT_CREATE",
    "ENTITLEMENT_UPDATE",
    "ENTITLEMENT_DELETE",
    "LOBBY_MESSAGE_CREATE",
    "LOBBY_MESSAGE_UPDATE",
    "LOBBY_MESSAGE_DELETE",
    "GAME_DIRECT_MESSAGE_CREATE",
    "GAME_DIRECT_MESSAGE_UPDATE",
    "GAME_DIRECT_MESSAGE_DELETE"
]


class InnerEventPayload(TypedDict):
    type: EventName
    timestamp: str
    data: NotRequired[events.EventData]


class OuterEventPayload(TypedDict):
    version: int
    application_id: str
    type: int
    event: NotRequired[InnerEventPayload]


type HandlerFunc[EventT: events.Event] = Callable[[EventT, datetime], Coroutine[Any, Any, Any]]
# A coroutine function (async def) that takes two arguments in this order: an event object and a datetime.datetime object.

type HandlerFuncDecorator[EventT: events.Event] = Callable[[HandlerFunc[EventT]], HandlerFunc[EventT]]
# A decorator that takes HandlerFunc and returns HandlerFunc."""


EVENTS_MAP: dict[EventName, type[events.Event]] = {
    "APPLICATION_AUTHORIZED": events.ApplicationAuthorized,
    "APPLICATION_DEAUTHORIZED": events.ApplicationDeauthorized,
    "ENTITLEMENT_CREATE": events.EntitlementCreate,
    "ENTITLEMENT_UPDATE": events.EntitlementUpdate,
    "ENTITLEMENT_DELETE": events.EntitlementDelete,
    "LOBBY_MESSAGE_CREATE": events.LobbyMessageCreate,
    "LOBBY_MESSAGE_UPDATE": events.LobbyMessageUpdate,
    "LOBBY_MESSAGE_DELETE": events.LobbyMessageDelete,
    "GAME_DIRECT_MESSAGE_CREATE": events.GameDirectMessageCreate,
    "GAME_DIRECT_MESSAGE_UPDATE": events.GameDirectMessageUpdate,
    "GAME_DIRECT_MESSAGE_DELETE": events.GameDirectMessageDelete
}


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

    __slots__ = ("url_path", "verify_key", "_event_handlers")

    def __init__(self, url_path: str, verify_key: str):
        self.url_path = url_path
        self.verify_key = verify_key
        self._event_handlers: dict[str, HandlerFunc[Any]] = {}

    def on_event[EventT: events.Event](self, event: type[EventT], /) -> HandlerFuncDecorator[EventT]:
        """

        A decorator for registering a function to call when an event of the specified type is received.

        This decorator takes a single positional argument:
        an event *class type* of your choice (e.g. `events.ApplicationAuthorized`).

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
        if not issubclass(event, events.Event): # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(f"Expected an event class type (e.g. 'events.ApplicationAuthorized'), got '{type(event).__name__}'.")
        
        def decorator(func: HandlerFunc[EventT]) -> HandlerFunc[EventT]:
            if not inspect.iscoroutinefunction(func):
                raise TypeError(f"Expected a coroutine function (async def), got '{type(func).__name__}'.")
            
            sig = inspect.signature(func)
            params = sig.parameters
            if len(params) != 2:
                raise TypeError(f"Expected 2 arguments, got {len(params)}.")
            
            if func in self._event_handlers.values():
                raise RuntimeError(f"Function '{func.__name__}' is already registered. Decorator-stacking is not supported.")

            reversed_map = {v: k for k, v in EVENTS_MAP.items()} # Reverse from {event_type: event_obj} to {event_obj: event_type}
            self._event_handlers[reversed_map[event]] = func
            return func

        return decorator

    async def _dispatch_event(self, *, name: EventName, data: events.EventData, timestamp: datetime) -> None:
        """If an event handler is registered for the event type received, call the handler function with the needed arguments."""
        handler = self._event_handlers.get(name)
        if handler:
            event_cls = EVENTS_MAP[name]
            event = event_cls(data)
            await handler(event, timestamp)

    def __repr__(self) -> str:
        return f"<Application url_path={self.url_path!r}>"


def start_listening(*, host: str, port: int, applications: list[Application], basic_log: bool = True) -> None:
    """
    Starts listening for webhook events for the endpoints of the given application/s.

    *Note: `WARNING`, `ERROR` and `CRITICAL` logs are always enabled for uvicorn (library that runs the server).*

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

    app = Starlette()

    async def handle_request(request: Request, application: Application) -> Response:

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
        
        payload: OuterEventPayload = json.loads(body_str)

        if payload["type"] == 0:
            if basic_log:
                logging.info(f"[{application.url_path}] Received a PING.")
            
            return Response(status_code=204, headers={"Content-Type": "application/json"})
        
        else:
            event = payload.get("event")

            if event:
                name = event["type"]
                data = event.get("data")

                if not data:
                    if basic_log:
                        logging.warning(f"[{application.url_path}] Ignoring an event without data: {name}")
                else:
                    timestamp = iso_to_datetime(event["timestamp"])
                    await application._dispatch_event(name=name, data=data, timestamp=timestamp) # pyright: ignore[reportPrivateUsage]

                    if basic_log:
                        logging.info(f"[{application.url_path}] Received an event: {name}")
            else:
                logging.warning(f"[{application.url_path}] Ignoring a payload without an event.")

        return Response(status_code=204)
        
    for application in applications:
        
        async def listener(request: Request) -> Response:
            return await handle_request(request, application)
        
        app.add_route(application.url_path, listener, methods=["POST"])
        
    logging.info(f"Starting to listen for webhook events on {host}:{port}.")

    uvicorn.run(app=app, host=host, port=port, log_level="warning")
