from sqlalchemy.orm import Session
from cs2_tournament.app import models, schemas

def get_game_by_name(db: Session, name: str):
    return db.query(models.Game).filter(models.Game.name == name).first()

def get_game_by_id(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(name=game.name)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

def create_team(db: Session, team: schemas.TeamCreate, captain_id: int):
    if len(team.players) != 5:
        raise ValueError("A team must have exactly 5 players")

    db_team = models.Team(name=team.name, game_id=team.game_id, captain_id=captain_id)
    db.add(db_team)
    db.flush()

    for player in team.players:
        db_player = models.Player(nickname=player.nickname, team_id=db_team.id)
        db.add(db_player)

    db.commit()
    db.refresh(db_team)
    return db_team

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_match(db: Session, match: schemas.MatchCreate):
    winner_team_id = match.team_a_id if match.score_a > match.score_b else match.team_b_id
    db_match = models.Match(
        tournament_id=match.tournament_id,
        team_a_id=match.team_a_id,
        team_b_id=match.team_b_id,
        score_a=match.score_a,
        score_b=match.score_b,
        winner_team_id=winner_team_id,
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()
