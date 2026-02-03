from fastapi import APIRouter, status, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.session import SessionLocal

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Service health check",
    description="Verifies application liveness and database connectivity"
)
def health_check():
    """
    Health check endpoint used for monitoring, load balancers,
    and container orchestration platforms.
    """
    db = None
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "service": "todo-api",
            "database": "up"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable"
        )

    finally:
        if db:
            db.close()
