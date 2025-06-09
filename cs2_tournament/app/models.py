from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from cs2_tournament.app.database import Base

# Ассоціативна таблиця для турнірів і команд
tournament_teams = Table(
    "tournament_teams",
    Base.metadata,
    Column("tournament_id", Integer, ForeignKey("tournaments.id")),
    Column("team_id", Integer, ForeignKey("teams.id")),
)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    teams = relationship("Team", back_populates="captain")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    teams = relationship("Team", back_populates="game")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    captain_id = Column(Integer, ForeignKey("users.id"))  # <== зв’язок з User


    captain = relationship("User", back_populates="teams")
    players = relationship("Player", back_populates="team", cascade="all, delete")
    game = relationship("Game")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="players")


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    status = Column(String)  # upcoming, ongoing, finished

    teams = relationship("Team", secondary=tournament_teams, back_populates="tournaments")
    matches = relationship("Match", back_populates="tournament")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    team_a_id = Column(Integer, ForeignKey("teams.id"))
    team_b_id = Column(Integer, ForeignKey("teams.id"))
    score_a = Column(Integer)
    score_b = Column(Integer)
    winner_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    tournament = relationship("Tournament", back_populates="matches")
    team_a = relationship("Team", foreign_keys=[team_a_id])
    team_b = relationship("Team", foreign_keys=[team_b_id])
    winner = relationship("Team", foreign_keys=[winner_team_id])


class TeamRating(Base):
    __tablename__ = "team_ratings"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), unique=True)
    rating = Column(Integer, default=1000)

    team = relationship("Team")
