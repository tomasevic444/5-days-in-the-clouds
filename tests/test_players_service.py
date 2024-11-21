import pytest
from fastapi import HTTPException
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from app.models.player import Player
from app.services.player_service import create_player, get_player, update_player_in_db
from unittest.mock import patch
from uuid import uuid4

# Fixture for mock database
@pytest.fixture
def mock_db():
    db = TinyDB(storage=MemoryStorage)
    return db
@pytest.fixture
def set_test_db(mock_db):
    # Patch the global database used in your service
    with patch("app.services.player_service.players_table", mock_db.table("players")):
        yield
@pytest.fixture
def mock_player():
    return Player(id=str(uuid4()), nickname="Player1", team=None, elo=1000, hoursPlayed=50, wins=0, losses=0)
def test_create_player(mock_db, mock_player):
    players_table = mock_db.table("players")  # Use the mock database

    # Patch the global 'players_table' used in the function
    with patch("app.services.player_service.players_table", players_table):
        # First player creation
        create_player(mock_player)  # Call the function to test

        # Debug: Check database contents
        print("Database after first player creation:", players_table.all())

        # Assert the player was added to the mocked table
        assert len(players_table) == 1  # Check that one player is inserted
        assert players_table.all()[0]["nickname"] == mock_player.nickname

        # Ensure duplicate nickname raises error
        with pytest.raises(HTTPException) as exc_info:
            create_player(mock_player)  # Attempt duplicate creation

        # Debug: Check the raised exception
        print("Raised Exception:", exc_info.value)

        # Verify exception details
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Nickname already exists"


def test_get_player(mock_db, mock_player, set_test_db):
    players_table = mock_db.table("players")
    players_table.insert(mock_player.model_dump())  # Insert player
    player = get_player(mock_player.id)
    assert player.nickname == mock_player.nickname

    # Test non-existent player
    with pytest.raises(HTTPException):
        get_player(str(uuid4()))

def test_update_player_in_db(mock_db, mock_player, set_test_db):
    players_table = mock_db.table("players")
    players_table.insert(mock_player.model_dump())
    mock_player.hoursPlayed += 10
    update_player_in_db(mock_player)
    updated_player = players_table.search(Query().id == mock_player.id)[0]
    assert updated_player["hoursPlayed"] == mock_player.hoursPlayed
