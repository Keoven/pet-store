from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from pet_store.exceptions import InvalidSpecies
from .models import Pet, Species


class SpeciesService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, data) -> Species:
        species = Species(**data)
        self.db_session.add(species)
        self.db_session.commit()
        self.db_session.refresh(species)
        return species

    def list(self) -> List[str]:
        return self.db_session.scalars(select(Species.id)).all()


class PetService:
    def __init__(self, db: Session):
        self.db = db
        self.species_service = SpeciesService(db)

    def create(self, data) -> Pet:
        if data['species'] not in self.species_service.list():
            raise InvalidSpecies('Invalid species')

        pet = Pet(**data)
        self.db.add(pet)
        self.db.commit()
        self.db.refresh(pet)
        return pet

    def list(self, name: str, species: str, age: str) -> List[Pet]:
        query = self.db.query(Pet)

        if name:
            query = query.filter(Pet.name.contains(name))

        if species:
            query = query.filter_by(species=species)

        if age:
            query = query.filter_by(age=age)

        return query.all()
