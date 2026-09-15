import sqlite3
from pathlib import Path

DB_PATH = Path("naqclinixai.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                sex TEXT,
                phone TEXT,
                clinical_notes TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                visit_date TEXT,
                visit_type TEXT,
                chief_complaint TEXT,
                clinical_findings TEXT,
                diagnosis TEXT,
                treatment_plan TEXT,
                notes TEXT,
                created_at TEXT
            )
        """)
        conn.commit()


def add_patient(patient_id, name, age, sex, phone, clinical_notes, created_at):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO patients
               (patient_id, name, age, sex, phone, clinical_notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (patient_id, name, age, sex, phone, clinical_notes, created_at),
        )
        conn.commit()


def get_patients():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM patients ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def patient_exists(patient_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM patients WHERE patient_id = ?",
            (patient_id,),
        ).fetchone()
        return row is not None


def add_visit(patient_id, visit_date, visit_type, chief_complaint,
              clinical_findings, diagnosis, treatment_plan, notes, created_at):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO visits
               (patient_id, visit_date, visit_type, chief_complaint,
                clinical_findings, diagnosis, treatment_plan, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (patient_id, visit_date, visit_type, chief_complaint,
             clinical_findings, diagnosis, treatment_plan, notes, created_at),
        )
        conn.commit()


def get_patient_visits(patient_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM visits WHERE patient_id = ? ORDER BY visit_date DESC",
            (patient_id,),
        ).fetchall()
        return [dict(r) for r in rows]
