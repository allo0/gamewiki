import json
from typing import Optional, Type

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

