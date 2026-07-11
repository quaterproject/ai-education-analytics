from app.core.database import get_db

# Re-export database session dependency
__all__ = ["get_db"]
