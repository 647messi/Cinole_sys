from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(
    prefix="/system/dev-test",
    tags=["System - Dev Test"],
)


@router.get("/db")
def test_database_connection(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT current_database();"))
    database_name = result.scalar()

    return {
        "status": "ok",
        "database": database_name,
    }


@router.post("/db-write")
def test_database_write(db: Session = Depends(get_db)):
    db.execute(
        text("""
            CREATE TABLE IF NOT EXISTS dev_test_logs (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    )

    db.execute(
        text("""
            INSERT INTO dev_test_logs (message)
            VALUES (:message);
        """),
        {"message": "FastAPI database write test"},
    )

    db.commit()

    result = db.execute(
        text("""
            SELECT id, message, created_at
            FROM dev_test_logs
            ORDER BY id DESC
            LIMIT 1;
        """)
    )

    row = result.fetchone()

    return {
        "status": "ok",
        "inserted": {
            "id": row.id,
            "message": row.message,
            "created_at": row.created_at,
        },
    }