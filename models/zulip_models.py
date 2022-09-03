from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass()
class EditHistory:
    prev_content: Optional[str]
    prev_rendered_content: Optional[str]
    prev_rendered_content_version: Optional[str]
    prev_stream: Optional[int]
    prev_topic: Optional[str]
    stream: Optional[int]
    timestamp: int
    topic: Optional[str]
    user_id: int


@dataclass()
class Reaction:
    emoji_name: str
    emoji_code: str
    reaction_type: str
    user_id: int
    user: object  # deprecated


@dataclass()
class TopicLink:
    text: str
    url: str


@dataclass()
class Message:
    avatar_url: Optional[str]
    client: str
    content: str
    content_type: str
    display_recipient: Union[str, List[dict]]  # TODO: data class for display_recipient
    edit_history: Optional[List[EditHistory]]
    id: int
    is_me_message: bool
    last_edit_timestamp: Optional[int]
    reactions: List[Reaction]
    recipient_id: int
    sender_email: str
    sender_full_name: str
    sender_id: int
    sender_realm_str: str
    stream_id: Optional[int]
    subject: str  # will eventually be called topic
    submessages: List[str]  # experimental integrations
    timestamp: int
    topic_links: List[TopicLink]
    type: str


@dataclass()
class MessageEvent:
    id: int
    type: str
    message: Union[Message, dict]
    flags: List[str]

    def __post_init__(self):
        self.message = Message(**self.message)

@dataclass()
class RegisterQueueResponse:
    result: str
    msg: str
    queue_id: str
    zulip_version: str
    zulip_feature_level: int
    zulip_merge_base: str
    max_message_id: int # deprecated
    last_event_id: int

