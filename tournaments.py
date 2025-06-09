from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cs2_tournament.app import models, schemas
from cs2_tournament.app.database import get_db

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])

@router.post("/", response_model=schemas.TournamentOut)
def create_tournament(tournament: schemas.TournamentCreate, db: Session = Depends(get_db)):
    db_t = models.Tournament(name=tournament.name, date=tournament.date, status="upcoming")
    db.add(db_t)
    db.commit()
    db.refresh(db_t)
    return db_t

@router.get("/", response_model=list[schemas.TournamentOut])
def list_tournaments(db: Session = Depends(get_db)):
    return db.query(models.Tournament).all()
