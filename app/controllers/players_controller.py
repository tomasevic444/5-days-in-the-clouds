from fastapi import APIRouter
from app.services.player_service import create_player, get_player, get_all_players
from app.models.player import Player
from typing import List
router = APIRouter()

@router.post("/create", response_model=Player)
def create_new_player(player: Player):
    return create_player(player)

@router.get("/{player_id}", response_model=Player)
def get_player_by_id(player_id: str):
    return get_player(player_id)

@router.get("/", response_model=List[Player])  
def get_all_players_endpoint():
    """
    Retrieve all players from the database.
    """
    return get_all_players()