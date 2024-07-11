from enum import Enum
from typing import Dict, Any

from pydantic import BaseModel, Field


class AgentLogType(Enum):
    TOOL_IN = 'tool_in'
    TOOL_OUT = 'tool_out'
    INFO = 'info'
    ERROR = 'error'


class AgentLog(BaseModel):
    type: AgentLogType
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    terminal: bool = False
