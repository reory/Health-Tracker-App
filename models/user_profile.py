from dataclasses import dataclass, field
from .base import BaseModel

@dataclass
class UserProfile(BaseModel):
    """
    Core profile model extending BaseModel 
    with user-profile specific fields.
    """

    # Display name for the user(can be left unset if needed.)
    name: str | None = None
    # The user's preferred timezone for scheduling and reminders.
    timezone: str = "UTC"
    # The user's preferred measurments - weight, kg, lbs, etc.
    preferred_units: dict[str, str] = field(default_factory=dict)
    # User's birthdate in format (YYYY-MM-DD).
    date_of_birth: str | None = None
    # Name and number of an emergency contact.
    emergency_contact: str | None = None
    # General health notes - Medical conditons, Health preferences, etc.
    notes: str | None = None