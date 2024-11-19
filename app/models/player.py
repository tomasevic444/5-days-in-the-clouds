from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class Player(BaseModel):
    id: str= Field(default_factory=lambda: str(uuid4()))
    nickname: str
    wins: int = 0
    losses: int = 0
    elo: float = 0
    hoursPlayed: int = 0
    team: Optional[str] = None
    ratingAdjustment: int = 50