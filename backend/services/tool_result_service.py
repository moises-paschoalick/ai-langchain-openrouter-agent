from typing import Optional
from services.memory_service import MemoryService
from models.message import Message

class ToolResultService:
    def __init__(self):
        self.memory_service = MemoryService()

    def process_tool_result(self, conversation_id: str, tool_name: str, tool_output: str, tool_call_id: Optional[str] = None) -> Optional[Message]:
        # If tool_call_id is not provided, try to find it in the last message
        if not tool_call_id:
            history = self.memory_service.get_history(conversation_id)
            if history:
                last_msg = history[-1]
                if last_msg.role == "assistant" and last_msg.tool_call_id:
                    tool_call_id = last_msg.tool_call_id

        # Persist the tool result as a message
        message = self.memory_service.add_message(
            conversation_id=conversation_id,
            role="tool",
            content=tool_output,
            tool_call_id=tool_call_id,
            name=tool_name
        )
        return message
