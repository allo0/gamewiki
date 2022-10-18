from enum import IntEnum
from typing import List, Optional

from pydantic import BaseModel


class GenreType(IntEnum):
    PointNclick: int = 2
    Fighting: int = 4
    Shooter: int = 5
    Music: int = 7
    Platform: int = 8
    Puzzle: int = 9
    Racing: int = 10
    RealTimeStrategy: int = 11
    RolePlaying: int = 12
    Simulator: int = 13
    Sport: int = 14
    Strategy: int = 15
    TurnBasedStrategy: int = 16
    Tactical: int = 24
    HackNslash_BeatemUp: int = 25
    QuizTrivia: int = 26
    Pinball: int = 30
    Adventure: int = 31
    Indie: int = 32
    Arcade: int = 33
    VisualNovel: int = 34
    CardNBoardGame: int = 35
    MOBA: int = 36


class GameDetails(BaseModel):
    id: str = ''
    name: str = ''
    summary: str = ''
    cover: Optional[str] = ''
    screenshots: List[str] = []
    total_rating: str = ''
    url: str = ''
    genres: List[GenreType] = []


class ListGameDetails(BaseModel):
    list_of_games: List[GameDetails] = []
