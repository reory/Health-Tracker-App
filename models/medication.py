from dataclasses import dataclass, field
from datetime import datetime
from .dosage import Dosage
from .schedule import Schedule
from .base import BaseModel

@dataclass
class Medication(BaseModel):
    """Core data model defining all medication fields and behaviour."""

    # Primary key for this medication, stored as a string.
    id: str = ""
    # Name of the medication - Asprin, Anadin, etc.
    name: str = ""
    # Descriptions of medication or instructions on how to take them.
    description: str = ""
    # Dosage information - amount, units or forms.
    dosage: str = ""
    # Medication schedules - morning, evening, etc.
    schedule: list[Schedule] = field(default_factory=list)
    # Allows medication to be archived without deleting the information.
    is_active: bool = True
    # Allows notes to be taken about medication, etc.
    notes: str = ""