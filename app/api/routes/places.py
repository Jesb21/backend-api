from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.schemas.place import PlaceCreate, Place
from app.api.database import get_db
from app.api.models.place import Place as PlaceModel
from app.api.models.user import User
from app.api.core.security import get_current_user_from_token

places_router = APIRouter(prefix="/places", tags=["places"])

@places_router.get("", response_model=List[Place])
def get_places(
    lat: float,
    lon: float,
    radius: int = 1000,
    db: Session = Depends(get_db)
):
    try:
        places = db.query(PlaceModel).filter(
            (PlaceModel.latitude - lat) ** 2 + (PlaceModel.longitude - lon) ** 2 <= (radius / 111111) ** 2
        ).all()
        return places
    except Exception as e:
        logger.error(f"Error getting places: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting places"
        )

@places_router.get("/{place_id}", response_model=Place)
def get_place(
    place_id: int,
    db: Session = Depends(get_db)
):
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    return place

@places_router.post("", response_model=Place)
def create_place(
    place: PlaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    try:
        db_place = PlaceModel(**place.dict())
        db.add(db_place)
        db.commit()
        db.refresh(db_place)
        return db_place
    except Exception as e:
        logger.error(f"Error creating place: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    return place

@places_router.post("", response_model=Place)
def create_place(
    place: PlaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    try:
        db_place = PlaceModel(**place.dict())
        db.add(db_place)
        db.commit()
        db.refresh(db_place)
        return db_place
    except Exception as e:
        logger.error(f"Error creating place: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating place"
        )

@places_router.put("/{place_id}", response_model=Place)
def update_place(
    place_id: int,
    place: PlaceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    db_place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not db_place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    for key, value in place.dict().items():
        setattr(db_place, key, value)
    
    db.commit()
    db.refresh(db_place)
    return db_place
    db_place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not db_place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    for key, value in place.dict().items():
        setattr(db_place, key, value)
    
    db.commit()
    db.refresh(db_place)
    return db_place

@places_router.delete("/{place_id}", response_model=dict)
def delete_place(
    place_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    db_place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not db_place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    db.delete(db_place)
    db.commit()
    return {"detail": "Place deleted successfully"}
    db_place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not db_place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    db.delete(db_place)
    db.commit()
    return {"detail": "Place deleted successfully"}
