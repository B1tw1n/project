from sqlalchemy.orm import Session
from cs2_tournament.app import models, schemas

def get_game_by_name(db: Session, name: str):
    return db.query(models.Game).filter(models.Game.name == name).first()

def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(name=game.name)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def create_team(db: Session, team: schemas.TeamCreate):
    if len(team.players) != 5:
        raise ValueError("A team must have exactly 5 players")

    db_team = models.Team(name=team.name, game_id=team.game_id)
    db.add(db_team)
    db.flush()  # Щоб отримати ID до створення гравців

    for player in team.players:
        db_player = models.Player(nickname=player.nickname, team_id=db_team.id)
        db.add(db_player)

    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()
