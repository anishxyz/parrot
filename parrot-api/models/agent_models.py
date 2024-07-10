from enum import Enum
from typing import Dict, Any

from pydantic import BaseModel, Field


class AgentLog(BaseModel):
    type: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    terminal: bool = False


class AgentLogType(Enum):
    TOOL_IN = 'tool_in'
    TOOL_OUT = 'tool_out'
    INFO = 'info'
    ERROR = 'error'
