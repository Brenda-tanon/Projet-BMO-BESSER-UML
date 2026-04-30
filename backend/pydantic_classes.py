from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class StatusReservation(Enum):
    Anuler = "Anuler"
    En_attente = "En_attente"
    Confirmer = "Confirmer"

############################################
# Classes are defined here
############################################
class IndisponibliteCreate(BaseModel):
    date_fin: date
    date_debut: date
    motif: str
    sale_evenement: Any
    reservation: int  # 1:1 Relationship (mandatory)


class ReservationCreate(BaseModel):
    date_debutR: date
    liste_option: Any
    date_finR: date
    nom: str
    Status: StatusReservation
    peut_inclure: List[int]  # N:M Relationship
    lier: Optional[List[int]] = None  # 1:N Relationship
    indisponiblite: int  # 1:1 Relationship (mandatory)
    etre_effectuer: int  # N:1 Relationship (mandatory)


class gestionaireCreate(BaseModel):
    liste_dispoibilités_passées: Any
    date_du_jour: date
    liste_diponiblité: Any
    liste_congres: Any
    effectuer: Optional[List[int]] = None  # 1:N Relationship
    reserver: Optional[List[int]] = None  # 1:N Relationship


class optionCreate(BaseModel):
    nomO: str
    peut_etre_presente: List[int]  # N:M Relationship


class prestationCreate(optionCreate):
    type: str


class materielCreate(optionCreate):
    quantite: int
    nom: str


class EvenementCreate(BaseModel):
    nomEve: str
    description: str
    nbpartion: int
    emailReferent: str
    etre_faite: Optional[int] = None  # N:1 Relationship (optional)


class ElementCreate(BaseModel):
    cap_max: int
    nomE: str


class Centre_de_congresCreate(BaseModel):
    nomC: str
    etre_reserver: int  # N:1 Relationship (mandatory)


