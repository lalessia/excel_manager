import sqlite3
import os
import sys
from typing import Optional

# --------------------------------------------------
# Percorso DB compatibile con PyInstaller
# --------------------------------------------------
def get_db_path() -> str:
    """
    Restituisce il percorso del database.
    - In dev: core/db/app.db
    - In exe: cartella accanto all'eseguibile
    """
    if hasattr(sys, "_MEIPASS"):
        # exe → DB esterno e persistente
        base_dir = os.path.dirname(sys.executable)
    else:
        # sviluppo
        base_dir = os.path.join(os.path.dirname(__file__), "..", "db")

    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, "app.db")


DB_PATH = get_db_path()


def get_connection():
    """Apre una connessione SQLite"""
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# Init DB
# --------------------------------------------------
def init_db():
    """
    Crea il database e la tabella extras se non esistono.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            prezzo REAL NOT NULL CHECK (prezzo >= 0)
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# CRUD
# --------------------------------------------------
def get_all_extras():
    """
    Ritorna tutti gli extra ordinati per nome.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome, prezzo FROM extras ORDER BY nome"
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def insert_extra(nome: str, prezzo: float) -> int | None:
    """
    Inserisce un extra e ritorna l'ID generato.
    Se il nome esiste già, ritorna None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO extras (nome, prezzo) VALUES (?, ?)",
            (nome, prezzo)
        )
        conn.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()

def update_extra(extra_id: int, nome: str, prezzo: float) -> Optional[bool]:
    """
    Aggiorna un extra esistente.
    Ritorna:
    - True  → aggiornato
    - False → ID non trovato
    - None  → nome duplicato
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE extras SET nome = ?, prezzo = ? WHERE id = ?",
            (nome, prezzo, extra_id)
        )
        conn.commit()
        return cursor.rowcount > 0

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()


def delete_extra(extra_id: int) -> bool:
    """
    Elimina un extra tramite ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM extras WHERE id = ?",
        (extra_id,)
    )

    conn.commit()
    success = cursor.rowcount > 0
    conn.close()

    return success
