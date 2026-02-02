from http.client import HTTPException

from sqlalchemy.orm import Session

import models
import schemas


def create_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_cities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()


def delete_city(db: Session, city_id: int):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return city


def get_temperatures(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Temperature).offset(skip).limit(limit).all()


def get_city_temperatures(db: Session, city_id: int):
    return db.query(models.Temperature).filter(models.Temperature.city_id == city_id).all()