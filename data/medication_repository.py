from __future__ import annotations
from typing import List, Protocol
from datetime import datetime
# Import Models.
from models.medication import Medication
from models.schedule import Schedule
# Import Data.
from data.schedule_repository import ScheduleRepositoryProtocol
from data.errors import DatabaseError, NotFoundError
# Import Validators.
from validators.medication_validator import MedicationValidator

class MedicationRepositoryProtocol(Protocol): 
    """Outlines what a Medication repository must implement.""" 

    def add(self, medication: Medication) -> Medication: ... 
    def get_all(self) -> List[Medication]: ... 
    def get_by_id(self, medication_id: str) -> Medication: ... 
    def update(self, medication: Medication) -> Medication: ... 
    def delete(self, medication_id: str) -> None: ...


class MedicationRepository(MedicationRepositoryProtocol):
    """SQLite-backed repository for Medication objects."""

    def __init__(self, connection, schedule_repo: ScheduleRepositoryProtocol):

        self.connection = connection
        self.schedule_repo = schedule_repo
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
                CREATE TABLE IF NOT EXISTS medications (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    dosage TEXT,
                    notes TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL
                );
                """
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to create medications table: {e}")

    def add(self, medication: Medication) -> Medication:
        """Validate and insert a new medication into the database."""
        MedicationValidator.validate(medication)
        
        # Save schedules first.
        for sched in medication.schedule:
            self.schedule_repo.add(sched)

        conn = self.connection
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO medications (id, name, description, dosage, notes, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, 
                (
                    medication.id,
                    medication.name,
                    medication.description,
                    medication.dosage,
                    medication.notes,
                    1 if medication.is_active else 0,
                    medication.created_at.isoformat(),
                ),
            )
            conn.commit()
        except Exception as e:
            raise DatabaseError(f"Failed to insert medication: {e}")

        return medication

    def get_all(self) -> List[Medication]:
        """Return all medications from the database."""

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM medications")
        rows = cursor.fetchall()


        meds =  [self._row_to_medication(row) for row in rows]

        return meds

    def get_by_id(self, medication_id: str) -> Medication:
        """
        Return a single medication by ID, or raise NotFoundError if not found.
        """
        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM medications WHERE id = ?", (medication_id,))
            row = cursor.fetchone()
        except Exception as e:
            raise DatabaseError(f"Failed to fetch medication: {e}")
        
        if row is None:
            raise NotFoundError(f"medication with id {medication_id} not found")
        
        med = self._row_to_medication(row)
        MedicationValidator.validate(med)
        return med

    def update(self, medication: Medication) -> Medication:

        """Validate and update an existing medication."""
        MedicationValidator.validate(medication)

        conn = self.connection
        cursor = conn.cursor()

        # Replace schedules.
        if medication.schedule:
            self.schedule_repo.delete_by_medication(medication.id)
            for sched in medication.schedule:
                self.schedule_repo.add(sched)

        cursor.execute(
            """
            UPDATE medications
            SET name = ?, description = ?, dosage = ?, notes = ?, is_active = ?
            WHERE id = ?
            """, 
            (
                medication.name,
                medication.description,
                medication.dosage,
                medication.notes or "",
                1 if medication.is_active else 0,
                medication.id,
            ),
        )
        conn.commit()
        return medication

    def delete(self, medication_id: str) -> None:
        """Delete a medication by ID."""

        conn = self.connection
        cursor = conn.cursor()

        cursor.execute("DELETE FROM medications WHERE id = ?", (medication_id,))
        conn.commit()
        

    # Internal helper methods.
    def _row_to_medication(self, row) -> Medication:
        """Convert a SQLite row into a Medication dataclass."""

        med = Medication(
            id=row["id"],
            name=row["name"],
            description=row["description"] or "",
            dosage=row["dosage"] or "",
            notes=row["notes"] or "",
            is_active=bool(row["is_active"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            schedule=self._load_schedule(row["id"]),
        )

        # Validate Database row.
        MedicationValidator.validate(med)
        return med

    def _load_schedule(self, medication_id: str) -> List[Schedule]:
        """
        Query storage for all Schedule objects 
        associated with a given medication.
        """
        # Delegate to the schedule repository to load all related Schedule objects
        return self.schedule_repo.get_by_medication(medication_id)

       

        