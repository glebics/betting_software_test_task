from pydantic import BaseModel, Field
from typing import Optional
import decimal


class BetCreate(BaseModel):
    event_id: str
    amount: decimal.Decimal = Field(gt=0, description="Сумма ставки")


class BetDB(BaseModel):
    id: int
    event_id: str
    amount: decimal.Decimal
    status: str  # "NEW", "WIN", "LOSE"

    class Config:
        orm_mode = True
