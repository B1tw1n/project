from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from cs2_tournament.app import schemas, models, crud
from cs2_tournament.app.auth import get_current_user
from cs2_tournament.app.models import User
from cs2_tournament.app.database import get_db, engine, Base
from cs2_tournament.app.auth_router import router as auth_router
from cs2_tournament.app.games import games_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")



@app.post("/teams/", response_model=schemas.Team)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if len(team.players) != 4:
        raise HTTPException(status_code=400, detail="Team must have exactly 4 players")
    db_game = db.query(models.Game).filter(models.Game.id == team.game_id).first()
    if not db_game:
        raise HTTPException(status_code=400, detail="Game not found")
    # Передаємо капітана в crud
    return crud.create_team(db=db, team=team, captain_id=current_user.id)


@app.get("/teams/", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    return teams



@app.post("/games/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    db_game = crud.get_game_by_name(db, name=game.name)
    if db_game:
        raise HTTPException(status_code=400, detail="Game already registered")
    return crud.create_game(db=db, game=game)



app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(games_router, prefix="/games", tags=["games"])
