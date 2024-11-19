from typing import Dict, List
from fastapi import HTTPException
from app.models.team import Team
from app.models.player import Player
from app.services.player_service import players_db  # Simulated database for players

# Simulated in-memory database for teams
teams_db: Dict[str, Team] = {}

def create_team(team_name: str, player_ids: List[str]) -> Team:
    # Validation: Team name must be unique
    if any(team.teamName == team_name for team in teams_db.values()):
        raise HTTPException(status_code=400, detail="Team name must be unique")
    
    # Validation: Must have exactly 5 players
    if len(player_ids) != 5:
        raise HTTPException(status_code=400, detail="A team must have exactly 5 players")
    
    # Fetch players from player IDs and validate
    players = []
    for player_id in player_ids:
        player = next((p for p in players_db.values() if p.id == player_id), None)
        if not player:
            raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
        if player.team is not None:  # Use `team` instead of `teamId`
            raise HTTPException(status_code=400, detail=f"Player {player.nickname} is already in a team")
        players.append(player)

    # Create the team
    team = Team(teamName=team_name, players=players)
    teams_db[team.id] = team

    # Assign team ID to players
    for player in players:
        player.team = team.id  # Assign the team ID to the `team` attribute

    return team

def get_team_by_id(team_id: str) -> Team:
    """
    Fetch a team by ID. Raise an HTTPException if the team is not found.
    """
    team = teams_db.get(team_id)  # Look up the team in the in-memory database
    if not team:
        raise HTTPException(status_code=404, detail=f"Team with ID {team_id} not found")
    return team