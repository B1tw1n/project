from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    nickname: str

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    team_id: int

    class Config:
        orm_mode = True


class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    game_id: int
    players: List[PlayerCreate]

class Team(TeamBase):
    id: int
    game_id: int
    players: List[Player] = []

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    name: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        from_attributes = True


class TournamentBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    status: str

class TournamentCreate(TournamentBase):
    pass

class TournamentOut(TournamentBase):
    id: int
    teams: List[Team]

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    tournament_id: int
    team_a_id: int
    team_b_id: int
    score_a: int
    score_b: int

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    winner_team_id: Optional[int]

    class Config:
        orm_mode = True

# --- RATING ---
class TeamRating(BaseModel):
    team_id: int
    rating: int

    class Config:
        orm_mode = True
