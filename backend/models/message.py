from dataclasses import dataclass, field
from typing import Optional, Literal
from datetime import datetime

@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool"]
    content: str
    tool_call_id: Optional[str] = None
    name: Optional[str] = None  # For tool outputs (the name of the tool)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "role": self.role,
            "content": self.content,
            "tool_call_id": self.tool_call_id,
            "name": self.name,
            "timestamp": self.timestamp.isoformat()
        }
