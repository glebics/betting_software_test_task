"""
Модуль содержит ORM-модель Bet для работы с таблицей 'bets' в базе данных.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric

Base = declarative_base()


class Bet(Base):
    """
    ORM-модель ставки (Bet).
    Содержит поля:
    - id: Первичный ключ (int).
    - event_id: Идентификатор события (str).
    - amount: Сумма ставки (Decimal).
    - status: Статус ставки (str), может быть NEW, WIN или LOSE.
    """
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    amount = Column(Numeric(10, 2))
    status = Column(String, default="NEW")
