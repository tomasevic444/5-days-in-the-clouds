from typing import Dict
from app.models.match import Match
from app.models.player import Player
from app.models.team import Team
from app.services.team_service import get_team_by_id
from fastapi import HTTPException
from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage  # Using in-memory storage for TinyDB

# Initialize TinyDB in-memory database
db = TinyDB(storage=MemoryStorage)
matches_table = db.table("matches")
teams_table = db.table("teams")  # Assuming teams are stored here as well
PlayerQuery = Query()
TeamQuery = Query()

def create_match(match: Match):
    if match.duration < 1:
        raise HTTPException(status_code=400, detail="Duration must be at least 1 hour")

    # Fetch teams
    team1 = get_team_by_id(match.team1Id)
    team2 = get_team_by_id(match.team2Id)
    
    if not team1 or not team2:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    # Add duration to players' hoursPlayed
    for player in team1.players + team2.players:
        player.hoursPlayed += match.duration

    # Update ELO, wins, losses based on the match result
    if match.winningTeamId:
        if match.winningTeamId == team1.id:
            winning_team = team1
            losing_team = team2
        elif match.winningTeamId == team2.id:
            winning_team = team2
            losing_team = team1
        else:
            raise HTTPException(status_code=400, detail="Invalid winningTeamId")

        # Update player stats
        update_team_stats(winning_team, losing_team, S=1, duration=match.duration)
        update_team_stats(losing_team, winning_team, S=0, duration=match.duration)

    else:  # Draw case
        update_team_stats(team1, team2, S=0.5, duration=match.duration)
        update_team_stats(team2, team1, S=0.5, duration=match.duration)

    # Store the match in the matches table of TinyDB
    matches_table.insert(match.dict())  # Save match data in the database
    return match

def update_team_stats(team, opponent_team, S, duration):
    opponent_elo = sum(player.elo for player in opponent_team.players) / len(opponent_team.players)

    for player in team.players:
        # Calculate expected score
        E = 1 / (1 + 10 ** ((opponent_elo - player.elo) / 400))

        # Determine K (ratingAdjustment)
        if player.hoursPlayed < 500:
            K = 50
        elif player.hoursPlayed < 1000:
            K = 40
        elif player.hoursPlayed < 3000:
            K = 30
        elif player.hoursPlayed < 5000:
            K = 20
        else:
            K = 10

        # Update ELO
        player.elo = player.elo + K * (S - E)

        # Update wins/losses if not a draw
        if S == 1:
            player.wins += 1
        elif S == 0:
            player.losses += 1

# Retrieve a match by its ID from TinyDB
def get_match_by_id(match_id: str) -> Match:
    match_data = matches_table.get(Query().id == match_id)
    if not match_data:
        raise HTTPException(status_code=404, detail="Match not found")
    return Match(**match_data)