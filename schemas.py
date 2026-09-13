from pydantic import BaseModel
from datetime import date
from typing import Optional

class TrailCreate(BaseModel):
    place: str
    date: date
    distance_km: float
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None

class TrailOut(TrailCreate):
    id: int

    class Config:
        from_attributes = True