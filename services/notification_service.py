import flet as ft
# Import Data.
from data.medication_repository import MedicationRepository
# Allows accepting any type where flexibility is needed.
from typing import Any

class NotificationService:
    """
    Handles UI notifications using Flets snackbar API.
    Snack bar is temporary message reminder from Flet.
    """

    def __init__(self, page: Any, medication_repo: MedicationRepository):
        """Wire up UI context and medication data access."""

        # Keep a reference to the page so we can trigger UI updates.
        self.page = page

        self.medication_repo = medication_repo

        # Allow the settings screen to enable/disable notifications.
        self.enabled=True

        # Create a resuable instance SnackBar instance ONCE
        # In Flet version 0.28.3, attachment of the object to the page overlay.
        self.snack_bar = ft.SnackBar(
            content=ft.Text(""),
            action="OK"
        )

        # Add the snack bar to the page overlay so it can be shown later.
        self.page.overlay.append(self.snack_bar)

    def send_notification(self, reminder):
        """Displays a notification for the ReminderEvent."""

        # The settings toggle - so settings can turn notifications on/off
        if not self.enabled:
            return
        
        # Look up medication name
        med = self.medication_repo.get_by_id(reminder.medication_id)
        if med is None:
            return

        # Build message.
        if med.dosage:
            message = f"Time to take {med.name} ({med.dosage})!"
        else:
            message = f"Time to take {med.name}"

        # Update the text dynamically.
        self.snack_bar.content = ft.Text(message)

        # Open the snack bar
        self.snack_bar.open = True

        # Refresh the UI.
        self.page.update()