# Marks this class as a dataclass so field become typed attributes.
from dataclasses import dataclass
from .base import BaseModel


@dataclass
class Appointment(BaseModel):
    """Typed data model defining the fields for an appointment."""
    
    # Event title as text.
    title: str = ""
    # Event date as text.
    date: str = ""
    # Event time as text.
    time: str = ""
    # Where the event takes place.
    location: str = ""
    # Optional extra details.
    notes: str | None = None