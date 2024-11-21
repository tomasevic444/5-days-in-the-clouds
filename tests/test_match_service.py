import pytest
from unittest.mock import patch
from uuid import uuid4
from app.models.match import Match
from app.models.player import Player
from app.models.team import Team
from app.services.match_service import create_match
from fastapi import HTTPException

# Fixtures
@pytest.fixture
def mock_teams():
    players_team1 = [
        Player(id=str(uuid4()), nickname=f"Player1_{i}", team=None, elo=1000, hoursPlayed=100, wins=0, losses=0)
        for i in range(5)
    ]
    players_team2 = [
        Player(id=str(uuid4()), nickname=f"Player2_{i}", team=None, elo=1100, hoursPlayed=200, wins=0, losses=0)
        for i in range(5)
    ]

    team1 = Team(id=str(uuid4()), teamName="Team1", players=players_team1)
    team2 = Team(id=str(uuid4()), teamName="Team2", players=players_team2)

    return team1, team2

@pytest.fixture
def mock_match(mock_teams):
    team1, team2 = mock_teams
    return Match(
        id=str(uuid4()),
        team1Id=team1.id,
        team2Id=team2.id,
        duration=2,
        winningTeamId=team1.id,  # Team1 wins
    )

# Mock for update_player_in_db
@pytest.fixture
def mock_update_player():
    with patch("app.services.match_service.update_player_in_db") as mock:
        yield mock

# Mock for get_team_by_id
@pytest.fixture
def mock_get_team(mock_teams):
    team1, team2 = mock_teams
    with patch("app.services.match_service.get_team_by_id", side_effect=lambda tid: team1 if tid == team1.id else team2):
        yield

# Tests
def test_create_match_success(mock_match, mock_teams, mock_get_team, mock_update_player):
    team1, team2 = mock_teams

    with patch("app.services.match_service.matches_table") as mock_matches_table:
        # Create the match
        created_match = create_match(mock_match)

        # Assert match creation
        assert created_match.team1Id == team1.id
        assert created_match.team2Id == team2.id
        assert created_match.winningTeamId == team1.id

        # Validate match saved in the database
        mock_matches_table.insert.assert_called_once_with(mock_match.model_dump())

        # Validate player updates
        for player in team1.players + team2.players:
            mock_update_player.assert_any_call(player)

def test_create_match_invalid_duration(mock_match):
    mock_match.duration = 0  # Invalid duration

    with pytest.raises(HTTPException) as exc_info:
        create_match(mock_match)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Duration must be at least 1 hour"



def test_create_match_invalid_winning_team(mock_match, mock_get_team):
    # Invalid winningTeamId
    mock_match.winningTeamId = str(uuid4())

    with pytest.raises(HTTPException) as exc_info:
        create_match(mock_match)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid winningTeamId"

def test_update_team_stats(mock_teams, mock_update_player):
    team1, team2 = mock_teams
    opponent_elo = sum(player.elo for player in team2.players) / len(team2.players)

    # Call update_team_stats for the winning team
    from app.services.match_service import update_team_stats
    update_team_stats(team1, team2, S=1, duration=2)

    # Assert Elo adjustments and win updates
    for player in team1.players:
        # Replicate the logic from update_team_stats (with rounding in the exponent)
        E = 1 / (1 + 10 ** (round((opponent_elo - player.elo) / 400)))
        K = 50 if player.hoursPlayed < 500 else 40  # Determine K-factor
        adjustment = round(K * (1 - E))
        expected_elo = player.elo  # The player's Elo was already updated inside update_team_stats

        # Assert Elo and wins
        mock_player = mock_update_player.call_args_list[0][0][0]  # Get the player passed to the mock
        assert mock_player.elo == expected_elo, f"Expected {expected_elo}, got {mock_player.elo}"
        assert mock_player.wins == 1