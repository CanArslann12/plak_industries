import sqlite3
from pathlib import Path

from flask import current_app, g


_SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT NOT NULL,
    telefon TEXT NOT NULL,
    mesaj TEXT,
    tarih TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


def _database_path():
    database_url = current_app.config["DATABASE_URL"]
    if not database_url.startswith("sqlite:///"):
        raise ValueError("DATABASE_URL yalnızca SQLite desteklemelidir.")
    return database_url.removeprefix("sqlite:///")


def get_db():
    if "db" not in g:
        database_path = _database_path()
        if database_path == ":memory:" and "db_memory" in current_app.extensions:
            g.db = current_app.extensions["db_memory"]
            return g.db
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
        if database_path == ":memory:":
            current_app.extensions["db_memory"] = g.db
    return g.db


def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None and current_app.config["DATABASE_URL"] != "sqlite:///:memory:":
        database.close()


def init_db(app):
    with app.app_context():
        database = get_db()
        database.execute(_SCHEMA)
        database.commit()
    app.teardown_appcontext(close_db)


def lead_ekle(isim, telefon, mesaj=""):
    database = get_db()
    try:
        cursor = database.execute(
            "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
            (isim, telefon, mesaj),
        )
        database.commit()
        return cursor.lastrowid
    except sqlite3.Error:
        database.rollback()
        raise


def tum_leadler():
    rows = get_db().execute(
        "SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY tarih DESC, id DESC"
    ).fetchall()
    return [dict(row) for row in rows]
