from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class DynamicTool:
    name: str
    description: str
    parameters: Dict[str, Any] # JSON Schema for parameters
    strict: bool = False
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": self.strict
        }
