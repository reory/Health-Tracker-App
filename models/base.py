from dataclasses import dataclass, field
from datetime import datetime, timezone
# Used to generate stable, unique IDs for models and records.
import uuid

@dataclass
class BaseModel:
    """Root model type; ensures consistent structure across all data class."""
    
    # Generate a unique ID for every model instance using UUID4.
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    # Store the creation and updated timestamps as a timezone UTC datetime.
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """Serialize this model into  a dict for JSON/storage."""

        # Create a copy of the instance dictionary(best practices for dataclass)
        data = self.__dict__.copy()

        #Convert datetime fields to ISO strings for serialization.
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        # Return the full serialized dictionary.
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create an object using the values in this dictionary."""

        # Convert ISO strings back to a readable datetime (format).
        parsed = data.copy()
        # Loop through the datetime fields we expoect in serialized form.
        for key in ("created_at", "updated_at"):
            # If the field exists and is stored as a string(isoformat).
            if key in parsed and isinstance(parsed[key], str):
                # Convert the string back to a proper datetime object.
                parsed[key] = datetime.fromisoformat(parsed[key])
        # create a new instance of this class using the parsed data.        
        return cls(**parsed)
    
    def mark_updated(self): 
        """
        Refresh the updated_at field so 
        repositories know this record has changed.
        """

        # Update the "updated_at" timestamp to the current UTC time.
        # Repositories or services can call this function.
        # This ensures whenever the model is modified tracking is accurate.
        self.updated_at = datetime.now(timezone.utc)

