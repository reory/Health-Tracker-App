from datetime import datetime, timezone
# Import Models.
from models.medication import Medication

# A dedicated exception type for medication validation failures.
# This allows the UI or repository to catch medication-specific
# issues and handle them cleanly.
class MedicationValidationError(Exception):
    """Custom exception for medication validation errors."""
    pass


class MedicationValidator:
    """Validates Medication objects before saving or updating."""

    @staticmethod
    def validate(med: Medication):
        """Ensure the medication is complete and checks all the required rules."""

        # Ensures the medication has a name.
        MedicationValidator._validate_name(med)
        # Confirm dosage information is present and valid.
        MedicationValidator._validate_dosage(med)
        # Validate notes (optional) ensuring they are a string.
        MedicationValidator._validate_notes(med)
        # Verify the medication id is valid. usually auto generated.
        MedicationValidator._validate_id(med)
        # Ensures created_at is a proper datetime and not set in the future.
        MedicationValidator._validate_created_at(med)

    @staticmethod
    def _validate_name(med: Medication):
        """Ensure the medication has a valid name."""

        # Medication name must be present and meaningful.
        if not med.name or not med.name.strip():
            raise MedicationValidationError("Medication name cannot be empty.")

        # Optional: enforce a reasonable length limit.
        if len(med.name) > 100:
            raise MedicationValidationError("Medication name is too long.")

    @staticmethod
    def _validate_dosage(med: Medication):
        """Ensure the dosage values is present and acceptable."""

        # Dosage must be provided (e.g., '10mg', '2 tablets').
        if not med.dosage or not med.dosage.strip():#type:ignore
            raise MedicationValidationError("Dosage cannot be empty.")

        # Optional: enforce a reasonable length limit.
        if len(med.dosage) > 50: #type:ignore
            raise MedicationValidationError("Dosage text is too long.")

    @staticmethod
    def _validate_notes(med: Medication):
        """Check that the notes provided are acceptable and valid."""

        # Notes are optional, but if provided, they must be a string.
        if med.notes is not None and not isinstance(med.notes, str):
            raise MedicationValidationError("Notes must be a string.")

        # Optional: enforce a reasonable length limit.
        if med.notes and len(med.notes) > 500: #type:ignore
            raise MedicationValidationError("Notes are too long.")

    @staticmethod
    def _validate_id(med: Medication):
        """Ensure that the medication has a valid and acceptable ID."""

        # ID should always be a non-empty string (usually auto-generated).
        if not med.id or not isinstance(med.id, str):
            raise MedicationValidationError("Medication ID must be a valid string.")

    @staticmethod
    def _validate_created_at(med: Medication):
        """Ensure the medication has a valid creation timestamp."""

        # created_at must be a datetime object.
        if not isinstance(med.created_at, datetime):
            raise MedicationValidationError("created_at must be a datetime object.")

        # Optional: prevent future timestamps.
        if med.created_at > datetime.now(timezone.utc):
            raise MedicationValidationError("created_at cannot be in the future.")