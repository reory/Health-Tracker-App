# Import Models.
from models.reminder import Reminder

class ReminderValidationError(Exception):
    """Custom exception for reminder validation errors."""
    pass

class ReminderValidator:
    """Validates reminder object before saving or validating."""

    @staticmethod
    def validate(reminder: Reminder) -> None:
        """Check that the reminder meets all required rules."""

        # Validates that the reminder is linked to a real medication.
        ReminderValidator._validate_medication_id(reminder)
        # Validate that the reminder is matched up to a specific entry.
        ReminderValidator._validate_scheduled_id(reminder)
        # Validate that the reminder is currently enable/disabled using a 
        # proper boolean function.
        ReminderValidator._validate_enabled(reminder)
        # Validate that the offset(mins before dosage) is a valid non negative
        # integer.
        ReminderValidator._validate_offset(reminder)

    @staticmethod
    def _validate_medication_id(reminder: Reminder) -> None:
        """Ensure the reminder references a valid medication."""

        if not isinstance(
            reminder.medication_id, str) or not reminder.medication_id.strip():
            raise ReminderValidationError(
                "medication_id must be a non-empty string.")

    @ staticmethod
    def _validate_scheduled_id(reminder: Reminder) -> None:
        """Ensure the reminder references a valid schedule."""

        if not isinstance(
            reminder.scheduled_id, str) or not reminder.scheduled_id. strip():
            raise ReminderValidationError(
                "scheduled_id must be a non-empty string.")

    @staticmethod
    def _validate_enabled(reminder: Reminder) -> None:
        """Check that the reminders enable state is valid."""

        if not isinstance(reminder.enabled, bool):
            raise ReminderValidationError("enabled must be a boolean.")
        
    @staticmethod
    def _validate_offset(reminder: Reminder) -> None:
        """Ensure the offset is a valid, supported number of minutes."""

        if not isinstance(reminder.reminder_offset_minutes, int):
            raise ReminderValidationError(
                "reminder_offset_minutes must be an integer.")
        if reminder.reminder_offset_minutes < 0: # Less than 0
            raise ReminderValidationError(
                "reminder_offset_minutes cannot be negative.")
        if reminder.reminder_offset_minutes > 1440: # greater then 24 hours.
            raise ReminderValidationError(
                "reminder_offset_minutes is too large.")