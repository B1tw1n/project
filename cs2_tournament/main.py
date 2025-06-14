from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from cs2_tournament.app import schemas, models, crud
from cs2_tournament.app.auth_router import router as auth_router
from cs2_tournament.app.games import games_router
from cs2_tournament.app.auth_router import get_current_user
from cs2_tournament.app.database import get_db, engine, Base
from fastapi.openapi.utils import get_openapi

Base.metadata.create_all(bind=engine)

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CS2 Tournament API",
        version="1.0.0",
        description="API for managing CS2 tournaments",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

@app.post("/teams/", response_model=schemas.Team)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if len(team.players) != 5:
        raise HTTPException(status_code=400, detail="Team must have exactly 5 players")
    db_game = crud.get_game_by_name(db, team.game_id)
    if not db_game:
        raise HTTPException(status_code=400, detail="Game not found")
    return crud.create_team(db=db, team=team, captain_id=current_user.id)

@app.post("/matches/", response_model=schemas.Match)
def create_match(
    match: schemas.MatchCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    tournament = db.query(models.Tournament).filter(models.Tournament.id == match.tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=400, detail="Tournament not found")

    team_a = db.query(models.Team).filter(models.Team.id == match.team_a_id).first()
    team_b = db.query(models.Team).filter(models.Team.id == match.team_b_id).first()
    if not team_a or not team_b:
        raise HTTPException(status_code=400, detail="One or both teams not found")

    return crud.create_match(db=db, match=match)

@app.get("/matches/", response_model=list[schemas.Match])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_matches(db, skip=skip, limit=limit)

@app.get("/")
def root():
    return {"message": "Welcome to CS2 Tournament API"}

@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(games_router, prefix="/games", tags=["games"])
