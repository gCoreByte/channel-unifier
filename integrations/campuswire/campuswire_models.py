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
  pseudoUser: PseudoUser
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
