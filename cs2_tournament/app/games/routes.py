from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cs2_tournament.app import crud, schemas
from cs2_tournament.app.database import get_db

games_router = APIRouter()

@games_router.post("/create", response_model=schemas.Game)
async def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    existing_game = crud.get_game_by_name(db, game.name)
    if existing_game:
        raise HTTPException(status_code=400, detail="Game already exists")

    new_game = crud.create_game(db, game)
    return new_game
