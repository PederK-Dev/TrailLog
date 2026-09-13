from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Trail(Base):
    __tablename__ = "trails"

    id = Column(Integer, primary_key=True, index=True)
    place = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    distance_km = Column(Float, nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)