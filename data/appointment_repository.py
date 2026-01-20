# Allow type hints to refer to things not defined yet.
from __future__ import annotations
# Standard library module for interacting with SQLite databases.
import sqlite3
# Provides list/optional annotations and protocol for defining typed interfaces.
from typing import List, Optional, Protocol
# Import Models.
from models.appointment import Appointment


class AppointmentRepositoryProtocol(Protocol):
    """Outlines what a Appointment repository must implement.""" 

    def add(self, appointment: Appointment) -> Appointment: ...
    def get_all(self) -> List[Appointment]: ...
    def get_by_id(self, appointment_id: str) -> Optional[Appointment]: ...
    def update(self, appointment: Appointment) -> Appointment: ...
    def delete(self, appointment_id: str) -> None: ...



class AppointmentRepository(AppointmentRepositoryProtocol):
    """SQLite-backed repository for Appointment objects."""

    def __init__(self, db: sqlite3.Connection):
        self.db =db
        self._create_table()

    def _create_table(self):
        """
        Ensures the Appointment table exists; runs only during database setup.
        """

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                location TEXT,
                notes TEXT
            )
            """
        )
        self.db.commit()

    def add(self, appointment: Appointment) -> Appointment:
        """
        Insert the given Appointment into storage.
        Returns the fully populated Appointment(Incuding any repo assigned fields)
        """
        cursor = self.db.execute(
            """
            INSERT INTO appointments (title, date, time, location, notes)
            VALUES (?, ?, ?, ?, ?)
            """,

            (appointment.title, 
             appointment.date, 
             appointment.time, 
             appointment.location,
             appointment.notes)
        )
        self.db.commit()

        # Return a new appointment instance with the generated ID.
        return Appointment(
            id=str(cursor.lastrowid),
            title=appointment.title,
            date=appointment.date,
            time=appointment.time,
            location=appointment.location,
            notes=appointment.notes,
        )
    
    def get_all(self) -> List[Appointment]:
        """Return every Appointment stored in the repository."""

        cursor = self.db.execute(
            "SELECT id, title,  date, time, location, notes FROM appointments ORDER BY date, time"
        )
        rows = cursor.fetchall()

        return [
            Appointment(
                id=row[0],
                title=row[1],
                date=row[2],
                time=row[3],
                location=row[4] or "",
                notes=row[5],
            )
            for row in rows
        ]
    
    def get_by_id(self, appointment_id: str) -> Appointment | None:
        """
        Look up a single Appointment by its unique ID. 
        Returns None if not found.
        """

        cursor = self.db.execute(
            "SELECT id, title, date, time, location, notes FROM appointments WHERE id = ?",
            (appointment_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None
        
        return Appointment(
            id=row[0],
            title=row[1],
            date=row[2],
            time=row[3],
            location=row[4] or "",
            notes=row[5],
        )
    
    def update(self, appointment: Appointment) -> Appointment:
        """
        Overwrite the stored Appointment with the new state.
        Assume the Appointment already exists: Callers handle missing IDS.
        """

        cursor = self.db.execute(
            """
            UPDATE appointments
            SET title = ?, date = ?, time = ?, location = ?, notes = ?
            WHERE id = ?
            """,
            (
                appointment.title,
                appointment.date,
                appointment.time,
                appointment.location,
                appointment.notes,
                appointment.id,
            )
        )
        self.db.commit()
        return appointment
    
    def delete(self, appointment_id: str) -> None:
        """Delete the Appointment by the given ID."""
        
        self.db.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        self.db.commit()