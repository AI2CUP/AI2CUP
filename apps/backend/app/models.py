from sqlalchemy import (
    Column, Integer, String, Boolean, Float, Text, DateTime, ForeignKey,
    create_engine, func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from app.config import get_settings

settings = get_settings()

_is_sqlite = settings.database_url.startswith("sqlite")
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if _is_sqlite else {},
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    listings = relationship("Listing", back_populates="owner")


class Listing(Base):
    """A coffee listing posted by a supplier or exporter."""
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # Coffee details
    region = Column(String, nullable=False)
    ecx_grade = Column(Integer, nullable=False)
    variety = Column(String, nullable=True)
    processing = Column(String, nullable=True)

    # Pricing & volume
    price_per_kg_etb = Column(Float, nullable=False)
    price_per_kg_usd = Column(Float, nullable=False)
    available_kg = Column(Integer, nullable=False)

    # Certification (comma-separated)
    certification = Column(String, nullable=True, default="")

    # Contact info (shown publicly)
    contact_name = Column(String, nullable=False)
    contact_phone = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="listings")


def init_db():
    Base.metadata.create_all(bind=engine)
