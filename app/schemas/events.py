from enum import Enum
from typing import List, Dict
from pydantic import BaseModel

class Event(BaseModel):
    event_name: str
    date_start: str
    date_end: str
    prize_amount: str
    event_id: str

class VLREventsResponse(BaseModel):
    events: List[Event]