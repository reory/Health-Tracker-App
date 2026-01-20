from __future__ import annotations 

# Handles serializing and loading data in JSON format.
import json
from typing import List, Protocol
from datetime import datetime
# Import Models.
from models.schedule import Schedule
# Import Validators.
from validators.schedule_validator import ScheduleValidator
# Import Data.
from data.errors import DatabaseError, NotFoundError

class ScheduleRepositoryProtocol(Protocol): 
    """Outlines what a Schedule repository must implement.""" 

    def add(self, schedule: Schedule) -> Schedule: ... 
    def get_all(self) -> List[Schedule]: ...
    def get_by_id(self, schedule_id: str) -> Schedule: ... 
    def get_by_medication(self, medication_id: str) -> List[Schedule]: ... 
    def update(self, schedule: Schedule) -> Schedule: ... 
    def delete(self, schedule_id: str) -> None: ... 
    def delete_by_medication(self, medication_id: str) -> None: ...


class ScheduleRepository(ScheduleRepositoryProtocol):
    """SQLite-backed repository for Schedule objects."""

    def __init__(self, connection):
        self.connection = connection
        self._create_table()

    def _create_table(self) -> None:
        conn = self.connection
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS schedules (
                    id TEXT PRIMARY KEY,
                    medication_id TEXT NOT NULL,
                    times TEXT NOT NULL,
                    days_of_week TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    start_date TEXT NOT NULL,
                    end_date TEXT,
                    is_active INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (medication_id)
                        REFERENCES medications(id)
                        ON DELETE CASCADE
                );
                """
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to create schedules table: {e}")
        
        
    # CRUD operations. (Create, Read Update and Delete operations.)
    def add(self, schedule: Schedule) -> Schedule:
        """Save a new schedule and return the stored version."""

        # Run validation rules before saving the Schedule.
        ScheduleValidator.validate(schedule)

        conn = self.connection
        cursor = conn.cursor()

        try: 
            cursor.execute(
                """
                INSERT INTO schedules (
                    id, medication_id, times, days_of_week, frequency,
                    start_date, end_date, is_active, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, 
                (
                    schedule.id,
                    schedule.medication_id,
                    json.dumps([t.strftime("%H:%M") for t in schedule.times]),
                    json.dumps(schedule.days_of_week),
                    schedule.frequency,
                    schedule.start_date.isoformat(),
                    schedule.end_date.isoformat() if schedule.end_date else None,
                    1 if schedule.is_active else 0,
                    schedule.created_at.isoformat(),
                ),
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to insert schedule: {e}")
        
        return schedule

    def get_all(self) -> List[Schedule]:
        """Return a list of all schedules."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM schedules")
            rows = cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch schedules: {e}")
        
        return [self._row_to_schedule(row) for row in rows]

    def get_by_id(self, schedule_id: str) -> Schedule:
        """Fetch a schedule from the database."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM schedules WHERE id = ?", (schedule_id,))
            row = cursor.fetchone()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch schedule: {e}")
        
        if row is None:
            raise NotFoundError(f"Schedule with id {schedule_id} not found")
        
        schedule = self._row_to_schedule(row)
        ScheduleValidator.validate(schedule)
        return schedule

    def get_by_medication(self, medication_id: str) -> List[Schedule]:
        """Return all schedules associated with a medication."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM schedules WHERE medication_id = ?", 
                           (medication_id,))
            rows = cursor.fetchall()
        except Exception as e:
            raise DatabaseError(
                f"Failed to fetch schedules for medication {medication_id}: {e}"
            )
        
        return [self._row_to_schedule(row) for row in rows]

    def update(self, schedule: Schedule) -> Schedule:
        """
        Overwrite the stored Schedule with the new state.
        Assume the Schedule already exists.
        """

        # Run validation rules before saving the Schedule.
        ScheduleValidator.validate(schedule)

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE schedules
                SET times = ?,
                    frequency = ?, 
                    days_of_week = ?, 
                    start_date = ?, 
                    end_date = ?, 
                    is_active = ?
                WHERE id = ?;
                """, 
                (
                    json.dumps([t.strftime("%H:%M") for t in schedule.times]),
                    schedule.frequency,
                    json.dumps(schedule.days_of_week),
                    schedule.start_date.isoformat(),
                    schedule.end_date.isoformat() if schedule.end_date else None,
                    1 if schedule.is_active else 0,
                    schedule.id,
                ),
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to update schedule: {e}")
        
        return schedule

    def delete(self, schedule_id: str) -> None:
        """Delete a schedule from the database."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM schedules WHERE id = ?;", (schedule_id,))
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to delete schedule: {e}")
        
    def delete_by_medication(self, medication_id: str) -> None:
        """Delete every entry associated with the given ID"""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                "DELETE FROM schedules WHERE medication_id = ?",
                (medication_id,),
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(
                f"Failed to delete schedules for medication {medication_id}: {e}"
            )
        
    # Internal helpers.
    def _row_to_schedule(self, row) -> Schedule:
        """Build a Schedule object from the row returned by the query."""

        # Make app better to identify malformed data - 
        # such as data with missing rows, corrupted DB rows, etc.
        raw_times =json.loads(row["times"]) or []
        times = [datetime.strptime(t, "%H:%M").time() for t in raw_times]
        days = json.loads(row["days_of_week"]) or []

        schedule = Schedule(
            id=row["id"],
            medication_id=str(row["medication_id"]),
            times=times,
            frequency=row["frequency"],
            days_of_week=days,
            start_date=datetime.fromisoformat(row["start_date"]).date(),
            end_date=datetime.fromisoformat(row["end_date"]).date() 
            if row["end_date"] 
            else None,
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
        )

        # Run validation rules before saving the Schedule.
        ScheduleValidator.validate(schedule)
        return schedule