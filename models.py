from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)

class Superhero(db.Model, SerializerMixin):
    __tablename__ = 'superheroes'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    city_id = Column(Integer, ForeignKey('cities.id'))
    city = relationship("City", back_populates="superheroes")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    heroes = relationship("Hero", back_populates="superhero")

class City(db.Model, SerializerMixin):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    superheroes = relationship("Superhero", back_populates="city")

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    super_name = Column(String, nullable=False)
    superpower = Column(String, nullable=False)
    superhero_id = Column(Integer, ForeignKey('superheroes.id'))
    superhero = relationship("Superhero", back_populates="heroes")
    hero_powers = relationship("HeroPower", back_populates="hero")

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, default="Default description with sufficient length.")
    hero_powers = relationship("HeroPower", back_populates="power")

    __table_args__ = (
        CheckConstraint("LENGTH(description) >= 20", name="check_description_length"),
    )

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    id = Column(Integer, primary_key=True)
    strength = Column(String, nullable=False)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    power_id = Column(Integer, ForeignKey('powers.id'))
    hero = relationship("Hero", back_populates="hero_powers")
    power = relationship("Power", back_populates="hero_powers")

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return value
