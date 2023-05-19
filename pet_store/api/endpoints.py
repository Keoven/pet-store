from typing import Any, List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from pet_store import schemas
from pet_store.exceptions import InvalidSpecies
from pet_store.db import get_db
from pet_store.pet.services import PetService

pet_router = APIRouter()


@pet_router.post('/', response_model=schemas.Pet, status_code=status.HTTP_201_CREATED)
def create_pet(
    *,
    db: Session = Depends(get_db),
    pet_in: schemas.PetCreate,
) -> Any:
    data = jsonable_encoder(pet_in)
    service = PetService(db)
    try:
        pet = service.create(data)
    except (InvalidSpecies, ValueError):
        raise HTTPException(status_code=422)

    return pet


@pet_router.get('/', response_model=List[schemas.Pet])
def list_pet(
    db: Session = Depends(get_db),
    name: str = None,
    species: str = None,
    age: int = None,
) -> Any:
    service = PetService(db)
    return service.list(name=name, species=species, age=age)
