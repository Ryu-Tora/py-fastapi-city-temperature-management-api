from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import httpx
from ..database import SessionLocal
from .. import crud, schemas


router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def fetch_temperatures(city_name: str) -> float:
    url = f"https://api.open-meteo.com/v1/forecast?current_weather=true&latitude=0&longitude=0"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        return data["current_weather"]["temperature"]


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)):
    cities = crud.get_cities(db)
    for city in cities:
        temp = await fetch_temperatures(city.name)
        crud.create_temperatures(db, city_id=city.id, temperature=temp)
    return {"message": "tamperatures updated successfully"}


@router.get("", response_model=schemas.TemperatureRead)
def list_all(city_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_temperatures(db, city_id=city_id)
