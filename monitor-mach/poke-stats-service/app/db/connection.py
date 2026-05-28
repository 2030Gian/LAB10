import sqlite3
from pathlib import Path
from app.core.config import settings


def get_connection() -> sqlite3.Connection:
    db_path = Path(settings.DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row

    return connection