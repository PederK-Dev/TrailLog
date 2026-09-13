from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from fastapi import HTTPException

import models
import schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "TrailLog API is running"}

@app.post("/trails")
def create_trail(trail: schemas.TrailCreate, db: Session = Depends(get_db)):
    new_trail = models.Trail(
        place=trail.place,
        date=trail.date,
        distance_km=trail.distance_km,
        duration_minutes=trail.duration_minutes,
        notes=trail.notes
    )
    db.add(new_trail)
    db.commit()
    db.refresh(new_trail)
    return new_trail

@app.get("/trails", response_model=List[schemas.TrailOut])
def get_trails(db: Session = Depends(get_db)):
    return db.query(models.Trail).all()

@app.get("/trails/{trail_id}", response_model=schemas.TrailOut)
def get_trail(trail_id: int, db: Session = Depends(get_db)):
    trail = db.query(models.Trail).filter(models.Trail.id == trail_id).first()
    if trail is None:
        raise HTTPException(status_code=404, detail="Trail not found")
    return trail

@app.put("/trails/{trail_id}", response_model=schemas.TrailOut)
def update_trail(trail_id: int, updated_trail: schemas.TrailCreate, db: Session = Depends(get_db)):
    trail = db.query(models.Trail).filter(models.Trail.id == trail_id).first()
    if trail is None:
        raise HTTPException(status_code=404, detail="Trail not found")

    trail.place = updated_trail.place
    trail.date = updated_trail.date
    trail.distance_km = updated_trail.distance_km
    trail.duration_minutes = updated_trail.duration_minutes
    trail.notes = updated_trail.notes

    db.commit()
    db.refresh(trail)
    return trail

@app.delete("/trails/{trail_id}")
def delete_trail(trail_id: int, db: Session = Depends(get_db)):
    trail = db.query(models.Trail).filter(models.Trail.id == trail_id).first()
    if trail is None:
        raise HTTPException(status_code=404, detail="Trail not found")

    db.delete(trail)
    db.commit()
    return {"detail": f"Trail {trail_id} deleted"}

@app.get("/trails/stats/total-distance")
def get_total_distance(db: Session = Depends(get_db)):
    trails = db.query(models.Trail).all()
    total = sum(trail.distance_km for trail in trails)
    return {"total_distance_km": total}


@app.get("/trails/stats/longest", response_model=schemas.TrailOut)
def get_longest_trail(db: Session = Depends(get_db)):
    longest = db.query(models.Trail).order_by(models.Trail.distance_km.desc()).first()
    if longest is None:
        raise HTTPException(status_code=404, detail="No trails found")
    return longest