"""
Модуль содержит Pydantic-схемы для валидации данных и 
сериализации/десериализации ставок (Bet).
"""
from pydantic import BaseModel, Field
from typing import Optional
import decimal


class BetCreate(BaseModel):
    """
    Схема для создания новой ставки.
    Поля:
    - event_id: Идентификатор события (str).
    - amount: Сумма ставки (decimal.Decimal), должна быть > 0.
    """
    event_id: str
    amount: decimal.Decimal = Field(gt=0, description="Сумма ставки")


class BetDB(BaseModel):
    """
    Схема для возврата информации о ставке (Bet) из базы данных.
    Поля:
    - id: Уникальный идентификатор ставки (int).
    - event_id: Идентификатор события (str).
    - amount: Сумма ставки (decimal.Decimal).
    - status: Текущий статус ставки (str).
    """
    id: int
    event_id: str
    amount: decimal.Decimal
    status: str  # Возможные варианты: "NEW", "WIN", "LOSE"

    class Config:
        orm_mode = True
