from dataclasses import dataclass
from typing import Optional

@dataclass
class Dosage:
    """Typed data model defining dosage amount and units."""

    # Displays numerical amount of the medication - 2.5, 500, 137.5, etc
    amount: float
    # Displays unit of measurement - # mg, ml, tablets, drops, amounts, etc
    unit: str              
    
    # Description of the medication form - tablet, capsule, etc.
    # None means if no form filled in that is fine, excepts a str or none.
    form: str | None = None

    def __str__(self) -> str:
        """Serialize dosage to a simple string format."""

        if self.form:
            # Include form when present.
            return f"{self.amount}|{self.unit}|{self.form}"
        # fallback: serialize amount + unit only.
        return f"{self.amount}|{self.unit}"
    

    
    @staticmethod
    def from_string(value: str) -> Optional ["Dosage"]:
        """Deserialize dosage from the stored string format."""

        if not value:
            return None # No dasage stored nothing to parse.
        
        # Split the serialized dosage string into components.
        parts = value.split("|") 
        # First part = numeric amount
        amount = float(parts[0])
        # second part = units(mg, ml, lb, etc)
        unit = parts[1]
        # Optional form field - only if present in the data.
        form = parts[2] if len(parts) > 2 and parts[2] else None
        
        # Creat a dosage instance from these values.
        return Dosage(amount=amount, unit=unit, form=form)