from __future__ import annotations

# Used for storing and formatting timestamps.
from datetime import datetime
from typing import List, Protocol
# Import Models.
from models.intake_log import IntakeLog
# Import Validators.
from validators.intake_log_validator import IntakeLogValidator
# Import Data.
from data.errors import DatabaseError, NotFoundError

class IntakeLogRepositoryProtocol(Protocol): 
    """Outlines what a Intake log repository must implement."""  

    def add(self, log: IntakeLog) -> IntakeLog: ... 
    def update(self, log: IntakeLog) -> IntakeLog: ... 
    def delete(self, log_id: str) -> None: ... 
    def get_by_id(self, log_id: str) -> IntakeLog: ... 
    def get_all(self) -> List[IntakeLog]: ... 
    def get_by_medication(self, medication_id: str) -> List[IntakeLog]: ...


class IntakeLogRepository(IntakeLogRepositoryProtocol):
    """SQLite-backed repository for Intake Log objects."""

    def __init__(self, connection) -> None:
        self.connection = connection
        self._create_table()

    def _create_table(self) -> None:
        """
        Ensures the Intake log table exists; runs only during database setup.
        """
        cursor = self.connection.cursor()
        cursor.execute(
            """       
            CREATE TABLE IF NOT EXISTS intake_logs (
                id TEXT PRIMARY KEY,
                medication_id TEXT NOT NULL,
                scheduled_time TEXT,
                taken_time TEXT,
                amount_taken REAL NOT NULL,
                notes TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (medication_id) REFERENCES medication(id) ON DELETE CASCADE
            );
            """
        )
        self.connection.commit()


    def add(self, log: IntakeLog) -> IntakeLog:
        """
        Stores this Intake log in the database and gives back the saved version.
        """
        
        # Validate before writing to the database.
        IntakeLogValidator.validate(log)

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO intake_logs (
                id, medication_id, scheduled_time, taken_time,
                amount_taken, notes, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, 
            (
                log.id,
                log.medication_id,
                log.scheduled_time.isoformat() if log.scheduled_time else None,
                log.taken_time.isoformat(),
                log.amount_taken,
                log.notes,
                log.created_at.isoformat(),
            ),
        )
        
        conn.commit()
        return log

    def update(self, log: IntakeLog) -> IntakeLog:
        """
        Overwrite the stored intake log with the new state.
        Assume the Intake log already exists.
        """

        # Validate before updating.
        IntakeLogValidator.validate(log)

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE intake_logs
            SET medication_id = ?, scheduled_time = ?, taken_time = ?,
                amount_taken = ?, notes = ?
            WHERE id = ?
        """, (
            log.medication_id,
            log.scheduled_time.isoformat() if log.scheduled_time else None,
            log.taken_time.isoformat(),
            log.amount_taken,
            log.notes,
            log.id,
        ))

        conn.commit()
        return log

    def delete(self, log_id: str) -> None:
        """Delete the Intake log by the given ID."""

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute("DELETE FROM intake_logs WHERE id = ?", (log_id,))
        conn.commit()

    def get_by_id(self, log_id: str) -> IntakeLog:
        """Look up a single Intake log by its unique ID."""

        conn = self.connection
        cursor = conn.cursor()

        try:

            cursor.execute("SELECT * FROM intake_logs WHERE id = ?", (log_id,))
            row = cursor.fetchone()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch intake log: {e}")

        if row is None:
            raise NotFoundError(f"Intake log with id {log_id} not found.")
        
        log = self._row_to_intake_log(row)
        IntakeLogValidator.validate(log)
        return log
    

    def get_all(self) -> List[IntakeLog]:
        """Return every Intake log stored in the repository."""

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM intake_logs")
        rows = cursor.fetchall()
        

        return [self._row_to_intake_log(r) for r in rows]

    def get_by_medication(self, medication_id: str) -> List[IntakeLog]:
        """Fetch every Intake log recorded for the given medication."""

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM intake_logs WHERE medication_id = ?", 
            (medication_id,)
        )
        rows = cursor.fetchall()
        
        return [self._row_to_intake_log(r) for r in rows]

    def _row_to_intake_log(self, row) -> IntakeLog:
        """Convert a SQLite row into an Intake log model."""

        log = IntakeLog(
            id=row["id"],
            medication_id=row["medication_id"],
            scheduled_time=datetime.fromisoformat(row["scheduled_time"]) 
            if row["scheduled_time"] 
            else None,
            taken_time=datetime.fromisoformat(row["taken_time"]),
            amount_taken=row["amount_taken"],
            notes=row["notes"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

        # Validate DB row after conversion (defensive programming).
        IntakeLogValidator.validate(log)
        return log