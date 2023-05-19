from datetime import datetime

from pydantic import BaseModel


# Pet shared properties
class PetBase(BaseModel):
    species: str
    name: str
    age: int


# Pet properties to receive on creation
class PetCreate(PetBase):
    pass


# Pet properties stored in DB
class PetInDB(PetBase):
    id: str
    species_id: str
    name: str
    age: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


# Pet properties to return to client
class Pet(PetBase):
    id: str
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True


# Species properties stored in DB
class SpeciesInDB(BaseModel):
    id: str
    name: str
    updated_at: datetime
    created_at: datetime
