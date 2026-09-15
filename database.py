import sqlite3
from pathlib import Path

# ============================================================
# NAQclinixAI Local Database
# ============================================================

DATABASE_PATH = Path("naqclinixai.db")


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            phone TEXT,
            clinical_notes TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_patient(
    patient_id,
    name,
    age,
    sex,
    phone,
    clinical_notes,
    created_at
):

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO patients (
            patient_id,
            name,
            age,
            sex,
            phone,
            clinical_notes,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            patient_id,
            name,
            age,
            sex,
            phone,
            clinical_notes,
            created_at
        )
    )

    connection.commit()

    patient_database_id = cursor.lastrowid

    connection.close()

    return patient_database_id


def get_patients():

    connection = get_connection()

    patients = connection.execute(
        """
        SELECT *
        FROM patients
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return patients


def get_patient(patient_id):

    connection = get_connection()

    patient = connection.execute(
        """
        SELECT *
        FROM patients
        WHERE patient_id = ?
        """,
        (patient_id,)
    ).fetchone()

    connection.close()

    return patient


def patient_exists(patient_id):

    connection = get_connection()

    patient = connection.execute(
        """
        SELECT id
        FROM patients
        WHERE patient_id = ?
        """,
        (patient_id,)
    ).fetchone()

    connection.close()

    return patient is not None
