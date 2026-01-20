# Access to SQLite database and its functions.
import sqlite3
# Object for working with files and folder paths.
from pathlib import Path
# Import Data.
from data.appointment_repository import AppointmentRepository
from data.medication_repository import MedicationRepository
from data.schedule_repository import ScheduleRepository
from data.reminder_repository import ReminderRepository
from data.intake_log_repository import IntakeLogRepository
from data.user_profile_repository import UserProfileRepository


# Path to the SQLite database file (stored inside the data folder)
DB_PATH = Path(__file__).parent / "app.db"


def get_connection():
    """
    Returns a SQLITE connection with foreign keys enabled.
    All repositories will use this function.
    """

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Enables dict-like row access
    conn.execute("PRAGMA foreign_keys = ON;")  # Enforce FK constraints
    return conn


class Database:
    """A wrapper around SQLite providing simple, safe database access."""

    def __init__(self):

        # Obtain the shared DB connection used by all repositories
        self.conn = get_connection()

        # Pass the same connection to all repositories.
        # This is the order of dependency.
        self.schedules = ScheduleRepository(self.conn)
        self.medications = MedicationRepository(self.conn, self.schedules)
        self.appointments = AppointmentRepository(self.conn)
        self.reminders = ReminderRepository(self.conn)
        self.intake_logs = IntakeLogRepository(self.conn)
        self.user_profile = UserProfileRepository(self.conn)
        