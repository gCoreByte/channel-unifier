from enum import Enum

# TODO: map these out
EVENT_TYPES_RECEIVABLE = {
  "presence-changed",
  "user-points-changed",
  "hello",
  "message",
  "typing"
  }


class EventType(Enum):
    PresenceChanged = 'presence-changed'
    UserPointsChanged = 'user-points-changed'
    Hello = 'hello'
    World = 'world'
    Message = 'message' # TODO: how to differentiate between sent and received?
    Typing = 'typing'
    WallPostCreated = 'wall-post-created'



# All valid endpoints that we currently use
LOGIN_ENDPOINT = "https://api.campuswire.com/v1/auth/login"
WS_ENDPOINT = "wss://api.campuswire.com/v1/ws"
