from enum import Enum
from pydantic import BaseModel
from typing import Optional
import decimal


class EventState(str, Enum):
    NEW = "NEW"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


class Event(BaseModel):
    event_id: str
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None
