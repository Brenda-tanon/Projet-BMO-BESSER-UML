import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class StatusReservation(enum.Enum):
    Anuler = "Anuler"
    En_attente = "En_attente"
    Confirmer = "Confirmer"


# Tables definition for many-to-many relationships
reservation_option = Table(
    "reservation_option",
    Base.metadata,
    Column("peut_etre_presente", ForeignKey("reservation.id"), primary_key=True),
    Column("peut_inclure", ForeignKey("option.id"), primary_key=True),
)

# Tables definition
class Indisponiblite(Base):
    __tablename__ = "indisponiblite"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_debut: Mapped[dt_date] = mapped_column(Date)
    date_fin: Mapped[dt_date] = mapped_column(Date)
    motif: Mapped[str] = mapped_column(String(100))
    sale_evenement: Mapped[any] = mapped_column()
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), unique=True)

class Reservation(Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    liste_option: Mapped[any] = mapped_column()
    Status: Mapped[StatusReservation] = mapped_column(Enum(StatusReservation))
    date_debutR: Mapped[dt_date] = mapped_column(Date)
    date_finR: Mapped[dt_date] = mapped_column(Date)
    etre_effectuer_id: Mapped[int] = mapped_column(ForeignKey("gestionaire.id"))

class gestionaire(Base):
    __tablename__ = "gestionaire"
    id: Mapped[int] = mapped_column(primary_key=True)
    liste_congres: Mapped[any] = mapped_column()
    date_du_jour: Mapped[dt_date] = mapped_column(Date)
    liste_diponiblité: Mapped[any] = mapped_column()
    liste_dispoibilités_passées: Mapped[any] = mapped_column()

class option(Base):
    __tablename__ = "option"
    id: Mapped[int] = mapped_column(primary_key=True)
    nomO: Mapped[str] = mapped_column(String(100))
    type_spec: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "option",
        "polymorphic_on": "type_spec",
    }

class prestation(option):
    __tablename__ = "prestation"
    id: Mapped[int] = mapped_column(ForeignKey("option.id"), primary_key=True)
    type: Mapped[str] = mapped_column(String(100))
    __mapper_args__ = {
        "polymorphic_identity": "prestation",
    }

class materiel(option):
    __tablename__ = "materiel"
    id: Mapped[int] = mapped_column(ForeignKey("option.id"), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    quantite: Mapped[int] = mapped_column(Integer)
    __mapper_args__ = {
        "polymorphic_identity": "materiel",
    }

class Evenement(Base):
    __tablename__ = "evenement"
    id: Mapped[int] = mapped_column(primary_key=True)
    nomEve: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(100))
    nbpartion: Mapped[int] = mapped_column(Integer)
    emailReferent: Mapped[str] = mapped_column(String(100))
    etre_faite_id: Mapped[int] = mapped_column(ForeignKey("reservation.id"), nullable=True)

class Element(Base):
    __tablename__ = "element"
    id: Mapped[int] = mapped_column(primary_key=True)
    nomE: Mapped[str] = mapped_column(String(100))
    cap_max: Mapped[int] = mapped_column(Integer)

class Centre_de_congres(Base):
    __tablename__ = "centre_de_congres"
    id: Mapped[int] = mapped_column(primary_key=True)
    nomC: Mapped[str] = mapped_column(String(100))
    etre_reserver_id: Mapped[int] = mapped_column(ForeignKey("gestionaire.id"))


#--- Relationships of the indisponiblite table
Indisponiblite.reservation: Mapped["Reservation"] = relationship("Reservation", back_populates="indisponiblite", foreign_keys=[Indisponiblite.reservation_id])

#--- Relationships of the reservation table
Reservation.indisponiblite: Mapped["Indisponiblite"] = relationship("Indisponiblite", back_populates="reservation", foreign_keys=[Indisponiblite.reservation_id])
Reservation.etre_effectuer: Mapped["gestionaire"] = relationship("gestionaire", back_populates="effectuer", foreign_keys=[Reservation.etre_effectuer_id])
Reservation.peut_inclure: Mapped[List["option"]] = relationship("option", secondary=reservation_option, back_populates="peut_etre_presente")
Reservation.lier: Mapped[List["Evenement"]] = relationship("Evenement", back_populates="etre_faite", foreign_keys=[Evenement.etre_faite_id])

#--- Relationships of the gestionaire table
gestionaire.reserver: Mapped[List["Centre_de_congres"]] = relationship("Centre_de_congres", back_populates="etre_reserver", foreign_keys=[Centre_de_congres.etre_reserver_id])
gestionaire.effectuer: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="etre_effectuer", foreign_keys=[Reservation.etre_effectuer_id])

#--- Relationships of the option table
option.peut_etre_presente: Mapped[List["Reservation"]] = relationship("Reservation", secondary=reservation_option, back_populates="peut_inclure")

#--- Relationships of the evenement table
Evenement.etre_faite: Mapped["Reservation"] = relationship("Reservation", back_populates="lier", foreign_keys=[Evenement.etre_faite_id])

#--- Relationships of the centre_de_congres table
Centre_de_congres.etre_reserver: Mapped["gestionaire"] = relationship("gestionaire", back_populates="reserver", foreign_keys=[Centre_de_congres.etre_reserver_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)