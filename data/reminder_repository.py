from __future__ import annotations
from typing import List, Protocol
# Import Models
from models.reminder import Reminder
# Import Validators.
from validators.reminder_validator import ReminderValidator
# Import Data.
from data.errors import DatabaseError, NotFoundError

class ReminderRepositoryProtocol(Protocol): 
    """Outlines what a Reminder repository must implement.""" 

    def add(self, reminder: Reminder) -> Reminder: ... 
    def update(self, reminder: Reminder) -> Reminder: ... 
    def delete(self, reminder_id: str) -> None: ... 
    def get_by_id(self, reminder_id: str) -> Reminder: ... 
    def get_all(self) -> List[Reminder]: ... 
    def get_by_schedule(self, schedule_id: str) -> List[Reminder]: ... 
    def get_by_medication(self, medication_id: str) -> List[Reminder]: ...



class ReminderRepository(ReminderRepositoryProtocol):
    """SQLite-backed repository for Reminder settings."""

    def __init__(self, connection):
        self.connection = connection
        self._create_table()

    def _create_table(self) -> None:
        """
        Ensures the required table structure is 
        in place during database setup.
        """
        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS reminders (
                    id TEXT PRIMARY KEY,
                    medication_id TEXT NOT NULL,
                    schedule_id TEXT NOT NULL,
                    enabled INTEGER NOT NULL,
                    reminder_offset_minutes INTEGER NOT NULL,
                    FOREIGN KEY (medication_id)
                        REFERENCES medications(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (schedule_id)
                        REFERENCES schedules(id)
                        ON DELETE CASCADE
                );
                """
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to create reminders table: {e}")
        
    # CRUD operations.

    def add(self, reminder: Reminder) -> Reminder:
        """Save a new reminder and return the stored version."""

        # Run validation rules before saving the reminder.
        ReminderValidator.validate(reminder)

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO reminders (
                    id, medication_id, schedule_id,
                    enabled, reminder_offset_minutes
                )
                VALUES (?, ?, ?, ?, ?)
                """, 
                (
                    reminder.id,
                    reminder.medication_id,
                    reminder.scheduled_id,
                    1 if reminder.enabled else 0,
                    reminder.reminder_offset_minutes,
                ),
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to insert reminder: {e}")
        
        return reminder

    def update(self, reminder: Reminder) -> Reminder:
        """
        Overwrite the stored Reminder with the new state.
        Assume the Reminder already exists.
        """

        # Run validation rules before saving the reminder.
        ReminderValidator.validate(reminder)

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE reminders
                SET medication_id = ?,
                    schedule_id = ?,
                    enabled = ?,
                    reminder_offset_minutes = ?
                WHERE id = ?
                """, 
                (
                    reminder.medication_id,
                    reminder.scheduled_id,
                    1 if reminder.enabled else 0,
                    reminder.reminder_offset_minutes,
                    reminder.id,
                ),
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to update reminder: {e}")
        

        return reminder

    def delete(self, reminder_id: str) -> None:
        """Delete a reminder from the database."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to delete reminder: {e}")
        

    def get_by_id(self, reminder_id: str) -> Reminder:
        """fetch a reminder from the database."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM reminders WHERE id = ?", (reminder_id,))
            row = cursor.fetchone()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch reminder: {e}")
        
        if row is None:
            raise NotFoundError(f"Reminder with id {reminder_id} not found")

        reminder = self._row_to_reminder(row)
        ReminderValidator.validate(reminder)
        return reminder

    def get_all(self) -> List[Reminder]:
        """Return a list of all reminders."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM reminders")
            rows = cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch reminders: {e}")
        

        return [self._row_to_reminder(r) for r in rows]

    def get_by_schedule(self, schedule_id: str) -> List[Reminder]:
        """Return a list of reminders by schedule."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM reminders
                WHERE schedule_id = ?
                """, 
                (schedule_id,)
            )
            rows = cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch reminders for schedule {schedule_id}: {e}")
        
        return [self._row_to_reminder(r) for r in rows]

    def get_by_medication(self, medication_id: str) -> List[Reminder]:
        """Return a list of reminders by medication."""

        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT * FROM reminders
                WHERE medication_id = ?
                """, 
                (medication_id,)
            )
            rows = cursor.fetchall()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch reminders for medication {medication_id}: {e}")
    
        return [self._row_to_reminder(r) for r in rows]

    # Internal helper methods.
    def _row_to_reminder(self, row) -> Reminder:
        """Returns a row of reminder information."""

        reminder = Reminder(
            id=row["id"],
            medication_id=row["medication_id"],
            scheduled_id=row["schedule_id"],
            enabled=bool(row["enabled"]),
            reminder_offset_minutes=row["reminder_offset_minutes"],
        )
        
        # Run validation rules before saving the reminder.
        ReminderValidator.validate(reminder)
        return reminder
