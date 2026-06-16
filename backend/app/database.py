from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL)

# Configure the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your data models to inherit from
Base = declarative_base()

# Request dependency to handle DB lifecycle
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
