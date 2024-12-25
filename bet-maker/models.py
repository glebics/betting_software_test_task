from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric

Base = declarative_base()


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    amount = Column(Numeric(10, 2))
    status = Column(String, default="NEW")
