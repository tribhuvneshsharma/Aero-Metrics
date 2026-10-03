import os
import csv
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, RouteWeightModel, LeadTimeWeightModel

# Read DATABASE_URL or fallback to local SQLite for zero-config standalone execution
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./apix.db")

# SQLite needs check_same_thread=False
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db(db: Session = None):
    """
    Initialise all database tables and seed reference routes & weights from CSV if empty.
    """
    Base.metadata.create_all(bind=engine)
    
    close_after = False
    if db is None:
        db = SessionLocal()
        close_after = True
        
    try:
        # 1. Seed Route Weights if empty
        if db.query(RouteWeightModel).count() == 0:
            csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "reference", "route_basket.csv")
            if os.path.exists(csv_path):
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        eff_from = date.fromisoformat(row["effective_from"]) if row.get("effective_from") else date(2026, 1, 1)
                        eff_to = date.fromisoformat(row["effective_to"]) if row.get("effective_to") else None
                        rw = RouteWeightModel(
                            route_code=row["route_code"],
                            origin=row["origin"],
                            destination=row["destination"],
                            weight=float(row["weight"]),
                            effective_from=eff_from,
                            effective_to=eff_to,
                            weight_source=row.get("weight_source", "DGCA traffic proxy")
                        )
                        db.add(rw)
                db.commit()

        # 2. Seed Lead Time Weights if empty
        if db.query(LeadTimeWeightModel).count() == 0:
            csv_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "reference", "lead_time_weights.csv")
            if os.path.exists(csv_path):
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        lw = LeadTimeWeightModel(
                            horizon=row["horizon"],
                            lead_time_days=int(row["lead_time_days"]),
                            weight=float(row["weight"]),
                            description=row.get("description", "")
                        )
                        db.add(lw)
                db.commit()
    finally:
        if close_after:
            db.close()
