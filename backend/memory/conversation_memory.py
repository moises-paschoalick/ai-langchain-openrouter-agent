from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from models.message import Message

class ConversationMemory:
    @staticmethod
    def format_history(messages: List[Message]) -> List[BaseMessage]:
        formatted_messages = []
        for msg in messages:
            if msg.role == "user":
                formatted_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                if msg.tool_call_id:
                    # Reconstruct tool_calls so OpenAI knows this message triggered a tool
                    tool_calls = [{
                        "id": msg.tool_call_id,
                        "name": msg.name,
                        "args": {}, # We don't store args yet, hoping empty dict is accepted for history reconstruction
                        "type": "tool_call"
                    }]
                    formatted_messages.append(AIMessage(content=msg.content or "", tool_calls=tool_calls))
                else:
                    formatted_messages.append(AIMessage(content=msg.content))
            elif msg.role == "system":
                formatted_messages.append(SystemMessage(content=msg.content))
            elif msg.role == "tool":
                formatted_messages.append(ToolMessage(
                    content=msg.content,
                    tool_call_id=msg.tool_call_id or "unknown",
                    name=msg.name or "tool"
                ))
        return formatted_messages
