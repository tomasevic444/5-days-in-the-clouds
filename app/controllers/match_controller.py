from fastapi import APIRouter
from app.models.match import Match
from app.services.match_service import create_match, get_match_by_id

router = APIRouter()

@router.post("", response_model=Match)
def create_new_match(match: Match):
    return create_match(match)

@router.get("/{match_id}", response_model=Match)
def get_match(match_id: str):
    return get_match_by_id(match_id)