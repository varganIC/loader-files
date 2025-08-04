from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    settings.get_sync_database_url()
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# def get_db() -> SessionLocal:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
