from typing import Dict, Optional
from models.conversation import Conversation
from models.message import Message

class ConversationRepository:
    _instance = None
    _storage: Dict[str, Conversation] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConversationRepository, cls).__new__(cls)
        return cls._instance

    def create(self, conversation_id: str) -> Conversation:
        conversation = Conversation(id=conversation_id)
        self._storage[conversation_id] = conversation
        return conversation

    def get(self, conversation_id: str) -> Optional[Conversation]:
        return self._storage.get(conversation_id)

    def add_message(self, conversation_id: str, message: Message) -> Optional[Conversation]:
        conversation = self.get(conversation_id)
        if conversation:
            conversation.add_message(message)
            return conversation
        return None
