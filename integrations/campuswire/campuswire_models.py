from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass()
class Preferences:
  collapsedLeft: bool
  sendReadReceipts: bool
  reputationNoticeSeen: bool

@dataclass()
class PseudoUser:
  id: str
  firstName: str
  slug: str

@dataclass()
class User:
  id: str
  slug: str
  username: str
  firstName: str
  lastName: str
  email: str
  photo: str
  network: str
  verified: bool
  registered: bool
  genus: str
  preferences: Preferences
  created_at: str
  pseudoUser: Optional[PseudoUser]
  presence: object
  walkthrough: int

@dataclass()
class LoginResponseSmall:
  token: str
  expiresAt: str

@dataclass()
class LoginResponse(LoginResponseSmall):
  user: User
  refreshed: bool

@dataclass()
class Hello:
  id: int

@dataclass()
class World:
  replyTo: int

# TODO: Document events
@dataclass()
class PresenceChanged:
  user: User
  s: int

@dataclass()
class PresenceChangedSelf:
  status: str
  id: int

@dataclass()
class UserPointsChanged:
  id: str
  user: str
  giver: str
  group: str
  type: str # this should be an enum
  source: str
  points: int
  direction: str # this should be an enum
  createdAt: str
