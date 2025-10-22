# A Python wrapper for Discord's [Webhook Events](https://discord.com/developers/docs/events/webhook-events#webhook-events).

**In the code, each variable, class or function that is meant to be used has a docstring of its documentation.**

*All unparsed `dict` attributes are the standard Discord API objects of their name, unless said otherwise.*

## Step-by-step walkthrough
### 1. Create your application object
```python
from webhook_events import Application

app = Application(...)
```
`Application` takes two arguments:
1. url_path (str):<br>
The URL path to the webhook endpoint you have specified on *your application's Developer Portal page -> 'Webhooks'*. For example, if your endpoint is *https://quackbots.xyz/webhook1*, then `url_path` should be */webhook1* (it depends on your server/file configuration).

2. verify_key (str):<br>
Your application's public key, used to verify Discord's request signature.<br>
You can find this on *your application's Developer Portal page -> 'General Information'*.

### 2. Register an event listener
```python
from webhook_events import Application, events
from datetime import datetime

app = Application(...)

@app.on_event(events.ApplicationAuthorized)
async def foo(event: events.ApplicationAuthorized, time: datetime):
  ...
```
`on_event` is the decorator for registering a function to call when an event of the specified type is received.<br><br>
This decorator takes a single *positional* argument:<br>
An event object (class variable) of your choice (e.g. `events.ApplicationAuthorized`).

The function you use with this decorator must be a coroutine function (`async def`) that takes two arguments, in this order:
- An event object (e.g. `events.ApplicationAuthorized`) identical to the one passed to the decorator.
- A `datetime.datetime` object, representing the time when the event occurred.

### 3. Start listening for webhook events
```python
from webhook_events import Application, events, start_listening

app = Application(...)

# Implement event handler(s)

start_listening(host="0.0.0.0", port=8080, applications=[app])
```
`start_listening` takes four *keyword* arguments:<br>
1. host (str):<br>The host to run the application on (e.g. `0.0.0.0`)
2. port (int):<br>The port to run the application on.
3. applications (list[Application]):<br>A list of `Application` objects to handle webhook events for.
4. basic_log (bool):<br>Whether to log the following:<br>
    - (info) Received a PING.<br>
    - (info) Received an event.<br>
    - (warning) Signature verification failed.<br>
    - (warning) Received an event without data (should never happen).

### Full example
```python
from webhook_events import Application, events, start_listening
from datetime import datetime


app1 = Application(url_path="/webhook1", verify_key="banana")
app2 = Application(url_path="/webhook2", verify_key="apple")


@app1.on_event(events.ApplicationAuthorized)
async def foo(event: events.ApplicationAuthorized, time: datetime):
  username = event.user["username"]
  print(f"{username} authorized app1 at {time}!")


@app2.on_event(events.ApplicationDeauthorized)
async def foo(event: events.ApplicationDeauthorized, time: datetime):
  username = event.user["username"]
  print(f"{username} deauthorized app2 at {time}.")


start_listening(host="0.0.0.0", port=8080, applications=[app1, app2])
```
