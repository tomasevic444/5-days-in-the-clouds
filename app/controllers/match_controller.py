from fastapi import APIRouter
from app.models.match import Match
from app.services.match_service import create_match

router = APIRouter()

@router.post("/", response_model=Match)
def create_new_match(match: Match):
    return create_match(match)