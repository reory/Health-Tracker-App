import flet as ft
# Import Models.
from models.appointment import Appointment
from typing import Any


def edit_appointment_view(page: Any, appointment_id: str) -> ft.View:
    """Construct the edit appointment view using ths shared page context."""

    appt = page.appointment_repo.get_by_id(appointment_id)

    if appt is None:
        return ft.View(
            route="/edit_appointment",
            controls=[ft.Text("Appointment not found")]
        )

    name_field = ft.TextField(label="Appointment Title", value=appt.title)
    date_field = ft.TextField(label="Date (YYYY-MM-DD)", value=appt.date)
    time_field = ft.TextField(label="Time (HH:MM)", value=appt.time)
    location_field = ft.TextField(label="Location", value=appt.location)
    notes_field = ft.TextField(label="Notes", multiline=True, value=appt.notes)

    def save_changes(e):
        """Triggered when the user submits edited appointment data."""
        
        appt.title = name_field.value
        appt.date = date_field.value
        appt.time = time_field.value
        appt.location = location_field.value
        appt.notes = notes_field.value

        page.appointment_repo.update(appt)
        page.show_appointments()

        page.snack_bar = ft.SnackBar(ft.Text("Appointment updated"))
        page.snack_bar.open = True
        page.update()
    
    # UI Layout.
    return ft.View(
        route="/edit_appointment",
        controls=[
            ft.AppBar(
                title=ft.Text("Edit Appointment"),
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
                        "Save Changes",
                        icon=ft.Icons.SAVE,
                        on_click=save_changes),

                    ft.ElevatedButton(
                        "Cancel",
                        icon=ft.Icons.CLOSE,
                        on_click=lambda _: page.show_appointments()
                    ),
                ],
                spacing=20,
                expand=True,
            ),
            padding=20,
        )
    ],
)
