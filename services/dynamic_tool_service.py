from typing import List, Dict, Any
from models.dynamic_tool import DynamicTool
from repositories.tool_repository import ToolRepository
from langchain.tools import StructuredTool
from pydantic import create_model
from langchain_core.tools import Tool

class DynamicToolService:
    def __init__(self):
        self.repository = ToolRepository()

    def register_tool(self, name: str, description: str, parameters: Dict[str, Any], strict: bool = False) -> DynamicTool:
        tool = DynamicTool(name=name, description=description, parameters=parameters, strict=strict)
        self.repository.add_tool(tool)
        return tool

    def get_all_tools(self) -> List[DynamicTool]:
        return self.repository.get_all_tools()

    def get_langchain_tools(self) -> List[Tool]:
        """
        Converts stored DynamicTools into LangChain Tools.
        Since these tools are executed externally, we provide a dummy function.
        However, for OpenAI Tools Agent, we need to provide the schema.
        """
        dynamic_tools = self.repository.get_all_tools()
        lc_tools = []
        
        for dt in dynamic_tools:
            # We can use a simpler approach for OpenAI Tools:
            # Just create a Tool with the right name and description, 
            # and attach the args_schema if possible, OR
            # use StructuredTool.from_function with a dummy func and the schema.
            
            # Constructing a Pydantic model from the JSON schema is complex dynamically.
            # But create_openai_tools_agent handles "tools" which can be:
            # - BaseTool
            # - Dict (OpenAI format)
            
            # So we can just return the dict format expected by OpenAI!
            # BUT ChatAgent expects a list of tools to bind.
            
            # Let's try to create a StructuredTool with a dummy function.
            # The agent will call it, we intercept the call in ChatService (via AgentAction),
            # so the function body doesn't matter much, BUT the schema does.
            
            # Actually, if we return a list of tools to `create_openai_tools_agent`,
            # it converts them to OpenAI format.
            
            # A simpler way: define a dummy function that takes **kwargs
            def dummy_func(**kwargs):
                return "Tool called externally"
            
            # We need to set the name and description
            # And ideally the args_schema.
            # Since we have the JSON schema for parameters, we can try to pass it directly
            # if we were using the low-level API.
            
            # Workaround: Create a Tool that has the `args` property matching our schema.
            # Or better, use the `tool` decorator approach but dynamically? No.
            
            # Let's use the `StructuredTool` but we need a Pydantic model for args_schema.
            # Generating Pydantic model from JSON Schema at runtime:
            # This is possible but adds complexity.
            
            # ALTERNATIVE:
            # We can create a class that inherits from BaseTool and overrides `get_input_schema`.
            
            # For now, let's try to pass the tool definition as a DICT if LangChain supports it.
            # Looking at `create_openai_tools_agent` source (or docs), it calls `bind_tools`.
            # `bind_tools` supports dicts!
            
            tool_dict = {
                "type": "function",
                "function": {
                    "name": dt.name,
                    "description": dt.description,
                    "parameters": dt.parameters
                }
            }
            if dt.strict:
                tool_dict["function"]["strict"] = True
                
            lc_tools.append(tool_dict)
            
        return lc_tools
