# Flet UI toolkit used for constructing and building the app interface.
import flet as ft
from models.appointment import Appointment
# Using Any so the linter doesn't complain about 
# custom page attributes (e.g., page.show_appointments)
from typing import Any

def add_appointment_view(page: Any) -> ft.View:
    """Construct the appointment view."""

    name_field = ft.TextField(label="Appointment Title")
    date_field = ft.TextField(label="Date (YYYY-MM-DD)")
    time_field = ft.TextField(label="Time (HH:MM)")
    location_field = ft.TextField(label="Location")
    notes_field = ft.TextField(label="Notes", multiline=True)

    def save_appointment(e):
        """Trigger when the user submits the appointment form."""
       
        # Create Appointment model instance.
        appt = Appointment(
           title=name_field.value or "",
           date=date_field.value or "",  
           time=time_field.value or "", 
           location=location_field.value or "",
           notes=notes_field.value
        )

        # Save to database
        page.appointment_repo.add(appt)

        # Navigate back to the appointments screen
        page.show_appointments()

        # Show confirmation after navigation.
        page.snack_bar = ft.SnackBar(ft.Text("Appointment saved"))
        page.snack_bar.open = True

        # Refresh the page.
        page.update()

    # UI layout.
    return ft.View(
        route="/add_appointment",
        controls=[
            ft.AppBar(
                title=ft.Text("Add Appointment"),
                bgcolor=ft.Colors.GREEN,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_appointments()
            ),
        ),           
        ft.Container(
            content=ft.Column(
                [
                    name_field,
                    date_field,
                    time_field,
                    location_field,
                    notes_field,
                    
                    ft.ElevatedButton(
                        "Save",
                        icon=ft.Icons.SAVE, 
                        on_click=save_appointment),
                    
                        ft.ElevatedButton(
                        "Cancel",
                        icon=ft.Icons.CLOSE,
                        on_click=lambda e: page.show_appointments()
                    ),
                ],
                spacing=20,
                expand=True,
            ),
            padding=20,
        )
    ],
)