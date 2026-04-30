import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Indisponiblite", "description": "Operations for Indisponiblite entities"},
        {"name": "Indisponiblite Relationships", "description": "Manage Indisponiblite relationships"},
        {"name": "Reservation", "description": "Operations for Reservation entities"},
        {"name": "Reservation Relationships", "description": "Manage Reservation relationships"},
        {"name": "Reservation Methods", "description": "Execute Reservation methods"},
        {"name": "gestionaire", "description": "Operations for gestionaire entities"},
        {"name": "gestionaire Relationships", "description": "Manage gestionaire relationships"},
        {"name": "gestionaire Methods", "description": "Execute gestionaire methods"},
        {"name": "option", "description": "Operations for option entities"},
        {"name": "option Relationships", "description": "Manage option relationships"},
        {"name": "prestation", "description": "Operations for prestation entities"},
        {"name": "materiel", "description": "Operations for materiel entities"},
        {"name": "Evenement", "description": "Operations for Evenement entities"},
        {"name": "Evenement Relationships", "description": "Manage Evenement relationships"},
        {"name": "Element", "description": "Operations for Element entities"},
        {"name": "Element Methods", "description": "Execute Element methods"},
        {"name": "Centre_de_congres", "description": "Operations for Centre_de_congres entities"},
        {"name": "Centre_de_congres Relationships", "description": "Manage Centre_de_congres relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["indisponiblite_count"] = database.query(Indisponiblite).count()
    stats["reservation_count"] = database.query(Reservation).count()
    stats["gestionaire_count"] = database.query(gestionaire).count()
    stats["option_count"] = database.query(option).count()
    stats["prestation_count"] = database.query(prestation).count()
    stats["materiel_count"] = database.query(materiel).count()
    stats["evenement_count"] = database.query(Evenement).count()
    stats["element_count"] = database.query(Element).count()
    stats["centre_de_congres_count"] = database.query(Centre_de_congres).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Indisponiblite functions
#
############################################

@app.get("/indisponiblite/", response_model=None, tags=["Indisponiblite"])
def get_all_indisponiblite(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Indisponiblite)
        query = query.options(joinedload(Indisponiblite.reservation))
        indisponiblite_list = query.all()

        # Serialize with relationships included
        result = []
        for indisponiblite_item in indisponiblite_list:
            item_dict = indisponiblite_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if indisponiblite_item.reservation:
                related_obj = indisponiblite_item.reservation
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['reservation'] = related_dict
            else:
                item_dict['reservation'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Indisponiblite).all()


@app.get("/indisponiblite/count/", response_model=None, tags=["Indisponiblite"])
def get_count_indisponiblite(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Indisponiblite entities"""
    count = database.query(Indisponiblite).count()
    return {"count": count}


@app.get("/indisponiblite/paginated/", response_model=None, tags=["Indisponiblite"])
def get_paginated_indisponiblite(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Indisponiblite entities"""
    total = database.query(Indisponiblite).count()
    indisponiblite_list = database.query(Indisponiblite).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": indisponiblite_list
    }


@app.get("/indisponiblite/search/", response_model=None, tags=["Indisponiblite"])
def search_indisponiblite(
    database: Session = Depends(get_db)
) -> list:
    """Search Indisponiblite entities by attributes"""
    query = database.query(Indisponiblite)


    results = query.all()
    return results


@app.get("/indisponiblite/{indisponiblite_id}/", response_model=None, tags=["Indisponiblite"])
async def get_indisponiblite(indisponiblite_id: int, database: Session = Depends(get_db)) -> Indisponiblite:
    db_indisponiblite = database.query(Indisponiblite).filter(Indisponiblite.id == indisponiblite_id).first()
    if db_indisponiblite is None:
        raise HTTPException(status_code=404, detail="Indisponiblite not found")

    response_data = {
        "indisponiblite": db_indisponiblite,
}
    return response_data



@app.post("/indisponiblite/", response_model=None, tags=["Indisponiblite"])
async def create_indisponiblite(indisponiblite_data: IndisponibliteCreate, database: Session = Depends(get_db)) -> Indisponiblite:

    if indisponiblite_data.reservation is not None:
        db_reservation = database.query(Reservation).filter(Reservation.id == indisponiblite_data.reservation).first()
        if not db_reservation:
            raise HTTPException(status_code=400, detail="Reservation not found")
    else:
        raise HTTPException(status_code=400, detail="Reservation ID is required")

    db_indisponiblite = Indisponiblite(
        date_fin=indisponiblite_data.date_fin,        date_debut=indisponiblite_data.date_debut,        motif=indisponiblite_data.motif,        sale_evenement=indisponiblite_data.sale_evenement,        reservation_id=indisponiblite_data.reservation        )

    database.add(db_indisponiblite)
    database.commit()
    database.refresh(db_indisponiblite)




    return db_indisponiblite


@app.post("/indisponiblite/bulk/", response_model=None, tags=["Indisponiblite"])
async def bulk_create_indisponiblite(items: list[IndisponibliteCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Indisponiblite entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.reservation:
                raise ValueError("Reservation ID is required")

            db_indisponiblite = Indisponiblite(
                date_fin=item_data.date_fin,                date_debut=item_data.date_debut,                motif=item_data.motif,                sale_evenement=item_data.sale_evenement,                reservation_id=item_data.reservation            )
            database.add(db_indisponiblite)
            database.flush()  # Get ID without committing
            created_items.append(db_indisponiblite.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Indisponiblite entities"
    }


@app.delete("/indisponiblite/bulk/", response_model=None, tags=["Indisponiblite"])
async def bulk_delete_indisponiblite(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Indisponiblite entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_indisponiblite = database.query(Indisponiblite).filter(Indisponiblite.id == item_id).first()
        if db_indisponiblite:
            database.delete(db_indisponiblite)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Indisponiblite entities"
    }

@app.put("/indisponiblite/{indisponiblite_id}/", response_model=None, tags=["Indisponiblite"])
async def update_indisponiblite(indisponiblite_id: int, indisponiblite_data: IndisponibliteCreate, database: Session = Depends(get_db)) -> Indisponiblite:
    db_indisponiblite = database.query(Indisponiblite).filter(Indisponiblite.id == indisponiblite_id).first()
    if db_indisponiblite is None:
        raise HTTPException(status_code=404, detail="Indisponiblite not found")

    setattr(db_indisponiblite, 'date_fin', indisponiblite_data.date_fin)
    setattr(db_indisponiblite, 'date_debut', indisponiblite_data.date_debut)
    setattr(db_indisponiblite, 'motif', indisponiblite_data.motif)
    setattr(db_indisponiblite, 'sale_evenement', indisponiblite_data.sale_evenement)
    if indisponiblite_data.reservation is not None:
        db_reservation = database.query(Reservation).filter(Reservation.id == indisponiblite_data.reservation).first()
        if not db_reservation:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_indisponiblite, 'reservation_id', indisponiblite_data.reservation)
    database.commit()
    database.refresh(db_indisponiblite)

    return db_indisponiblite


@app.delete("/indisponiblite/{indisponiblite_id}/", response_model=None, tags=["Indisponiblite"])
async def delete_indisponiblite(indisponiblite_id: int, database: Session = Depends(get_db)):
    db_indisponiblite = database.query(Indisponiblite).filter(Indisponiblite.id == indisponiblite_id).first()
    if db_indisponiblite is None:
        raise HTTPException(status_code=404, detail="Indisponiblite not found")
    database.delete(db_indisponiblite)
    database.commit()
    return db_indisponiblite





############################################
#
#   Reservation functions
#
############################################

@app.get("/reservation/", response_model=None, tags=["Reservation"])
def get_all_reservation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Reservation)
        query = query.options(joinedload(Reservation.indisponiblite))
        query = query.options(joinedload(Reservation.etre_effectuer))
        reservation_list = query.all()

        # Serialize with relationships included
        result = []
        for reservation_item in reservation_list:
            item_dict = reservation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if reservation_item.indisponiblite:
                related_obj = reservation_item.indisponiblite
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['indisponiblite'] = related_dict
            else:
                item_dict['indisponiblite'] = None
            if reservation_item.etre_effectuer:
                related_obj = reservation_item.etre_effectuer
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['etre_effectuer'] = related_dict
            else:
                item_dict['etre_effectuer'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            option_list = database.query(option).join(reservation_option, option.id == reservation_option.c.peut_inclure).filter(reservation_option.c.peut_etre_presente == reservation_item.id).all()
            item_dict['peut_inclure'] = []
            for option_obj in option_list:
                option_dict = option_obj.__dict__.copy()
                option_dict.pop('_sa_instance_state', None)
                item_dict['peut_inclure'].append(option_dict)
            evenement_list = database.query(Evenement).filter(Evenement.etre_faite_id == reservation_item.id).all()
            item_dict['lier'] = []
            for evenement_obj in evenement_list:
                evenement_dict = evenement_obj.__dict__.copy()
                evenement_dict.pop('_sa_instance_state', None)
                item_dict['lier'].append(evenement_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Reservation).all()


@app.get("/reservation/count/", response_model=None, tags=["Reservation"])
def get_count_reservation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Reservation entities"""
    count = database.query(Reservation).count()
    return {"count": count}


@app.get("/reservation/paginated/", response_model=None, tags=["Reservation"])
def get_paginated_reservation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Reservation entities"""
    total = database.query(Reservation).count()
    reservation_list = database.query(Reservation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": reservation_list
        }

    result = []
    for reservation_item in reservation_list:
        option_ids = database.query(reservation_option.c.peut_inclure).filter(reservation_option.c.peut_etre_presente == reservation_item.id).all()
        lier_ids = database.query(Evenement.id).filter(Evenement.etre_faite_id == reservation_item.id).all()
        item_data = {
            "reservation": reservation_item,
            "option_ids": [x[0] for x in option_ids],
            "lier_ids": [x[0] for x in lier_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/reservation/search/", response_model=None, tags=["Reservation"])
def search_reservation(
    database: Session = Depends(get_db)
) -> list:
    """Search Reservation entities by attributes"""
    query = database.query(Reservation)


    results = query.all()
    return results


@app.get("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def get_reservation(reservation_id: int, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    option_ids = database.query(reservation_option.c.peut_inclure).filter(reservation_option.c.peut_etre_presente == db_reservation.id).all()
    lier_ids = database.query(Evenement.id).filter(Evenement.etre_faite_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "option_ids": [x[0] for x in option_ids],
        "lier_ids": [x[0] for x in lier_ids]}
    return response_data



@app.post("/reservation/", response_model=None, tags=["Reservation"])
async def create_reservation(reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:

    if reservation_data.etre_effectuer is not None:
        db_etre_effectuer = database.query(gestionaire).filter(gestionaire.id == reservation_data.etre_effectuer).first()
        if not db_etre_effectuer:
            raise HTTPException(status_code=400, detail="gestionaire not found")
    else:
        raise HTTPException(status_code=400, detail="gestionaire ID is required")
    if reservation_data.peut_inclure:
        for id in reservation_data.peut_inclure:
            # Entity already validated before creation
            db_option = database.query(option).filter(option.id == id).first()
            if not db_option:
                raise HTTPException(status_code=404, detail=f"option with ID {id} not found")

    db_reservation = Reservation(
        date_debutR=reservation_data.date_debutR,        liste_option=reservation_data.liste_option,        date_finR=reservation_data.date_finR,        nom=reservation_data.nom,        Status=reservation_data.Status.value,        etre_effectuer_id=reservation_data.etre_effectuer        )

    database.add(db_reservation)
    database.commit()
    database.refresh(db_reservation)

    if reservation_data.lier:
        # Validate that all Evenement IDs exist
        for evenement_id in reservation_data.lier:
            db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
            if not db_evenement:
                raise HTTPException(status_code=400, detail=f"Evenement with id {evenement_id} not found")

        # Update the related entities with the new foreign key
        database.query(Evenement).filter(Evenement.id.in_(reservation_data.lier)).update(
            {Evenement.etre_faite_id: db_reservation.id}, synchronize_session=False
        )
        database.commit()

    if reservation_data.peut_inclure:
        for id in reservation_data.peut_inclure:
            # Entity already validated before creation
            db_option = database.query(option).filter(option.id == id).first()
            # Create the association
            association = reservation_option.insert().values(peut_etre_presente=db_reservation.id, peut_inclure=db_option.id)
            database.execute(association)
            database.commit()


    option_ids = database.query(reservation_option.c.peut_inclure).filter(reservation_option.c.peut_etre_presente == db_reservation.id).all()
    lier_ids = database.query(Evenement.id).filter(Evenement.etre_faite_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "option_ids": [x[0] for x in option_ids],
        "lier_ids": [x[0] for x in lier_ids]    }
    return response_data


@app.post("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_create_reservation(items: list[ReservationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Reservation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.etre_effectuer:
                raise ValueError("gestionaire ID is required")

            db_reservation = Reservation(
                date_debutR=item_data.date_debutR,                liste_option=item_data.liste_option,                date_finR=item_data.date_finR,                nom=item_data.nom,                Status=item_data.Status.value,                etre_effectuer_id=item_data.etre_effectuer            )
            database.add(db_reservation)
            database.flush()  # Get ID without committing
            created_items.append(db_reservation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Reservation entities"
    }


@app.delete("/reservation/bulk/", response_model=None, tags=["Reservation"])
async def bulk_delete_reservation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Reservation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == item_id).first()
        if db_reservation:
            database.delete(db_reservation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Reservation entities"
    }

@app.put("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def update_reservation(reservation_id: int, reservation_data: ReservationCreate, database: Session = Depends(get_db)) -> Reservation:
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    setattr(db_reservation, 'date_debutR', reservation_data.date_debutR)
    setattr(db_reservation, 'liste_option', reservation_data.liste_option)
    setattr(db_reservation, 'date_finR', reservation_data.date_finR)
    setattr(db_reservation, 'nom', reservation_data.nom)
    setattr(db_reservation, 'Status', reservation_data.Status.value)
    if reservation_data.etre_effectuer is not None:
        db_etre_effectuer = database.query(gestionaire).filter(gestionaire.id == reservation_data.etre_effectuer).first()
        if not db_etre_effectuer:
            raise HTTPException(status_code=400, detail="gestionaire not found")
        setattr(db_reservation, 'etre_effectuer_id', reservation_data.etre_effectuer)
    if reservation_data.lier is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Evenement).filter(Evenement.etre_faite_id == db_reservation.id).update(
            {Evenement.etre_faite_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if reservation_data.lier:
            # Validate that all IDs exist
            for evenement_id in reservation_data.lier:
                db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
                if not db_evenement:
                    raise HTTPException(status_code=400, detail=f"Evenement with id {evenement_id} not found")

            # Update the related entities with the new foreign key
            database.query(Evenement).filter(Evenement.id.in_(reservation_data.lier)).update(
                {Evenement.etre_faite_id: db_reservation.id}, synchronize_session=False
            )
    existing_option_ids = [assoc.peut_inclure for assoc in database.execute(
        reservation_option.select().where(reservation_option.c.peut_etre_presente == db_reservation.id))]

    options_to_remove = set(existing_option_ids) - set(reservation_data.peut_inclure)
    for option_id in options_to_remove:
        association = reservation_option.delete().where(
            (reservation_option.c.peut_etre_presente == db_reservation.id) & (reservation_option.c.peut_inclure == option_id))
        database.execute(association)

    new_option_ids = set(reservation_data.peut_inclure) - set(existing_option_ids)
    for option_id in new_option_ids:
        db_option = database.query(option).filter(option.id == option_id).first()
        if db_option is None:
            raise HTTPException(status_code=404, detail=f"option with ID {option_id} not found")
        association = reservation_option.insert().values(peut_inclure=db_option.id, peut_etre_presente=db_reservation.id)
        database.execute(association)
    database.commit()
    database.refresh(db_reservation)

    option_ids = database.query(reservation_option.c.peut_inclure).filter(reservation_option.c.peut_etre_presente == db_reservation.id).all()
    lier_ids = database.query(Evenement.id).filter(Evenement.etre_faite_id == db_reservation.id).all()
    response_data = {
        "reservation": db_reservation,
        "option_ids": [x[0] for x in option_ids],
        "lier_ids": [x[0] for x in lier_ids]    }
    return response_data


@app.delete("/reservation/{reservation_id}/", response_model=None, tags=["Reservation"])
async def delete_reservation(reservation_id: int, database: Session = Depends(get_db)):
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    database.delete(db_reservation)
    database.commit()
    return db_reservation

@app.post("/reservation/{reservation_id}/peut_inclure/{option_id}/", response_model=None, tags=["Reservation Relationships"])
async def add_peut_inclure_to_reservation(reservation_id: int, option_id: int, database: Session = Depends(get_db)):
    """Add a option to this Reservation's peut_inclure relationship"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")

    # Check if relationship already exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_etre_presente == reservation_id) &
        (reservation_option.c.peut_inclure == option_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = reservation_option.insert().values(peut_etre_presente=reservation_id, peut_inclure=option_id)
    database.execute(association)
    database.commit()

    return {"message": "option added to peut_inclure successfully"}


@app.delete("/reservation/{reservation_id}/peut_inclure/{option_id}/", response_model=None, tags=["Reservation Relationships"])
async def remove_peut_inclure_from_reservation(reservation_id: int, option_id: int, database: Session = Depends(get_db)):
    """Remove a option from this Reservation's peut_inclure relationship"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_etre_presente == reservation_id) &
        (reservation_option.c.peut_inclure == option_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = reservation_option.delete().where(
        (reservation_option.c.peut_etre_presente == reservation_id) &
        (reservation_option.c.peut_inclure == option_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "option removed from peut_inclure successfully"}


@app.get("/reservation/{reservation_id}/peut_inclure/", response_model=None, tags=["Reservation Relationships"])
async def get_peut_inclure_of_reservation(reservation_id: int, database: Session = Depends(get_db)):
    """Get all option entities related to this Reservation through peut_inclure"""
    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    option_ids = database.query(reservation_option.c.peut_inclure).filter(reservation_option.c.peut_etre_presente == reservation_id).all()
    option_list = database.query(option).filter(option.id.in_([id[0] for id in option_ids])).all()

    return {
        "reservation_id": reservation_id,
        "peut_inclure_count": len(option_list),
        "peut_inclure": option_list
    }



############################################
#   Reservation Method Endpoints
############################################




@app.post("/reservation/methods/calculerprix/", response_model=None, tags=["Reservation Methods"])
async def reservation_calculerprix(
    database: Session = Depends(get_db)
):
    """
    Execute the calculerprix class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "calculerprix",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/inclureOption/", response_model=None, tags=["Reservation Methods"])
async def reservation_inclureOption(
    database: Session = Depends(get_db)
):
    """
    Execute the inclureOption class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "inclureOption",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/methods/annuler/", response_model=None, tags=["Reservation Methods"])
async def reservation_annuler(
    database: Session = Depends(get_db)
):
    """
    Execute the annuler class method on Reservation.
    This method operates on all Reservation entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Reservation",
            "method": "annuler",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/reservation/{reservation_id}/methods/confirmer/", response_model=None, tags=["Reservation Methods"])
async def execute_reservation_confirmer(
    reservation_id: int,
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the confirmer method on a Reservation instance.
    """
    # Retrieve the entity from the database
    _reservation_object = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if _reservation_object is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Prepare method parameters

    # Execute the method
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        async def wrapper(_reservation_object):
            """
            Logique pour confirmer une réservation
            """
            if _reservation_object.statut == "En attente":
                _reservation_object.statut = "Confirmée"
                _reservation_object.est_payee = True
                return True
            return False


        result = await wrapper(_reservation_object)
        # Commit DB
        database.commit()
        database.refresh(_reservation_object)

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        return {
            "reservation_id": reservation_id,
            "method": "confirmer",
            "status": "executed",
            "result": str(result) if result is not None else None,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")



############################################
#
#   gestionaire functions
#
############################################

@app.get("/gestionaire/", response_model=None, tags=["gestionaire"])
def get_all_gestionaire(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(gestionaire)
        gestionaire_list = query.all()

        # Serialize with relationships included
        result = []
        for gestionaire_item in gestionaire_list:
            item_dict = gestionaire_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).filter(Reservation.etre_effectuer_id == gestionaire_item.id).all()
            item_dict['effectuer'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['effectuer'].append(reservation_dict)
            centre_de_congres_list = database.query(Centre_de_congres).filter(Centre_de_congres.etre_reserver_id == gestionaire_item.id).all()
            item_dict['reserver'] = []
            for centre_de_congres_obj in centre_de_congres_list:
                centre_de_congres_dict = centre_de_congres_obj.__dict__.copy()
                centre_de_congres_dict.pop('_sa_instance_state', None)
                item_dict['reserver'].append(centre_de_congres_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(gestionaire).all()


@app.get("/gestionaire/count/", response_model=None, tags=["gestionaire"])
def get_count_gestionaire(database: Session = Depends(get_db)) -> dict:
    """Get the total count of gestionaire entities"""
    count = database.query(gestionaire).count()
    return {"count": count}


@app.get("/gestionaire/paginated/", response_model=None, tags=["gestionaire"])
def get_paginated_gestionaire(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of gestionaire entities"""
    total = database.query(gestionaire).count()
    gestionaire_list = database.query(gestionaire).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": gestionaire_list
        }

    result = []
    for gestionaire_item in gestionaire_list:
        effectuer_ids = database.query(Reservation.id).filter(Reservation.etre_effectuer_id == gestionaire_item.id).all()
        reserver_ids = database.query(Centre_de_congres.id).filter(Centre_de_congres.etre_reserver_id == gestionaire_item.id).all()
        item_data = {
            "gestionaire": gestionaire_item,
            "effectuer_ids": [x[0] for x in effectuer_ids],            "reserver_ids": [x[0] for x in reserver_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/gestionaire/search/", response_model=None, tags=["gestionaire"])
def search_gestionaire(
    database: Session = Depends(get_db)
) -> list:
    """Search gestionaire entities by attributes"""
    query = database.query(gestionaire)


    results = query.all()
    return results


@app.get("/gestionaire/{gestionaire_id}/", response_model=None, tags=["gestionaire"])
async def get_gestionaire(gestionaire_id: int, database: Session = Depends(get_db)) -> gestionaire:
    db_gestionaire = database.query(gestionaire).filter(gestionaire.id == gestionaire_id).first()
    if db_gestionaire is None:
        raise HTTPException(status_code=404, detail="gestionaire not found")

    effectuer_ids = database.query(Reservation.id).filter(Reservation.etre_effectuer_id == db_gestionaire.id).all()
    reserver_ids = database.query(Centre_de_congres.id).filter(Centre_de_congres.etre_reserver_id == db_gestionaire.id).all()
    response_data = {
        "gestionaire": db_gestionaire,
        "effectuer_ids": [x[0] for x in effectuer_ids],        "reserver_ids": [x[0] for x in reserver_ids]}
    return response_data



@app.post("/gestionaire/", response_model=None, tags=["gestionaire"])
async def create_gestionaire(gestionaire_data: gestionaireCreate, database: Session = Depends(get_db)) -> gestionaire:


    db_gestionaire = gestionaire(
        liste_dispoibilités_passées=gestionaire_data.liste_dispoibilités_passées,        date_du_jour=gestionaire_data.date_du_jour,        liste_diponiblité=gestionaire_data.liste_diponiblité,        liste_congres=gestionaire_data.liste_congres        )

    database.add(db_gestionaire)
    database.commit()
    database.refresh(db_gestionaire)

    if gestionaire_data.effectuer:
        # Validate that all Reservation IDs exist
        for reservation_id in gestionaire_data.effectuer:
            db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
            if not db_reservation:
                raise HTTPException(status_code=400, detail=f"Reservation with id {reservation_id} not found")

        # Update the related entities with the new foreign key
        database.query(Reservation).filter(Reservation.id.in_(gestionaire_data.effectuer)).update(
            {Reservation.etre_effectuer_id: db_gestionaire.id}, synchronize_session=False
        )
        database.commit()
    if gestionaire_data.reserver:
        # Validate that all Centre_de_congres IDs exist
        for centre_de_congres_id in gestionaire_data.reserver:
            db_centre_de_congres = database.query(Centre_de_congres).filter(Centre_de_congres.id == centre_de_congres_id).first()
            if not db_centre_de_congres:
                raise HTTPException(status_code=400, detail=f"Centre_de_congres with id {centre_de_congres_id} not found")

        # Update the related entities with the new foreign key
        database.query(Centre_de_congres).filter(Centre_de_congres.id.in_(gestionaire_data.reserver)).update(
            {Centre_de_congres.etre_reserver_id: db_gestionaire.id}, synchronize_session=False
        )
        database.commit()



    effectuer_ids = database.query(Reservation.id).filter(Reservation.etre_effectuer_id == db_gestionaire.id).all()
    reserver_ids = database.query(Centre_de_congres.id).filter(Centre_de_congres.etre_reserver_id == db_gestionaire.id).all()
    response_data = {
        "gestionaire": db_gestionaire,
        "effectuer_ids": [x[0] for x in effectuer_ids],        "reserver_ids": [x[0] for x in reserver_ids]    }
    return response_data


@app.post("/gestionaire/bulk/", response_model=None, tags=["gestionaire"])
async def bulk_create_gestionaire(items: list[gestionaireCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple gestionaire entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_gestionaire = gestionaire(
                liste_dispoibilités_passées=item_data.liste_dispoibilités_passées,                date_du_jour=item_data.date_du_jour,                liste_diponiblité=item_data.liste_diponiblité,                liste_congres=item_data.liste_congres            )
            database.add(db_gestionaire)
            database.flush()  # Get ID without committing
            created_items.append(db_gestionaire.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} gestionaire entities"
    }


@app.delete("/gestionaire/bulk/", response_model=None, tags=["gestionaire"])
async def bulk_delete_gestionaire(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple gestionaire entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_gestionaire = database.query(gestionaire).filter(gestionaire.id == item_id).first()
        if db_gestionaire:
            database.delete(db_gestionaire)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} gestionaire entities"
    }

@app.put("/gestionaire/{gestionaire_id}/", response_model=None, tags=["gestionaire"])
async def update_gestionaire(gestionaire_id: int, gestionaire_data: gestionaireCreate, database: Session = Depends(get_db)) -> gestionaire:
    db_gestionaire = database.query(gestionaire).filter(gestionaire.id == gestionaire_id).first()
    if db_gestionaire is None:
        raise HTTPException(status_code=404, detail="gestionaire not found")

    setattr(db_gestionaire, 'liste_dispoibilités_passées', gestionaire_data.liste_dispoibilités_passées)
    setattr(db_gestionaire, 'date_du_jour', gestionaire_data.date_du_jour)
    setattr(db_gestionaire, 'liste_diponiblité', gestionaire_data.liste_diponiblité)
    setattr(db_gestionaire, 'liste_congres', gestionaire_data.liste_congres)
    if gestionaire_data.effectuer is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Reservation).filter(Reservation.etre_effectuer_id == db_gestionaire.id).update(
            {Reservation.etre_effectuer_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if gestionaire_data.effectuer:
            # Validate that all IDs exist
            for reservation_id in gestionaire_data.effectuer:
                db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
                if not db_reservation:
                    raise HTTPException(status_code=400, detail=f"Reservation with id {reservation_id} not found")

            # Update the related entities with the new foreign key
            database.query(Reservation).filter(Reservation.id.in_(gestionaire_data.effectuer)).update(
                {Reservation.etre_effectuer_id: db_gestionaire.id}, synchronize_session=False
            )
    if gestionaire_data.reserver is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(Centre_de_congres).filter(Centre_de_congres.etre_reserver_id == db_gestionaire.id).update(
            {Centre_de_congres.etre_reserver_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if gestionaire_data.reserver:
            # Validate that all IDs exist
            for centre_de_congres_id in gestionaire_data.reserver:
                db_centre_de_congres = database.query(Centre_de_congres).filter(Centre_de_congres.id == centre_de_congres_id).first()
                if not db_centre_de_congres:
                    raise HTTPException(status_code=400, detail=f"Centre_de_congres with id {centre_de_congres_id} not found")

            # Update the related entities with the new foreign key
            database.query(Centre_de_congres).filter(Centre_de_congres.id.in_(gestionaire_data.reserver)).update(
                {Centre_de_congres.etre_reserver_id: db_gestionaire.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_gestionaire)

    effectuer_ids = database.query(Reservation.id).filter(Reservation.etre_effectuer_id == db_gestionaire.id).all()
    reserver_ids = database.query(Centre_de_congres.id).filter(Centre_de_congres.etre_reserver_id == db_gestionaire.id).all()
    response_data = {
        "gestionaire": db_gestionaire,
        "effectuer_ids": [x[0] for x in effectuer_ids],        "reserver_ids": [x[0] for x in reserver_ids]    }
    return response_data


@app.delete("/gestionaire/{gestionaire_id}/", response_model=None, tags=["gestionaire"])
async def delete_gestionaire(gestionaire_id: int, database: Session = Depends(get_db)):
    db_gestionaire = database.query(gestionaire).filter(gestionaire.id == gestionaire_id).first()
    if db_gestionaire is None:
        raise HTTPException(status_code=404, detail="gestionaire not found")
    database.delete(db_gestionaire)
    database.commit()
    return db_gestionaire



############################################
#   gestionaire Method Endpoints
############################################




@app.post("/gestionaire/methods/verifieDisponibilite/", response_model=None, tags=["gestionaire Methods"])
async def gestionaire_verifieDisponibilite(
    database: Session = Depends(get_db)
):
    """
    Execute the verifieDisponibilite class method on gestionaire.
    This method operates on all gestionaire entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "gestionaire",
            "method": "verifieDisponibilite",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/gestionaire/methods/ajouterOptions/", response_model=None, tags=["gestionaire Methods"])
async def gestionaire_ajouterOptions(
    database: Session = Depends(get_db)
):
    """
    Execute the ajouterOptions class method on gestionaire.
    This method operates on all gestionaire entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "gestionaire",
            "method": "ajouterOptions",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






@app.post("/gestionaire/methods/creerReservation/", response_model=None, tags=["gestionaire Methods"])
async def gestionaire_creerReservation(
    database: Session = Depends(get_db)
):
    """
    Execute the creerReservation class method on gestionaire.
    This method operates on all gestionaire entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "gestionaire",
            "method": "creerReservation",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   option functions
#
############################################

@app.get("/option/", response_model=None, tags=["option"])
def get_all_option(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(option)
        option_list = query.all()

        # Serialize with relationships included
        result = []
        for option_item in option_list:
            item_dict = option_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).join(reservation_option, Reservation.id == reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == option_item.id).all()
            item_dict['peut_etre_presente'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['peut_etre_presente'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(option).all()


@app.get("/option/count/", response_model=None, tags=["option"])
def get_count_option(database: Session = Depends(get_db)) -> dict:
    """Get the total count of option entities"""
    count = database.query(option).count()
    return {"count": count}


@app.get("/option/paginated/", response_model=None, tags=["option"])
def get_paginated_option(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of option entities"""
    total = database.query(option).count()
    option_list = database.query(option).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": option_list
        }

    result = []
    for option_item in option_list:
        reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == option_item.id).all()
        item_data = {
            "option": option_item,
            "reservation_ids": [x[0] for x in reservation_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/option/search/", response_model=None, tags=["option"])
def search_option(
    database: Session = Depends(get_db)
) -> list:
    """Search option entities by attributes"""
    query = database.query(option)


    results = query.all()
    return results


@app.get("/option/{option_id}/", response_model=None, tags=["option"])
async def get_option(option_id: int, database: Session = Depends(get_db)) -> option:
    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_option.id).all()
    response_data = {
        "option": db_option,
        "reservation_ids": [x[0] for x in reservation_ids],
}
    return response_data



@app.post("/option/", response_model=None, tags=["option"])
async def create_option(option_data: optionCreate, database: Session = Depends(get_db)) -> option:

    if option_data.peut_etre_presente:
        for id in option_data.peut_etre_presente:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            if not db_reservation:
                raise HTTPException(status_code=404, detail=f"Reservation with ID {id} not found")

    db_option = option(
        nomO=option_data.nomO        )

    database.add(db_option)
    database.commit()
    database.refresh(db_option)


    if option_data.peut_etre_presente:
        for id in option_data.peut_etre_presente:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            # Create the association
            association = reservation_option.insert().values(peut_inclure=db_option.id, peut_etre_presente=db_reservation.id)
            database.execute(association)
            database.commit()


    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_option.id).all()
    response_data = {
        "option": db_option,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.post("/option/bulk/", response_model=None, tags=["option"])
async def bulk_create_option(items: list[optionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple option entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_option = option(
                nomO=item_data.nomO            )
            database.add(db_option)
            database.flush()  # Get ID without committing
            created_items.append(db_option.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} option entities"
    }


@app.delete("/option/bulk/", response_model=None, tags=["option"])
async def bulk_delete_option(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple option entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_option = database.query(option).filter(option.id == item_id).first()
        if db_option:
            database.delete(db_option)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} option entities"
    }

@app.put("/option/{option_id}/", response_model=None, tags=["option"])
async def update_option(option_id: int, option_data: optionCreate, database: Session = Depends(get_db)) -> option:
    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")

    setattr(db_option, 'nomO', option_data.nomO)
    existing_reservation_ids = [assoc.peut_etre_presente for assoc in database.execute(
        reservation_option.select().where(reservation_option.c.peut_inclure == db_option.id))]

    reservations_to_remove = set(existing_reservation_ids) - set(option_data.peut_etre_presente)
    for reservation_id in reservations_to_remove:
        association = reservation_option.delete().where(
            (reservation_option.c.peut_inclure == db_option.id) & (reservation_option.c.peut_etre_presente == reservation_id))
        database.execute(association)

    new_reservation_ids = set(option_data.peut_etre_presente) - set(existing_reservation_ids)
    for reservation_id in new_reservation_ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
        if db_reservation is None:
            raise HTTPException(status_code=404, detail=f"Reservation with ID {reservation_id} not found")
        association = reservation_option.insert().values(peut_etre_presente=db_reservation.id, peut_inclure=db_option.id)
        database.execute(association)
    database.commit()
    database.refresh(db_option)

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_option.id).all()
    response_data = {
        "option": db_option,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.delete("/option/{option_id}/", response_model=None, tags=["option"])
async def delete_option(option_id: int, database: Session = Depends(get_db)):
    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")
    database.delete(db_option)
    database.commit()
    return db_option

@app.post("/option/{option_id}/peut_etre_presente/{reservation_id}/", response_model=None, tags=["option Relationships"])
async def add_peut_etre_presente_to_option(option_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Add a Reservation to this option's peut_etre_presente relationship"""
    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")

    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship already exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_inclure == option_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = reservation_option.insert().values(peut_inclure=option_id, peut_etre_presente=reservation_id)
    database.execute(association)
    database.commit()

    return {"message": "Reservation added to peut_etre_presente successfully"}


@app.delete("/option/{option_id}/peut_etre_presente/{reservation_id}/", response_model=None, tags=["option Relationships"])
async def remove_peut_etre_presente_from_option(option_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Remove a Reservation from this option's peut_etre_presente relationship"""
    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")

    # Check if relationship exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_inclure == option_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = reservation_option.delete().where(
        (reservation_option.c.peut_inclure == option_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Reservation removed from peut_etre_presente successfully"}


@app.get("/option/{option_id}/peut_etre_presente/", response_model=None, tags=["option Relationships"])
async def get_peut_etre_presente_of_option(option_id: int, database: Session = Depends(get_db)):
    """Get all Reservation entities related to this option through peut_etre_presente"""
    db_option = database.query(option).filter(option.id == option_id).first()
    if db_option is None:
        raise HTTPException(status_code=404, detail="option not found")

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == option_id).all()
    reservation_list = database.query(Reservation).filter(Reservation.id.in_([id[0] for id in reservation_ids])).all()

    return {
        "option_id": option_id,
        "peut_etre_presente_count": len(reservation_list),
        "peut_etre_presente": reservation_list
    }





############################################
#
#   prestation functions
#
############################################

@app.get("/prestation/", response_model=None, tags=["prestation"])
def get_all_prestation(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(prestation)
        prestation_list = query.all()

        # Serialize with relationships included
        result = []
        for prestation_item in prestation_list:
            item_dict = prestation_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).join(reservation_option, Reservation.id == reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == prestation_item.id).all()
            item_dict['peut_etre_presente'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['peut_etre_presente'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(prestation).all()


@app.get("/prestation/count/", response_model=None, tags=["prestation"])
def get_count_prestation(database: Session = Depends(get_db)) -> dict:
    """Get the total count of prestation entities"""
    count = database.query(prestation).count()
    return {"count": count}


@app.get("/prestation/paginated/", response_model=None, tags=["prestation"])
def get_paginated_prestation(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of prestation entities"""
    total = database.query(prestation).count()
    prestation_list = database.query(prestation).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": prestation_list
        }

    result = []
    for prestation_item in prestation_list:
        reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == prestation_item.id).all()
        item_data = {
            "prestation": prestation_item,
            "reservation_ids": [x[0] for x in reservation_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/prestation/search/", response_model=None, tags=["prestation"])
def search_prestation(
    database: Session = Depends(get_db)
) -> list:
    """Search prestation entities by attributes"""
    query = database.query(prestation)


    results = query.all()
    return results


@app.get("/prestation/{prestation_id}/", response_model=None, tags=["prestation"])
async def get_prestation(prestation_id: int, database: Session = Depends(get_db)) -> prestation:
    db_prestation = database.query(prestation).filter(prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="prestation not found")

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_prestation.id).all()
    response_data = {
        "prestation": db_prestation,
        "reservation_ids": [x[0] for x in reservation_ids],
}
    return response_data



@app.post("/prestation/", response_model=None, tags=["prestation"])
async def create_prestation(prestation_data: prestationCreate, database: Session = Depends(get_db)) -> prestation:

    if prestation_data.peut_etre_presente:
        for id in prestation_data.peut_etre_presente:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            if not db_reservation:
                raise HTTPException(status_code=404, detail=f"Reservation with ID {id} not found")

    db_prestation = prestation(
        nomO=prestation_data.nomO,        type=prestation_data.type        )

    database.add(db_prestation)
    database.commit()
    database.refresh(db_prestation)


    if prestation_data.peut_etre_presente:
        for id in prestation_data.peut_etre_presente:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            # Create the association
            association = reservation_option.insert().values(peut_inclure=db_prestation.id, peut_etre_presente=db_reservation.id)
            database.execute(association)
            database.commit()


    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_prestation.id).all()
    response_data = {
        "prestation": db_prestation,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.post("/prestation/bulk/", response_model=None, tags=["prestation"])
async def bulk_create_prestation(items: list[prestationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple prestation entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_prestation = prestation(
                nomO=item_data.nomO,                type=item_data.type            )
            database.add(db_prestation)
            database.flush()  # Get ID without committing
            created_items.append(db_prestation.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} prestation entities"
    }


@app.delete("/prestation/bulk/", response_model=None, tags=["prestation"])
async def bulk_delete_prestation(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple prestation entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_prestation = database.query(prestation).filter(prestation.id == item_id).first()
        if db_prestation:
            database.delete(db_prestation)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} prestation entities"
    }

@app.put("/prestation/{prestation_id}/", response_model=None, tags=["prestation"])
async def update_prestation(prestation_id: int, prestation_data: prestationCreate, database: Session = Depends(get_db)) -> prestation:
    db_prestation = database.query(prestation).filter(prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="prestation not found")

    setattr(db_prestation, 'type', prestation_data.type)
    existing_reservation_ids = [assoc.peut_etre_presente for assoc in database.execute(
        reservation_option.select().where(reservation_option.c.peut_inclure == db_prestation.id))]

    reservations_to_remove = set(existing_reservation_ids) - set(prestation_data.peut_etre_presente)
    for reservation_id in reservations_to_remove:
        association = reservation_option.delete().where(
            (reservation_option.c.peut_inclure == db_prestation.id) & (reservation_option.c.peut_etre_presente == reservation_id))
        database.execute(association)

    new_reservation_ids = set(prestation_data.peut_etre_presente) - set(existing_reservation_ids)
    for reservation_id in new_reservation_ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
        if db_reservation is None:
            raise HTTPException(status_code=404, detail=f"Reservation with ID {reservation_id} not found")
        association = reservation_option.insert().values(peut_etre_presente=db_reservation.id, peut_inclure=db_prestation.id)
        database.execute(association)
    database.commit()
    database.refresh(db_prestation)

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_prestation.id).all()
    response_data = {
        "prestation": db_prestation,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.delete("/prestation/{prestation_id}/", response_model=None, tags=["prestation"])
async def delete_prestation(prestation_id: int, database: Session = Depends(get_db)):
    db_prestation = database.query(prestation).filter(prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="prestation not found")
    database.delete(db_prestation)
    database.commit()
    return db_prestation

@app.post("/prestation/{prestation_id}/peut_etre_presente/{reservation_id}/", response_model=None, tags=["prestation Relationships"])
async def add_peut_etre_presente_to_prestation(prestation_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Add a Reservation to this prestation's peut_etre_presente relationship"""
    db_prestation = database.query(prestation).filter(prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="prestation not found")

    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship already exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_inclure == prestation_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = reservation_option.insert().values(peut_inclure=prestation_id, peut_etre_presente=reservation_id)
    database.execute(association)
    database.commit()

    return {"message": "Reservation added to peut_etre_presente successfully"}


@app.delete("/prestation/{prestation_id}/peut_etre_presente/{reservation_id}/", response_model=None, tags=["prestation Relationships"])
async def remove_peut_etre_presente_from_prestation(prestation_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Remove a Reservation from this prestation's peut_etre_presente relationship"""
    db_prestation = database.query(prestation).filter(prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="prestation not found")

    # Check if relationship exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_inclure == prestation_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = reservation_option.delete().where(
        (reservation_option.c.peut_inclure == prestation_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Reservation removed from peut_etre_presente successfully"}


@app.get("/prestation/{prestation_id}/peut_etre_presente/", response_model=None, tags=["prestation Relationships"])
async def get_peut_etre_presente_of_prestation(prestation_id: int, database: Session = Depends(get_db)):
    """Get all Reservation entities related to this prestation through peut_etre_presente"""
    db_prestation = database.query(prestation).filter(prestation.id == prestation_id).first()
    if db_prestation is None:
        raise HTTPException(status_code=404, detail="prestation not found")

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == prestation_id).all()
    reservation_list = database.query(Reservation).filter(Reservation.id.in_([id[0] for id in reservation_ids])).all()

    return {
        "prestation_id": prestation_id,
        "peut_etre_presente_count": len(reservation_list),
        "peut_etre_presente": reservation_list
    }





############################################
#
#   materiel functions
#
############################################

@app.get("/materiel/", response_model=None, tags=["materiel"])
def get_all_materiel(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(materiel)
        materiel_list = query.all()

        # Serialize with relationships included
        result = []
        for materiel_item in materiel_list:
            item_dict = materiel_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            reservation_list = database.query(Reservation).join(reservation_option, Reservation.id == reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == materiel_item.id).all()
            item_dict['peut_etre_presente'] = []
            for reservation_obj in reservation_list:
                reservation_dict = reservation_obj.__dict__.copy()
                reservation_dict.pop('_sa_instance_state', None)
                item_dict['peut_etre_presente'].append(reservation_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(materiel).all()


@app.get("/materiel/count/", response_model=None, tags=["materiel"])
def get_count_materiel(database: Session = Depends(get_db)) -> dict:
    """Get the total count of materiel entities"""
    count = database.query(materiel).count()
    return {"count": count}


@app.get("/materiel/paginated/", response_model=None, tags=["materiel"])
def get_paginated_materiel(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of materiel entities"""
    total = database.query(materiel).count()
    materiel_list = database.query(materiel).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": materiel_list
        }

    result = []
    for materiel_item in materiel_list:
        reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == materiel_item.id).all()
        item_data = {
            "materiel": materiel_item,
            "reservation_ids": [x[0] for x in reservation_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/materiel/search/", response_model=None, tags=["materiel"])
def search_materiel(
    database: Session = Depends(get_db)
) -> list:
    """Search materiel entities by attributes"""
    query = database.query(materiel)


    results = query.all()
    return results


@app.get("/materiel/{materiel_id}/", response_model=None, tags=["materiel"])
async def get_materiel(materiel_id: int, database: Session = Depends(get_db)) -> materiel:
    db_materiel = database.query(materiel).filter(materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="materiel not found")

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "reservation_ids": [x[0] for x in reservation_ids],
}
    return response_data



@app.post("/materiel/", response_model=None, tags=["materiel"])
async def create_materiel(materiel_data: materielCreate, database: Session = Depends(get_db)) -> materiel:

    if materiel_data.peut_etre_presente:
        for id in materiel_data.peut_etre_presente:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            if not db_reservation:
                raise HTTPException(status_code=404, detail=f"Reservation with ID {id} not found")

    db_materiel = materiel(
        nomO=materiel_data.nomO,        quantite=materiel_data.quantite,        nom=materiel_data.nom        )

    database.add(db_materiel)
    database.commit()
    database.refresh(db_materiel)


    if materiel_data.peut_etre_presente:
        for id in materiel_data.peut_etre_presente:
            # Entity already validated before creation
            db_reservation = database.query(Reservation).filter(Reservation.id == id).first()
            # Create the association
            association = reservation_option.insert().values(peut_inclure=db_materiel.id, peut_etre_presente=db_reservation.id)
            database.execute(association)
            database.commit()


    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.post("/materiel/bulk/", response_model=None, tags=["materiel"])
async def bulk_create_materiel(items: list[materielCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple materiel entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_materiel = materiel(
                nomO=item_data.nomO,                quantite=item_data.quantite,                nom=item_data.nom            )
            database.add(db_materiel)
            database.flush()  # Get ID without committing
            created_items.append(db_materiel.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} materiel entities"
    }


@app.delete("/materiel/bulk/", response_model=None, tags=["materiel"])
async def bulk_delete_materiel(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple materiel entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_materiel = database.query(materiel).filter(materiel.id == item_id).first()
        if db_materiel:
            database.delete(db_materiel)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} materiel entities"
    }

@app.put("/materiel/{materiel_id}/", response_model=None, tags=["materiel"])
async def update_materiel(materiel_id: int, materiel_data: materielCreate, database: Session = Depends(get_db)) -> materiel:
    db_materiel = database.query(materiel).filter(materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="materiel not found")

    setattr(db_materiel, 'quantite', materiel_data.quantite)
    setattr(db_materiel, 'nom', materiel_data.nom)
    existing_reservation_ids = [assoc.peut_etre_presente for assoc in database.execute(
        reservation_option.select().where(reservation_option.c.peut_inclure == db_materiel.id))]

    reservations_to_remove = set(existing_reservation_ids) - set(materiel_data.peut_etre_presente)
    for reservation_id in reservations_to_remove:
        association = reservation_option.delete().where(
            (reservation_option.c.peut_inclure == db_materiel.id) & (reservation_option.c.peut_etre_presente == reservation_id))
        database.execute(association)

    new_reservation_ids = set(materiel_data.peut_etre_presente) - set(existing_reservation_ids)
    for reservation_id in new_reservation_ids:
        db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
        if db_reservation is None:
            raise HTTPException(status_code=404, detail=f"Reservation with ID {reservation_id} not found")
        association = reservation_option.insert().values(peut_etre_presente=db_reservation.id, peut_inclure=db_materiel.id)
        database.execute(association)
    database.commit()
    database.refresh(db_materiel)

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == db_materiel.id).all()
    response_data = {
        "materiel": db_materiel,
        "reservation_ids": [x[0] for x in reservation_ids],
    }
    return response_data


@app.delete("/materiel/{materiel_id}/", response_model=None, tags=["materiel"])
async def delete_materiel(materiel_id: int, database: Session = Depends(get_db)):
    db_materiel = database.query(materiel).filter(materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="materiel not found")
    database.delete(db_materiel)
    database.commit()
    return db_materiel

@app.post("/materiel/{materiel_id}/peut_etre_presente/{reservation_id}/", response_model=None, tags=["materiel Relationships"])
async def add_peut_etre_presente_to_materiel(materiel_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Add a Reservation to this materiel's peut_etre_presente relationship"""
    db_materiel = database.query(materiel).filter(materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="materiel not found")

    db_reservation = database.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Check if relationship already exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_inclure == materiel_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = reservation_option.insert().values(peut_inclure=materiel_id, peut_etre_presente=reservation_id)
    database.execute(association)
    database.commit()

    return {"message": "Reservation added to peut_etre_presente successfully"}


@app.delete("/materiel/{materiel_id}/peut_etre_presente/{reservation_id}/", response_model=None, tags=["materiel Relationships"])
async def remove_peut_etre_presente_from_materiel(materiel_id: int, reservation_id: int, database: Session = Depends(get_db)):
    """Remove a Reservation from this materiel's peut_etre_presente relationship"""
    db_materiel = database.query(materiel).filter(materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="materiel not found")

    # Check if relationship exists
    existing = database.query(reservation_option).filter(
        (reservation_option.c.peut_inclure == materiel_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = reservation_option.delete().where(
        (reservation_option.c.peut_inclure == materiel_id) &
        (reservation_option.c.peut_etre_presente == reservation_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Reservation removed from peut_etre_presente successfully"}


@app.get("/materiel/{materiel_id}/peut_etre_presente/", response_model=None, tags=["materiel Relationships"])
async def get_peut_etre_presente_of_materiel(materiel_id: int, database: Session = Depends(get_db)):
    """Get all Reservation entities related to this materiel through peut_etre_presente"""
    db_materiel = database.query(materiel).filter(materiel.id == materiel_id).first()
    if db_materiel is None:
        raise HTTPException(status_code=404, detail="materiel not found")

    reservation_ids = database.query(reservation_option.c.peut_etre_presente).filter(reservation_option.c.peut_inclure == materiel_id).all()
    reservation_list = database.query(Reservation).filter(Reservation.id.in_([id[0] for id in reservation_ids])).all()

    return {
        "materiel_id": materiel_id,
        "peut_etre_presente_count": len(reservation_list),
        "peut_etre_presente": reservation_list
    }





############################################
#
#   Evenement functions
#
############################################

@app.get("/evenement/", response_model=None, tags=["Evenement"])
def get_all_evenement(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Evenement)
        query = query.options(joinedload(Evenement.etre_faite))
        evenement_list = query.all()

        # Serialize with relationships included
        result = []
        for evenement_item in evenement_list:
            item_dict = evenement_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if evenement_item.etre_faite:
                related_obj = evenement_item.etre_faite
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['etre_faite'] = related_dict
            else:
                item_dict['etre_faite'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Evenement).all()


@app.get("/evenement/count/", response_model=None, tags=["Evenement"])
def get_count_evenement(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Evenement entities"""
    count = database.query(Evenement).count()
    return {"count": count}


@app.get("/evenement/paginated/", response_model=None, tags=["Evenement"])
def get_paginated_evenement(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Evenement entities"""
    total = database.query(Evenement).count()
    evenement_list = database.query(Evenement).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": evenement_list
    }


@app.get("/evenement/search/", response_model=None, tags=["Evenement"])
def search_evenement(
    database: Session = Depends(get_db)
) -> list:
    """Search Evenement entities by attributes"""
    query = database.query(Evenement)


    results = query.all()
    return results


@app.get("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def get_evenement(evenement_id: int, database: Session = Depends(get_db)) -> Evenement:
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")

    response_data = {
        "evenement": db_evenement,
}
    return response_data



@app.post("/evenement/", response_model=None, tags=["Evenement"])
async def create_evenement(evenement_data: EvenementCreate, database: Session = Depends(get_db)) -> Evenement:

    if evenement_data.etre_faite :
        db_etre_faite = database.query(Reservation).filter(Reservation.id == evenement_data.etre_faite).first()
        if not db_etre_faite:
            raise HTTPException(status_code=400, detail="Reservation not found")

    db_evenement = Evenement(
        nomEve=evenement_data.nomEve,        description=evenement_data.description,        nbpartion=evenement_data.nbpartion,        emailReferent=evenement_data.emailReferent,        etre_faite_id=evenement_data.etre_faite        )

    database.add(db_evenement)
    database.commit()
    database.refresh(db_evenement)




    return db_evenement


@app.post("/evenement/bulk/", response_model=None, tags=["Evenement"])
async def bulk_create_evenement(items: list[EvenementCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Evenement entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_evenement = Evenement(
                nomEve=item_data.nomEve,                description=item_data.description,                nbpartion=item_data.nbpartion,                emailReferent=item_data.emailReferent,                etre_faite_id=item_data.etre_faite            )
            database.add(db_evenement)
            database.flush()  # Get ID without committing
            created_items.append(db_evenement.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Evenement entities"
    }


@app.delete("/evenement/bulk/", response_model=None, tags=["Evenement"])
async def bulk_delete_evenement(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Evenement entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_evenement = database.query(Evenement).filter(Evenement.id == item_id).first()
        if db_evenement:
            database.delete(db_evenement)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Evenement entities"
    }

@app.put("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def update_evenement(evenement_id: int, evenement_data: EvenementCreate, database: Session = Depends(get_db)) -> Evenement:
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")

    setattr(db_evenement, 'nomEve', evenement_data.nomEve)
    setattr(db_evenement, 'description', evenement_data.description)
    setattr(db_evenement, 'nbpartion', evenement_data.nbpartion)
    setattr(db_evenement, 'emailReferent', evenement_data.emailReferent)
    if evenement_data.etre_faite is not None:
        db_etre_faite = database.query(Reservation).filter(Reservation.id == evenement_data.etre_faite).first()
        if not db_etre_faite:
            raise HTTPException(status_code=400, detail="Reservation not found")
        setattr(db_evenement, 'etre_faite_id', evenement_data.etre_faite)
    else:
        setattr(db_evenement, 'etre_faite_id', None)
    database.commit()
    database.refresh(db_evenement)

    return db_evenement


@app.delete("/evenement/{evenement_id}/", response_model=None, tags=["Evenement"])
async def delete_evenement(evenement_id: int, database: Session = Depends(get_db)):
    db_evenement = database.query(Evenement).filter(Evenement.id == evenement_id).first()
    if db_evenement is None:
        raise HTTPException(status_code=404, detail="Evenement not found")
    database.delete(db_evenement)
    database.commit()
    return db_evenement





############################################
#
#   Element functions
#
############################################

@app.get("/element/", response_model=None, tags=["Element"])
def get_all_element(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    return database.query(Element).all()


@app.get("/element/count/", response_model=None, tags=["Element"])
def get_count_element(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Element entities"""
    count = database.query(Element).count()
    return {"count": count}


@app.get("/element/paginated/", response_model=None, tags=["Element"])
def get_paginated_element(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Element entities"""
    total = database.query(Element).count()
    element_list = database.query(Element).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": element_list
    }


@app.get("/element/search/", response_model=None, tags=["Element"])
def search_element(
    database: Session = Depends(get_db)
) -> list:
    """Search Element entities by attributes"""
    query = database.query(Element)


    results = query.all()
    return results


@app.get("/element/{element_id}/", response_model=None, tags=["Element"])
async def get_element(element_id: int, database: Session = Depends(get_db)) -> Element:
    db_element = database.query(Element).filter(Element.id == element_id).first()
    if db_element is None:
        raise HTTPException(status_code=404, detail="Element not found")

    response_data = {
        "element": db_element,
}
    return response_data



@app.post("/element/", response_model=None, tags=["Element"])
async def create_element(element_data: ElementCreate, database: Session = Depends(get_db)) -> Element:


    db_element = Element(
        cap_max=element_data.cap_max,        nomE=element_data.nomE        )

    database.add(db_element)
    database.commit()
    database.refresh(db_element)




    return db_element


@app.post("/element/bulk/", response_model=None, tags=["Element"])
async def bulk_create_element(items: list[ElementCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Element entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_element = Element(
                cap_max=item_data.cap_max,                nomE=item_data.nomE            )
            database.add(db_element)
            database.flush()  # Get ID without committing
            created_items.append(db_element.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Element entities"
    }


@app.delete("/element/bulk/", response_model=None, tags=["Element"])
async def bulk_delete_element(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Element entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_element = database.query(Element).filter(Element.id == item_id).first()
        if db_element:
            database.delete(db_element)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Element entities"
    }

@app.put("/element/{element_id}/", response_model=None, tags=["Element"])
async def update_element(element_id: int, element_data: ElementCreate, database: Session = Depends(get_db)) -> Element:
    db_element = database.query(Element).filter(Element.id == element_id).first()
    if db_element is None:
        raise HTTPException(status_code=404, detail="Element not found")

    setattr(db_element, 'cap_max', element_data.cap_max)
    setattr(db_element, 'nomE', element_data.nomE)
    database.commit()
    database.refresh(db_element)

    return db_element


@app.delete("/element/{element_id}/", response_model=None, tags=["Element"])
async def delete_element(element_id: int, database: Session = Depends(get_db)):
    db_element = database.query(Element).filter(Element.id == element_id).first()
    if db_element is None:
        raise HTTPException(status_code=404, detail="Element not found")
    database.delete(db_element)
    database.commit()
    return db_element



############################################
#   Element Method Endpoints
############################################




@app.post("/element/methods/estDisponible/", response_model=None, tags=["Element Methods"])
async def element_estDisponible(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the estDisponible class method on Element.
    This method operates on all Element entities or performs class-level operations.

    Parameters (pass as JSON body):
    - date_debut: Any    - date_fin: Any    - liste_disponiblite: Any    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        date_debut = params.get('date_debut')
        date_fin = params.get('date_fin')
        liste_disponiblite = params.get('liste_disponiblite')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Element",
            "method": "estDisponible",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   Centre_de_congres functions
#
############################################

@app.get("/centre_de_congres/", response_model=None, tags=["Centre_de_congres"])
def get_all_centre_de_congres(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Centre_de_congres)
        query = query.options(joinedload(Centre_de_congres.etre_reserver))
        centre_de_congres_list = query.all()

        # Serialize with relationships included
        result = []
        for centre_de_congres_item in centre_de_congres_list:
            item_dict = centre_de_congres_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if centre_de_congres_item.etre_reserver:
                related_obj = centre_de_congres_item.etre_reserver
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['etre_reserver'] = related_dict
            else:
                item_dict['etre_reserver'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Centre_de_congres).all()


@app.get("/centre_de_congres/count/", response_model=None, tags=["Centre_de_congres"])
def get_count_centre_de_congres(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Centre_de_congres entities"""
    count = database.query(Centre_de_congres).count()
    return {"count": count}


@app.get("/centre_de_congres/paginated/", response_model=None, tags=["Centre_de_congres"])
def get_paginated_centre_de_congres(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Centre_de_congres entities"""
    total = database.query(Centre_de_congres).count()
    centre_de_congres_list = database.query(Centre_de_congres).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": centre_de_congres_list
    }


@app.get("/centre_de_congres/search/", response_model=None, tags=["Centre_de_congres"])
def search_centre_de_congres(
    database: Session = Depends(get_db)
) -> list:
    """Search Centre_de_congres entities by attributes"""
    query = database.query(Centre_de_congres)


    results = query.all()
    return results


@app.get("/centre_de_congres/{centre_de_congres_id}/", response_model=None, tags=["Centre_de_congres"])
async def get_centre_de_congres(centre_de_congres_id: int, database: Session = Depends(get_db)) -> Centre_de_congres:
    db_centre_de_congres = database.query(Centre_de_congres).filter(Centre_de_congres.id == centre_de_congres_id).first()
    if db_centre_de_congres is None:
        raise HTTPException(status_code=404, detail="Centre_de_congres not found")

    response_data = {
        "centre_de_congres": db_centre_de_congres,
}
    return response_data



@app.post("/centre_de_congres/", response_model=None, tags=["Centre_de_congres"])
async def create_centre_de_congres(centre_de_congres_data: Centre_de_congresCreate, database: Session = Depends(get_db)) -> Centre_de_congres:

    if centre_de_congres_data.etre_reserver is not None:
        db_etre_reserver = database.query(gestionaire).filter(gestionaire.id == centre_de_congres_data.etre_reserver).first()
        if not db_etre_reserver:
            raise HTTPException(status_code=400, detail="gestionaire not found")
    else:
        raise HTTPException(status_code=400, detail="gestionaire ID is required")

    db_centre_de_congres = Centre_de_congres(
        nomC=centre_de_congres_data.nomC,        etre_reserver_id=centre_de_congres_data.etre_reserver        )

    database.add(db_centre_de_congres)
    database.commit()
    database.refresh(db_centre_de_congres)




    return db_centre_de_congres


@app.post("/centre_de_congres/bulk/", response_model=None, tags=["Centre_de_congres"])
async def bulk_create_centre_de_congres(items: list[Centre_de_congresCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Centre_de_congres entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.etre_reserver:
                raise ValueError("gestionaire ID is required")

            db_centre_de_congres = Centre_de_congres(
                nomC=item_data.nomC,                etre_reserver_id=item_data.etre_reserver            )
            database.add(db_centre_de_congres)
            database.flush()  # Get ID without committing
            created_items.append(db_centre_de_congres.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Centre_de_congres entities"
    }


@app.delete("/centre_de_congres/bulk/", response_model=None, tags=["Centre_de_congres"])
async def bulk_delete_centre_de_congres(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Centre_de_congres entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_centre_de_congres = database.query(Centre_de_congres).filter(Centre_de_congres.id == item_id).first()
        if db_centre_de_congres:
            database.delete(db_centre_de_congres)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Centre_de_congres entities"
    }

@app.put("/centre_de_congres/{centre_de_congres_id}/", response_model=None, tags=["Centre_de_congres"])
async def update_centre_de_congres(centre_de_congres_id: int, centre_de_congres_data: Centre_de_congresCreate, database: Session = Depends(get_db)) -> Centre_de_congres:
    db_centre_de_congres = database.query(Centre_de_congres).filter(Centre_de_congres.id == centre_de_congres_id).first()
    if db_centre_de_congres is None:
        raise HTTPException(status_code=404, detail="Centre_de_congres not found")

    setattr(db_centre_de_congres, 'nomC', centre_de_congres_data.nomC)
    if centre_de_congres_data.etre_reserver is not None:
        db_etre_reserver = database.query(gestionaire).filter(gestionaire.id == centre_de_congres_data.etre_reserver).first()
        if not db_etre_reserver:
            raise HTTPException(status_code=400, detail="gestionaire not found")
        setattr(db_centre_de_congres, 'etre_reserver_id', centre_de_congres_data.etre_reserver)
    database.commit()
    database.refresh(db_centre_de_congres)

    return db_centre_de_congres


@app.delete("/centre_de_congres/{centre_de_congres_id}/", response_model=None, tags=["Centre_de_congres"])
async def delete_centre_de_congres(centre_de_congres_id: int, database: Session = Depends(get_db)):
    db_centre_de_congres = database.query(Centre_de_congres).filter(Centre_de_congres.id == centre_de_congres_id).first()
    if db_centre_de_congres is None:
        raise HTTPException(status_code=404, detail="Centre_de_congres not found")
    database.delete(db_centre_de_congres)
    database.commit()
    return db_centre_de_congres







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



