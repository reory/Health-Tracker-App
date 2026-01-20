from dataclasses import dataclass, field
import uuid

@dataclass
class Reminder:
    """Typed data model defining reminder settings and scheduling rules."""

    # Auto generate a unique ID.
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # Reference to the medication this event is associated with.
    medication_id: str = ""
    # The specific scheduled entry this reminder is tied to.
    scheduled_id: str = ""
    # Whether this reminder is currently active/enabled
    enabled: bool = True
    # How many minutes before the scheduled time that the reminder should work.
    reminder_offset_minutes: int = 10