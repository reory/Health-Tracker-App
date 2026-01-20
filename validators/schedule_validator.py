from datetime import date, time
# Import Models.
from models.schedule import Schedule

# A dedicated exception type for schedule validation errors.
# Using a specific custom exception
# Allows the UI, repo and engine to specifically catch schedule related
# validation issues and handle them efficiently.
class ScheduleValidationError(Exception):
    """Custom exception for schedule validation errors."""
    pass

class ScheduleValidator:
    """Validates Schedule objects before saving or processing."""

    @staticmethod
    def validate(schedule: Schedule):
        """Ensure the schedule is struturally sound before use."""

       # Validate that the schedule has at least one valid time
        # All time entries are proper datetime.time objects.
        ScheduleValidator._validate_times(schedule)
        # Ensure start_date and end_date are valid and in logical order.
        ScheduleValidator._validate_dates(schedule)
        # Confirms that the frequency field must have values which are allowed.
        # (Daily, weekly, etc)
        ScheduleValidator._validate_frequency(schedule)
        # If schedule is weekly, this ensures days_of_week is valid and non empty.
        ScheduleValidator._validate_days_of_week(schedule)

    @staticmethod
    def _validate_times(schedule: Schedule):
        """Check that the schedules time values are valid."""

        # Schedule must have at least one time.
        if not schedule.times:
            raise ScheduleValidationError("Schedule must include at least one time of day.")
        
        # Ensures every entry in the list is a proper datetime.time object.
        # Protects against user bugs or incorrect deserialization.
        for t in schedule.times:
            if not isinstance(t, time):
                raise ScheduleValidationError(f"Invalid time object: {t}")
            
        # Convert the list to a set to detect duplicate entries.
        # If the set is smaller, it means at least one time was duplicated.
        if len(schedule.times) > len(set(schedule.times)):
            raise ScheduleValidationError("Duplicate times are not allowed.")
        
    @staticmethod
    def _validate_dates(schedule: Schedule):
        """Ensure dates are present, well formed and logically consistent."""

        if not isinstance(schedule.start_date, date):
            raise ScheduleValidationError("Start date must be a valid date.")

        if schedule.end_date is not None:
            if not isinstance(schedule.end_date, date):
                raise ScheduleValidationError("End date must be a valid date or None.")

            if schedule.start_date > schedule.end_date:
                raise ScheduleValidationError("Start date cannot be after end date.")

    @staticmethod
    def _validate_frequency(schedule: Schedule):
        """Ensure the frequency is present, valid and supported by the system."""

        allowed = {"daily", "weekly", "custom"}

        if schedule.frequency not in allowed:
            raise ScheduleValidationError(
                f"Invalid frequency '{schedule.frequency}'. "
                f"Allowed values: {', '.join(allowed)}"
            )

    @staticmethod
    def _validate_days_of_week(schedule: Schedule):
        """Check that the schedules chose week days are valid."""

        if schedule.frequency != "weekly":
            return

        if not schedule.days_of_week:
            raise ScheduleValidationError("Weekly schedules must specify days_of_week.")

        for d in schedule.days_of_week:
            if d not in range(7):
                raise ScheduleValidationError(
                    f"Invalid day_of_week '{d}'. Must be between 0 (Mon) and 6 (Sun)."
                )

