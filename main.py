from fastapi import FastAPI
from app.controllers.players_controller import router as players_router
from app.controllers.teams_controller import router as teams_router
from app.controllers.match_controller import router as match_router
app = FastAPI()

# Include the players routes
app.include_router(teams_router, prefix="/teams", tags=["Teams"])
app.include_router(players_router, prefix="/players", tags=["Players"])
app.include_router(match_router, prefix="/matches", tags=["Matches"])
