"""SQLite storage helpers seeded from CSV data."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "intern_energy_station.db"

TABLE_FILES = {
    "interns": "interns.csv",
    "mentors": "mentors.csv",
    "weekly_tasks": "weekly_tasks.csv",
    "intern_progress": "intern_progress.csv",
    "mentor_feedback": "mentor_feedback.csv",
    "evaluation_results": "evaluation_results.csv",
}


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)


def read_csv_seed(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / name, encoding="utf-8-sig")


def database_exists(db_path: Path = DB_PATH) -> bool:
    return db_path.exists()


def init_database(db_path: Path = DB_PATH, *, force: bool = False) -> Path:
    """Initialize SQLite database from CSV seed files."""
    if db_path.exists() and not force:
        return db_path

    if db_path.exists() and force:
        db_path.unlink()

    with get_connection(db_path) as conn:
        for table_name, file_name in TABLE_FILES.items():
            df = read_csv_seed(file_name)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mentor_feedback_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                intern_id TEXT NOT NULL,
                mentor_id TEXT NOT NULL,
                week INTEGER NOT NULL,
                feedback_text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
    return db_path


def load_table(table_name: str, db_path: Path = DB_PATH) -> pd.DataFrame:
    init_database(db_path)
    with get_connection(db_path) as conn:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)


def load_all_tables(db_path: Path = DB_PATH) -> dict[str, pd.DataFrame]:
    init_database(db_path)
    return {table_name: load_table(table_name, db_path) for table_name in TABLE_FILES}


def save_mentor_feedback(
    intern_id: str,
    mentor_id: str,
    week: int,
    feedback_text: str,
    db_path: Path = DB_PATH,
) -> None:
    """Persist latest mentor feedback and append history."""
    init_database(db_path)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection(db_path) as conn:
        conn.execute(
            """
            UPDATE mentor_feedback
            SET feedback_text = ?, created_at = ?
            WHERE intern_id = ?
            """,
            (feedback_text, created_at, intern_id),
        )
        if conn.total_changes == 0:
            feedback_id = f"F{intern_id.replace('I', '')}"
            conn.execute(
                """
                INSERT INTO mentor_feedback (
                    feedback_id, intern_id, mentor_id, week, feedback_text,
                    professional_score, communication_score, initiative_score, created_at
                )
                VALUES (?, ?, ?, ?, ?, 70, 70, 70, ?)
                """,
                (feedback_id, intern_id, mentor_id, week, feedback_text, created_at),
            )
        conn.execute(
            """
            INSERT INTO mentor_feedback_history (intern_id, mentor_id, week, feedback_text, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (intern_id, mentor_id, week, feedback_text, created_at),
        )


def load_feedback_history(intern_id: str, db_path: Path = DB_PATH) -> pd.DataFrame:
    init_database(db_path)
    with get_connection(db_path) as conn:
        return pd.read_sql_query(
            """
            SELECT intern_id, mentor_id, week, feedback_text, created_at
            FROM mentor_feedback_history
            WHERE intern_id = ?
            ORDER BY created_at DESC
            """,
            conn,
            params=(intern_id,),
        )
