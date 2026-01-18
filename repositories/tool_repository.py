from typing import List, Optional
from models.dynamic_tool import DynamicTool

class ToolRepository:
    _instance = None
    _tools: List[DynamicTool] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ToolRepository, cls).__new__(cls)
            cls._instance._tools = []
        return cls._instance

    def add_tool(self, tool: DynamicTool):
        # Check if tool exists, update if so
        for i, t in enumerate(self._tools):
            if t.name == tool.name:
                self._tools[i] = tool
                return
        self._tools.append(tool)

    def get_tool(self, name: str) -> Optional[DynamicTool]:
        for tool in self._tools:
            if tool.name == name:
                return tool
        return None

    def get_all_tools(self) -> List[DynamicTool]:
        return self._tools
