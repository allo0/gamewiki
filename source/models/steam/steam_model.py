import json
from typing import Optional, Type, List

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class UserUtilities:
    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


@dataclass
class GetFriendList(UserUtilities):
    steamid: str
    relationship: str
    friend_since: str

    def __init__(self):
        super().__init__()


@dataclass
class GetPlayerAchievements(UserUtilities):
    apiname: str
    achieved: str
    unlocktime: str
    name: Optional[str] = None
    description: Optional[str] = None

    def __init__(self):
        super().__init__()

@dataclass
class GameFriendlyName:
    cdata: str

    def __init__(self, cdata: str) -> None:
        self.cdata = cdata

@dataclass
class Achievement:
    icon_closed: GameFriendlyName
    icon_open: GameFriendlyName
    name: GameFriendlyName
    apiname: GameFriendlyName
    description: GameFriendlyName
    unlock_timestamp: int
    closed: int
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, icon_closed: GameFriendlyName, icon_open: GameFriendlyName, name: GameFriendlyName,
                 apiname: GameFriendlyName, description: GameFriendlyName, unlock_timestamp: int, closed: int) -> None:
        self.icon_closed = icon_closed
        self.icon_open = icon_open
        self.name = name
        self.apiname = apiname
        self.description = description
        self.unlock_timestamp = unlock_timestamp
        self.closed = closed

@dataclass
class Achievements:
    achievement: List[Achievement]
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, achievement: List[Achievement]) -> None:
        self.achievement = achievement

@dataclass
class Game:
    game_friendly_name: GameFriendlyName
    game_name: GameFriendlyName
    game_link: GameFriendlyName
    game_icon: GameFriendlyName
    game_logo: GameFriendlyName
    game_logo_small: GameFriendlyName
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, game_friendly_name: GameFriendlyName, game_name: GameFriendlyName, game_link: GameFriendlyName,
                 game_icon: GameFriendlyName, game_logo: GameFriendlyName, game_logo_small: GameFriendlyName) -> None:
        self.game_friendly_name = game_friendly_name
        self.game_name = game_name
        self.game_link = game_link
        self.game_icon = game_icon
        self.game_logo = game_logo
        self.game_logo_small = game_logo_small

@dataclass
class Player:
    steam_id64: str
    custom_url: GameFriendlyName
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, steam_id64: str, custom_url: GameFriendlyName) -> None:
        self.steam_id64 = steam_id64
        self.custom_url = custom_url

@dataclass
class Stats:
    hours_played: int

    def __init__(self, hours_played: int) -> None:
        self.hours_played = hours_played

@dataclass
class Playerstats:
    privacy_state: str
    visibility_state: int
    game: Game
    player: Player
    stats: Stats
    achievements: Achievements
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, privacy_state: str, visibility_state: int, game: Game, player: Player, stats: Stats,
                 achievements: Achievements) -> None:
        self.privacy_state = privacy_state
        self.visibility_state = visibility_state
        self.game = game
        self.player = player
        self.stats = stats
        self.achievements = achievements

@dataclass
class Welcome10:
    playerstats: Playerstats
    class Config:
        arbitrary_types_allowed = True
    def __init__(self, playerstats: Playerstats) -> None:
        self.playerstats = playerstats
