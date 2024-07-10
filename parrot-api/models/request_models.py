from typing import Dict, Optional, Any

from pydantic import BaseModel


class AgentKickoffRequest(BaseModel):
    query: str
    headers: Optional[Dict[str, Any]] = None
    openapi: Dict[Any, Any]
    base_url: str

