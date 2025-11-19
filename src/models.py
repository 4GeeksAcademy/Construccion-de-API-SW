from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, select
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    @classmethod
    def get_all(cls):
        return db.session.execute(select(cls)).scalars().all()

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)

    @classmethod
    def find_by_email(cls, email):
        stmt = select(cls).where(cls.email == email)
        return db.session.execute(stmt).scalar_one_or_none()

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    birth_year: Mapped[str] = mapped_column(String(20))
    eye_color: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="character")

    @classmethod
    def get_all(cls):
        return db.session.execute(select(cls)).scalars().all()

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)

    @classmethod
    def search(cls, term):
        stmt = select(cls).where(cls.name.ilike(f"%{term}%"))
        return db.session.execute(stmt).scalars().all()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120))
    terrain: Mapped[str] = mapped_column(String(120))
    population: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    favorites: Mapped[list["Favorite"]] = relationship(back_populates="planet")

    @classmethod
    def get_all(cls):
        return db.session.execute(select(cls)).scalars().all()

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }


class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    model: Mapped[str] = mapped_column(String(120))
    manufacturer: Mapped[str] = mapped_column(String(120))
    crew: Mapped[str] = mapped_column(String(20))
    passengers: Mapped[str] = mapped_column(String(20))
    cargo_capacity: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="vehicle")

    @classmethod
    def get_all(cls):
        return db.session.execute(select(cls)).scalars().all()

    @classmethod
    def get_by_id(cls, id):
        return db.session.get(cls, id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model
        }


class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int | None] = mapped_column(
        ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int | None] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicle.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="favorites")
    character: Mapped["Character"] = relationship(back_populates="favorites")
    planet: Mapped["Planet"] = relationship(back_populates="favorites")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="favorites")

    @classmethod
    def get_by_user(cls, user_id):
        stmt = select(cls).where(cls.user_id == user_id)
        return db.session.execute(stmt).scalars().all()

    @classmethod
    def find(cls, user_id, char_id=None, planet_id=None, vehicle_id=None):
        stmt = select(cls).where(cls.user_id == user_id)
        if char_id:
            stmt = stmt.where(cls.character_id == char_id)
        if planet_id:
            stmt = stmt.where(cls.planet_id == planet_id)
        if vehicle_id:
            stmt = stmt.where(cls.vehicle_id == vehicle_id)
        return db.session.execute(stmt).scalar_one_or_none()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id
        }
