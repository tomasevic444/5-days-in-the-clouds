from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4
from app.models.player import Player

class Team(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    teamName: str
    players: List[Player]