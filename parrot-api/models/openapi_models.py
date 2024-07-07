from typing import List, Optional

from pydantic import BaseModel


class Asset(BaseModel):
    name: str
    dependents: List[str]
    inputs: List[str]
    route: str
    method: str
    tag: Optional[str]

