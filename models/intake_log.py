from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

@dataclass
class IntakeLog:
    """Typed data model capturing when and how a dose was taken."""

    # Unique identifier for this  intake record.
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # The ID of the medication this log refers to.
    medication_id: str = ""
    # The time that the dosage should have been taken.
    scheduled_time: datetime | None = None
    # The actual time that the user took the medication(UTC, timezone)
    taken_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    # How much of the medication was taken.
    amount_taken: float = 0.0
    # Notes a user may add, if any.
    notes: str | None = None
    # The time that the log was created.
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    