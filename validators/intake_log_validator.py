from datetime import datetime
# Import Models.
from models.intake_log import IntakeLog

# A dedicated exception type for intake log validation failures.
# This allows the UI or repository to catch log-specific issues
# and handle them cleanly.
class IntakeLogValidationError(Exception):
    """Custom exception for intake log validation errors."""
    pass


class IntakeLogValidator:
    """Validates IntakeLog objects before saving or updating."""

    @staticmethod
    def validate(log: IntakeLog):
        """Ensure the intake log is complete and all checks pass."""

        # Ensure that the log references a valid medication ID.
        IntakeLogValidator._validate_medication_id(log)
        # Validate the scheduled time.
        IntakeLogValidator._validate_scheduled_time(log)
        # Confirm the taken_time is a valid datetime and not in the future.
        IntakeLogValidator._validate_taken_time(log)
        # Validate the amount taken of medication must be numeric.
        IntakeLogValidator._validate_amount_taken(log)
        # Validate optional notes, ensuring that they are a string.
        IntakeLogValidator._validate_notes(log)
        # Validate when the entry was created.
        IntakeLogValidator._validate_created_at(log)

    @staticmethod
    def _validate_medication_id(log: IntakeLog):
        """
        Confirm medication ID is present, 
        non-empty and structured correctly.
        """

        # medication_id must be a non-empty string.
        if not log.medication_id or not isinstance(log.medication_id, str):
            raise IntakeLogValidationError("medication_id must be a valid string.")

    @staticmethod
    def _validate_scheduled_time(log: IntakeLog):
        """
        Confirm scheduled time is present, well formed and chronologically
        sound.
        """

        # scheduled_time may be None (manual logs are allowed).
        if log.scheduled_time is None:
            return

        # If provided, it must be a datetime object.
        if not isinstance(log.scheduled_time, datetime):
            raise IntakeLogValidationError("scheduled_time must be a datetime or None.")

        # Optional: prevent future scheduled times.
        if log.scheduled_time > datetime.now():
            raise IntakeLogValidationError("scheduled_time cannot be in the future.")

    @staticmethod
    def _validate_taken_time(log: IntakeLog):
        """Ensure the intake log has a valid taken_time."""

        # taken_time must always be a datetime.
        if not isinstance(log.taken_time, datetime):
            raise IntakeLogValidationError("taken_time must be a datetime.")

        # taken_time cannot be in the future.
        if log.taken_time > datetime.now():
            raise IntakeLogValidationError("taken_time cannot be in the future.")

        # Optional: ensure taken_time is not before scheduled_time.
        if log.scheduled_time and log.taken_time < log.scheduled_time:
            raise IntakeLogValidationError(
                "taken_time cannot be earlier than scheduled_time."
            )

    @staticmethod
    def _validate_amount_taken(log: IntakeLog):
        """Confirm amount taken is present, numeric and within limits."""

        # amount_taken must be a number.
        if not isinstance(log.amount_taken, (int, float)):
            raise IntakeLogValidationError("amount_taken must be a number.")

        # amount_taken must be non-negative.
        if log.amount_taken < 0:
            raise IntakeLogValidationError("amount_taken cannot be negative.")

    @staticmethod
    def _validate_notes(log: IntakeLog):
        """Check that notes provided are acceptable and entered correctly."""

        # Notes are optional, but if provided, they must be a string.
        if log.notes is not None and not isinstance(log.notes, str):
            raise IntakeLogValidationError("Notes must be a string.")

        # Optional: enforce a reasonable length limit.
        if log.notes and len(log.notes) > 500:
            raise IntakeLogValidationError("Notes are too long.")
        
    @staticmethod
    def _validate_created_at(log: IntakeLog):
        """Ensure Intake log has a valid creation timestamp."""
        
        # Created time must be a datetime.
        if not isinstance(log.created_at, datetime):
            raise IntakeLogValidationError("created_at must be a datetime.")
        
        # Created log cannot be past the date of entry (in the future.)
        if log.created_at > datetime.now():
            raise IntakeLogValidationError("created_at cannot be in the future.")
        
    def add(self, log: IntakeLog):
        """Record this intake event in the log store."""
        
        # Ensure intake entry meets all validation rules.
        IntakeLogValidator.validate(log)

    def update(self, log: IntakeLog):
        """Provide changes to a previously saved intake record."""

        # Ensure intake entry meets all validation rules.
        IntakeLogValidator.validate(log)