"""
Модуль содержит Pydantic-схемы и перечисления (Enum) для описания структуры 
и состояния событий (Event) в line_provider.
"""
from enum import Enum
from pydantic import BaseModel
from typing import Optional
import decimal


class EventState(str, Enum):
    """
    Перечисление возможных состояний события.
    - NEW: Событие активно и приём ставок открыт.
    - FINISHED_WIN: Событие завершилось с исходом "WIN".
    - FINISHED_LOSE: Событие завершилось с исходом "LOSE".
    """
    NEW = "NEW"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


class Event(BaseModel):
    """
    Схема (модель) события (Event).

    Поля:
    - event_id: Идентификатор события (str).
    - coefficient: Коэффициент для расчёта выигрыша (Decimal).
    - deadline: Временная метка (int), до которой принимаются ставки.
    - state: Текущее состояние события (EventState).
    """
    event_id: str
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None
    state: Optional[EventState] = None
