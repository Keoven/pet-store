from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, validates

from pet_store.utils import ulid
from pet_store.db import Base


class Species(Base):
    __tablename__ = 'species'

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    pet = relationship('Pet', back_populates='_species')


class Pet(Base):
    __tablename__ = 'pet'

    id = Column(String, primary_key=True, index=True, default=ulid)
    name = Column(String)
    age = Column(Integer)
    species = Column('species_id', String, ForeignKey('species.id'))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    _species = relationship('Species', back_populates='pet')

    @validates('name')
    def validate_name(self, key, name):
        name = name.strip()
        if name == '':
            raise ValueError('Invalid name')
        return name
