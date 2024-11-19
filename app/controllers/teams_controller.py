from fastapi import APIRouter, HTTPException
from app.services.team_service import create_team, get_team_by_id
from app.models.team import Team

router = APIRouter()


@router.post("/", response_model=Team)
def create_team_endpoint(team_data: dict):
    """
    Create a new team with validation.
    """
    try:
        team = create_team(team_data["teamName"], team_data["players"])
        return team
    except HTTPException as e:
        raise e
    
@router.get("/{team_id}", response_model=dict)
def get_team(team_id: str):
    """
    Fetch a team by its ID.
    If the team does not exist, return a 404 error.
    """
    try:
        team = get_team_by_id(team_id)
        return team.dict()  # Convert the Team object to a dictionary
    except HTTPException as e:
        raise e