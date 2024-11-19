from typing import Dict
from app.models.player import Player
from fastapi import HTTPException

# Simulated in-memory database
players_db: Dict[str, Player] = {}

def create_player(player: Player) -> Player:
    if player.nickname in players_db:
        raise HTTPException(status_code=400, detail="Nickname already exists")
    players_db[player.id] = player
    return player

def get_player(player_id: str) -> Player:
    player = players_db.get(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player