from fastapi import APIRouter
from app.services.player_service import create_player, get_player
from app.models.player import Player

router = APIRouter()

@router.post("/create", response_model=Player)
def create_new_player(player: Player):
    return create_player(player)

@router.get("/{player_id}", response_model=Player)
def get_player_by_id(player_id: str):
    return get_player(player_id)