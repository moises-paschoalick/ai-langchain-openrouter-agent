import uuid
from typing import List, Optional
from models.conversation import Conversation
from models.message import Message
from repositories.conversation_repository import ConversationRepository

class MemoryService:
    def __init__(self):
        self.repository = ConversationRepository()

    def create_thread(self) -> str:
        conversation_id = str(uuid.uuid4())
        self.repository.create(conversation_id)
        return conversation_id

    def add_message(self, conversation_id: str, role: str, content: str, tool_call_id: Optional[str] = None, name: Optional[str] = None) -> Optional[Message]:
        message = Message(role=role, content=content, tool_call_id=tool_call_id, name=name)
        conversation = self.repository.add_message(conversation_id, message)
        if conversation:
            return message
        return None

    def get_history(self, conversation_id: str) -> List[Message]:
        conversation = self.repository.get(conversation_id)
        if conversation:
            return conversation.messages
        return []

    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return self.repository.get(conversation_id)
