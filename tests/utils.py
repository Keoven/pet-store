import csv
from pathlib import Path

from pet_store.pet.services import PetService, SpeciesService


def seed_database(db_session):
    service = PetService(db_session)
    path = Path(__file__).parent / './pets.csv'
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            service.create(row)


def seed_species(db_session):
    service = SpeciesService(db_session)
    species = []
    for species_name in ['Cat', 'Dog']:
        species.append(service.create({
            'id': species_name.lower(),
            'name': species_name,
        }))

    return species
