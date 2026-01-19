from typing import Dict, Any, List, Union
from langchain_core.messages import AIMessage
from langchain_core.agents import AgentAction, AgentFinish
from services.memory_service import MemoryService
from memory.conversation_memory import ConversationMemory
from agents.chat_agent import get_chat_agent_runnable # We will need to expose this
from models.message import Message

from services.dynamic_tool_service import DynamicToolService

class ChatService:
    def __init__(self):
        self.memory_service = MemoryService()
        self.dynamic_tool_service = DynamicToolService()
        # We don't initialize self.agent here anymore because we need to rebuild it 
        # with dynamic tools on each request (or at least check if they changed).
        # For simplicity, we will get the agent in process_prompt.

    def process_prompt(self, conversation_id: str, prompt: str) -> Dict[str, Any]:
        # Get dynamic tools
        extra_tools = self.dynamic_tool_service.get_langchain_tools()
        agent = get_chat_agent_runnable(extra_tools=extra_tools)
        # 0. Check for pending tool calls (Pre-check)
        history_msgs = self.memory_service.get_history(conversation_id)
        if history_msgs:
            last_msg = history_msgs[-1]
            if last_msg.role == "assistant" and last_msg.tool_call_id:
                # We have a pending tool call!
                print(f"Detected pending tool call: {last_msg.tool_call_id}")
                # Inject a cancellation message into the repository
                self.memory_service.add_message(
                    conversation_id,
                    "tool",
                    "Tool execution cancelled by user (new prompt received).",
                    tool_call_id=last_msg.tool_call_id,
                    name=last_msg.name or "tool"
                )

        # 1. Add User Message
        self.memory_service.add_message(conversation_id, "user", prompt)

        # 2. Get History
        history_msgs = self.memory_service.get_history(conversation_id)
        formatted_history = ConversationMemory.format_history(history_msgs)

        # 3. Invoke Agent
        # The agent expects 'input' and 'chat_history' (or whatever we defined in prompt)
        # We need to ensure the prompt matches.
        # Assuming the agent is a Runnable that returns AgentAction or AgentFinish
        # Or if it's a compiled graph (LangGraph), it's different.
        # For now assuming standard LangChain Agent Runnable.
        
        # We need to pass the *latest* input? 
        # If we use 'chat_history', the prompt usually expects 'input' to be the current query.
        # But we already added it to history.
        # So 'input' might be empty or we treat the last message as input?
        # Standard pattern: input is the new message, chat_history is everything BEFORE.
        
        # Let's adjust:
        # history_msgs includes the new prompt.
        # So chat_history should be history_msgs[:-1]
        # input should be history_msgs[-1].content
        
        chat_history = formatted_history[:-1]
        current_input = formatted_history[-1].content if formatted_history else prompt

        response = agent.invoke({
            "input": current_input,
            "chat_history": chat_history,
            # agent_scratchpad is handled by the agent if it's an AgentRunnable, 
            # but if we are manually running, we might need to manage it.
            # If we use create_openai_tools_agent, it expects intermediate_steps.
            # Since we are persisting steps in history, we might need to reconstruct intermediate_steps from history?
            # This is the tricky part of "Stateless Agent with Stateful Memory".
            # If we store Tool messages in history, we can pass them as chat_history!
            # OpenAI Tools Agent can handle ToolMessages in chat_history.
            # So we don't need 'agent_scratchpad' if we use the right prompt structure.
            # BUT our current prompt has 'agent_scratchpad'.
            # We should probably remove 'agent_scratchpad' and rely on 'chat_history' containing the tool sequence.
            # We need to pass intermediate_steps because create_openai_tools_agent expects it
            # to format agent_scratchpad. Since we are flattening history, we pass empty list.
            "intermediate_steps": []
        })

        # 4. Handle Response
        if isinstance(response, AgentFinish):
            # Final Answer
            self.memory_service.add_message(conversation_id, "assistant", response.return_values["output"])
            return {
                "type": "message",
                "content": response.return_values["output"]
            }
        elif isinstance(response, list):
             # Sometimes it returns a list of actions
             actions = response
             # We take the first one for simplicity or handle all
             action = actions[0]
             # It's a tool call
             # Save the intent (Assistant Message with Tool Call)
             # We need to serialize the tool call
             tool_call_id = getattr(action, "tool_call_id", "call_" + action.tool)
             
             self.memory_service.add_message(
                 conversation_id, 
                 "assistant", 
                 content="", # Empty content for tool call
                 tool_call_id=tool_call_id,
                 name=action.tool
             )
             
             return {
                 "type": "tool_call",
                 "tool": action.tool,
                 "tool_input": action.tool_input,
                 "tool_call_id": tool_call_id
             }
        elif isinstance(response, AgentAction):
             # Single action
             action = response
             tool_call_id = getattr(action, "tool_call_id", "call_" + action.tool)
             
             self.memory_service.add_message(
                 conversation_id, 
                 "assistant", 
                 content="", 
                 tool_call_id=tool_call_id,
                 name=action.tool
             )
             
             return {
                 "type": "tool_call",
                 "tool": action.tool,
                 "tool_input": action.tool_input,
                 "tool_call_id": tool_call_id
             }
        
        return {"error": "Unknown response type"}
