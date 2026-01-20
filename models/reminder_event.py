from dataclasses import dataclass
from datetime import datetime

@dataclass
class ReminderEvent:
    """Typed data model defining a reminder's timing and metadata."""

    # The medication this reminder is associated with.
    medication_id: str
    # The specific scheduled entry that generates this reminder.
    schedule_id: str
    # The exact time the medication is supposed to be taken.
    schedule_time: datetime
    # The time that the reminder should notify.
    reminder_time: datetime
    # Whether the user has already logged that the dose has been taken.
    is_taken: bool
    # Only True if the scheduled_time has passed and the dose was missed.
    is_overdue: bool

    def is_due(self) -> bool:
        """Determin if the scheduled time has passed and the event is due."""

        # Trigger only when scheduled time has passed.
        # And the event is still pending.
        return datetime.now() >= self.reminder_time and not self.is_taken