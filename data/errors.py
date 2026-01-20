class DatabaseError(Exception):
    """Raised when a database operation fails."""

    pass


class NotFoundError(Exception):
    """Raised when a requested record does not exist."""
    
    pass