from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class Match(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    team1Id: str
    team2Id: str
    winningTeamId: Optional[str] = None  # Null for draw
    duration: int 