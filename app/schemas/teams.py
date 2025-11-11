from enum import Enum
from typing import List, Dict
from pydantic import BaseModel


class Composition(BaseModel):
    times_played: int
    agents: List[str]


class MapStats(BaseModel):
    compositions: List[Composition]


class TeamCompositions(BaseModel):
    team_id: str
    team_name: str
    maps: Dict[str, MapStats]


class VLRTeamCompositionsResponse(BaseModel):
    compositions: TeamCompositions
