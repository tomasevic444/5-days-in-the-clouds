import pytest
from unittest.mock import patch
from fastapi import HTTPException
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
from uuid import uuid4

from app.models.team import Team
from app.models.player import Player
from app.services.team_service import create_team, get_team_by_id, update_team_in_db
from app.services.player_service import get_player

# Fixtures
@pytest.fixture
def mock_db():
    db = TinyDB(storage=MemoryStorage)
    return db

@pytest.fixture
def mock_players(mock_db):
    players_table = mock_db.table("players")
    players = [
        Player(id=str(uuid4()), nickname=f"Player{i+1}", team=None, elo=1000, hoursPlayed=10, wins=0, losses=0)
        for i in range(5)
    ]
    for player in players:
        players_table.insert(player.model_dump())
    return players

@pytest.fixture
def mock_teams_table(mock_db):
    return mock_db.table("teams")

# Test: Create Team
def test_create_team(mock_db, mock_players):
    teams_table = mock_db.table("teams")
    players_table = mock_db.table("players")

    with patch("app.services.team_service.teams_table", teams_table), \
         patch("app.services.team_service.players_table", players_table), \
         patch("app.services.team_service.get_player", side_effect=lambda pid: next(p for p in mock_players if p.id == pid)):

        # Create a team
        team_name = "Team Alpha"
        player_ids = [player.id for player in mock_players]
        team = create_team(team_name, player_ids)

        # Assertions
        assert team.teamName == team_name
        assert len(team.players) == 5
        assert len(teams_table) == 1
        assert teams_table.all()[0]["teamName"] == team_name

        # Check that players have been assigned to the team
        for player_id in player_ids:
            player_data = players_table.get(Query().id == player_id)
            assert player_data["team"] == team.id

        # Test duplicate team name
        with pytest.raises(HTTPException) as exc_info:
            create_team(team_name, player_ids)
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == "Team name must be unique"

# Test: Get Team by ID
def test_get_team_by_id(mock_db, mock_players):
    teams_table = mock_db.table("teams")

    # Create a mock team
    team = Team(id=str(uuid4()), teamName="Team Bravo", players=mock_players)
    teams_table.insert(team.model_dump())

    with patch("app.services.team_service.teams_table", teams_table):
        # Fetch the team by ID
        fetched_team = get_team_by_id(team.id)

        # Assertions
        assert fetched_team.teamName == "Team Bravo"
        assert len(fetched_team.players) == 5

        # Test non-existent team
        with pytest.raises(HTTPException) as exc_info:
            get_team_by_id(str(uuid4()))
        assert exc_info.value.status_code == 404

# Test: Update Team in DB
def test_update_team_in_db(mock_db, mock_players):
    teams_table = mock_db.table("teams")

    # Create a mock team
    team = Team(id=str(uuid4()), teamName="Team Charlie", players=mock_players)
    teams_table.insert(team.model_dump())

    updated_player = mock_players[0]
    updated_player.nickname = "UpdatedNickname"

    with patch("app.services.team_service.teams_table", teams_table):
        # Update player in team
        update_team_in_db(team.id, updated_player)

        # Fetch updated team
        updated_team = get_team_by_id(team.id)

        # Assertions
        assert updated_team.players[0].nickname == "UpdatedNickname"
