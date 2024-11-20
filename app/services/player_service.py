from fastapi import HTTPException
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from app.models.player import Player
from uuid import uuid4

# Initialize the in-memory database
db = TinyDB(storage=MemoryStorage)  # You can replace MemoryStorage with a file-based storage for persistence
players_table = db.table("players")
PlayerQuery = Query()

def create_player(player: Player) -> Player:
    # Check if nickname already exists
    if players_table.search(PlayerQuery.nickname == player.nickname):
        raise HTTPException(status_code=400, detail="Nickname already exists")

    # Insert player into the database
    player_dict = player.dict()
    players_table.insert(player_dict)
    return player

def get_player(player_id: str) -> Player:
    # Fetch player by ID
    result = players_table.search(PlayerQuery.id == player_id)
    if not result:
        raise HTTPException(status_code=404, detail="Player not found")
    return Player(**result[0])

def get_all_players() -> list[Player]:
    # Fetch all players
    return [Player(**record) for record in players_table.all()]