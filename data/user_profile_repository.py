import json
# Import Models.
from models.user_profile import UserProfile

class UserProfileRepository:
    """
    Handle loading and saving the single UserPorfile record.
    Stores these in a JSON format for flexibility and expansion.
    """

    def __init__(self, conn):
        self.conn = conn
        self._user_table()

    def _user_table(self):
        """Create the UserProfile table."""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profile (
                id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
            """
        )
        
    def get_profile(self) -> UserProfile | None:
        """Returns the stored UserProfile, or None if not set."""

        row = self.conn.execute(
            "SELECT id, data FROM  user_profile LIMIT 1"
        ).fetchone()

        if not row:
            return None
            
        data = json.loads(row["data"])
        return UserProfile.from_dict(data)
        
    def save_profile(self, profile: UserProfile):
        """Insert or update the UserProfile row."""

        # Turn the profile object into JSON for storage.
        data = json.dumps(profile.to_dict())

        # Check if profile already exists.
        existing = self.conn.execute(
            "SELECT id FROM user_profile LIMIT 1"
        ).fetchone()

        if existing:
            # Update existing row.
            self.conn.execute(
                "UPDATE user_profile SET data = ? WHERE id = ?",
                (data, existing["id"]),
            )
        else:
            # Insert new row.
            self.conn.execute(
                "INSERT INTO user_profile (id, data) VALUES (?, ?)",
                (profile.id, data),
            )

        self.conn.commit()