
import base64
from typing import Set

import json
import aiohttp

from dacite import from_dict
from integrations.zulip.zulip_api import *
from utils.loop_handler import LoopHandler
from utils.url_helpers import replace_for_current
from integrations.zulip.zulip_models import *


def to_base64(email: str, api_key: str) -> bytes:
    to_encode = email + ":" + api_key
    return base64.b64encode(to_encode.encode('ascii'))


def generate_headers(email, api_key) -> dict:
    return {"Authorization": "Basic " + to_base64(email, api_key).decode('utf-8')}


# TODO: This would be more efficient with a linked list implementation
def filter_heartbeat(events: List[Event], event_types: Set) -> List[Event]:
    """Filters out heartbeat events - these are not relevant to us"""
    cleaned_events: List[Event] = []
    for event in events:
        if event.type in event_types:
            cleaned_events.append(event)
    return cleaned_events


def get_next_max_id(events: List[Event]) -> int:
    highest = -1
    for event in events:
        highest = max(event.id, highest)
    return highest


class Zulip:
    """Main wrapper of the Zulip integration"""

    def __init__(self, loop: LoopHandler, email: str, api_key: str, domain: str) -> None:
        self.last_event_id = None
        self.queue_id = None
        self.event_types = None
        self.loop = loop
        self.email = email
        self.api_key = api_key
        self.domain = domain
        self.headers = generate_headers(email, api_key)
        self.session = aiohttp.ClientSession(
            headers=generate_headers(self.email, self.api_key))

    def __del__(self):
        self.session.close()
        super()

    async def register_event_queue(self, event_types: set) -> None:
        """Registers a new event queue and saves the queue_id"""
        # Validate that we have a valid event
        if not event_types.issubset(EVENT_TYPES_SET):
            raise TypeError("Invalid event type added")
        self.event_types = event_types
        data = aiohttp.FormData()
        data.add_field('event_types', json.dumps(list(event_types)))
        data.add_field('all_public_streams', 'true',
                       content_type='multipart/form-data')
        async with self.session.post(
                replace_for_current(REGISTER_EVENT_QUEUE, self.domain), data=data
        ) as res:
            res_object: RegisterQueueResponse = from_dict(RegisterQueueResponse, await res.json())
            self.queue_id = res_object.queue_id
            self.last_event_id = res_object.last_event_id

    async def get_events(self) -> List[Event]:
        """Gets the newest events from the event queue"""
        params = {'queue_id': self.queue_id,
                  'last_event_id': self.last_event_id}
        async with self.session.get(replace_for_current(GET_EVENTS_FROM_QUEUE, self.domain), params=params) as res:
            res_object: QueueEventsResponse = from_dict(QueueEventsResponse, await res.json())
            self.last_event_id = get_next_max_id(res_object.events)
            return res_object.events

    async def run(self) -> None:
        """Main event loop task"""
        if not self.last_event_id or not self.queue_id:
            await self.register_event_queue({"message"})
        while True:
            try:
                events = await self.get_events()
                relevant_events = filter_heartbeat(events, self.event_types)
                if len(relevant_events) == 0:
                    # We received some irrelevant events, nothing to do
                    continue
                for event in relevant_events:
                    # TODO: create an EventHandler class, which would handle what event is sent to what function
                    message = event.message
                    await self.loop.send_to_all(data=message.content, integration_name="Zulip", username=message.sender_full_name, avatar_url=message.avatar_url)
            except Exception as e:
                print(e)
                self.session = aiohttp.ClientSession(
                    headers=generate_headers(self.email, self.api_key))
                await self.register_event_queue({"message"})
