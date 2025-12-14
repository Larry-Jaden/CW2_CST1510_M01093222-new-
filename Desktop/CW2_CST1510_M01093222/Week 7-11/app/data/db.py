
import sqlite3
from pathlib import Path

# Default data directory and DB path (anchored to project root)
# Use the repository/workspace layout so the DB and CSVs are found
# regardless of the current working directory when the app is run.
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "DATA"
DB_PATH = DATA_DIR / "intelligence_platform.db"


def _ensure_db_dir(db_path: Path):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)


def connect_database(db_path=None):
    """Connect to the SQLite database. Creates parent dir if needed.

    Args:
        db_path: Path or string to database file. If None, uses default `DB_PATH`.

    Returns:
        sqlite3.Connection
    """
    if db_path is None:
        db_path = DB_PATH
    db_path = Path(db_path)
    _ensure_db_dir(db_path)
    return sqlite3.connect(str(db_path))

