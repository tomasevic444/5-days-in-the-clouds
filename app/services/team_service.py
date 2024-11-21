from fastapi import HTTPException
from tinydb import TinyDB, Query
from app.models.team import Team
from app.models.player import Player
from app.services.player_service import get_player  # Assuming player service is correctly working
from uuid import uuid4
from typing import List
from tinydb.storages import MemoryStorage  # Importing MemoryStorage

# Initialize the in-memory database (TinyDB with MemoryStorage)
db = TinyDB(storage=MemoryStorage)  # You can switch to file-based storage if desired
teams_table = db.table("teams")
players_table = db.table("players")  # Define the players_table for reference
PlayerQuery = Query()  # Define the query for player lookups
TeamQuery = Query()  # Define the query for team lookups

def create_team(team_name: str, player_ids: List[str]) -> Team:
    # Validation: Team name must be unique
    if teams_table.search(TeamQuery.teamName == team_name):
        raise HTTPException(status_code=400, detail="Team name must be unique")
    
    # Validation: Must have exactly 5 players
    if len(player_ids) != 5:
        raise HTTPException(status_code=400, detail="A team must have exactly 5 players")
    
    # Fetch players from player IDs and validate
    players = []
    for player_id in player_ids:
        player = get_player(player_id)  # Using the player service to get player
        if player.team is not None:
            raise HTTPException(status_code=400, detail=f"Player {player.nickname} is already in a team")
        players.append(player)

    # Create the team
    team = Team(teamName=team_name, players=players)
    teams_table.insert(team.model_dump())  # Store team in the database

    # Assign team ID to players
    for player in players:
        player.team = team.id  # Assign the team ID to the `team` attribute
        # Update player in the player database with new team assignment
        player_dict = player.dict()
        players_table.update(player_dict, PlayerQuery.id == player.id)

    return team

def get_team_by_id(team_id: str) -> Team:

    team_data = teams_table.get(TeamQuery.id == team_id)  # Get team by ID
    if not team_data:
        raise HTTPException(status_code=404, detail=f"Team with ID {team_id} not found")
    return Team(**team_data)

def update_team_in_db(team_id: str, player: Player):

    # Fetch the team by its ID
    team_data = teams_table.get(TeamQuery.id == team_id)
    if not team_data:
        raise HTTPException(status_code=404, detail=f"Team with ID {team_id} not found")

    # Deserialize the team
    team = Team(**team_data)

    # Update the player's data in the team's players list
    for i, team_player in enumerate(team.players):
        if team_player.id == player.id:
            team.players[i] = player  # Replace the player's data
            break
    else:
        raise HTTPException(status_code=404, detail=f"Player with ID {player.id} not found in team {team_id}")

    # Save the updated team back to the database
    teams_table.update(team.model_dump(), TeamQuery.id == team.id)