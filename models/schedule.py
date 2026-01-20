from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import List, Optional
import uuid

@dataclass
class Schedule:
    """Typed data model defining schedule settings and scheduling rules."""

    # Auto generate a unique ID.
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # Stores the ID of the medication this item belongs to.
    medication_id: str = ""
    # Time of day the dose should be taken. anytime the user sets.
    times: List[time] = field(default_factory=list)
    # Daily, weekly, customizable
    frequency: str = "daily" 
    # Days of the week the dosage should be taken. (0=mon 6=sun) 
    days_of_week: List[int] = field(default_factory=list)
    # Start and end dates for the schedule.
    start_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None
    # Whether the schedule is currently active.
    is_active: bool = True
    # Timestamp when the schedule was created.
    created_at: datetime = field(default_factory=datetime.now)
    
    