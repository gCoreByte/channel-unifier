from enum import Enum

# TODO: map these out
EVENT_TYPES_SET = {"message"}


class EventType(Enum):
    MESSAGE = 'message'
    HEARTBEAT = 'heartbeat'


# All valid endpoints that we currently use
REGISTER_EVENT_QUEUE = "https://corebyte.zulipchat.com/api/v1/register"
GET_EVENTS_FROM_QUEUE = "https://corebyte.zulipchat.com/api/v1/events"
