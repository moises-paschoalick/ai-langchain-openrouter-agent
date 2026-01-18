from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from models.message import Message

@dataclass
class Conversation:
    id: str
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_message(self, message: Message):
        self.messages.append(message)
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
