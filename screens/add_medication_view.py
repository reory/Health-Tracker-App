import flet as ft
from typing import Any
# Import Models.
from models.medication import Medication

def add_medication_view(page: Any):
    """Form fields, Text fields are in this method to hold user info."""

    # Input fields
    name = ft.TextField(label="Medication Name")
    description = ft.TextField(label="Description / Instructions", multiline=True)
    dosage = ft.TextField(label="Dosage")
    notes = ft.TextField(label="Notes", multiline=True, min_lines=3)
    is_active = ft.Switch(label="Active Medication", value=True)

    def save_medication(e):
        """This function saves data to the database."""

        # Critical: force Flet to sync TextField values.
        page.update()

        # Create medication model instance.
        med = Medication(
            name=name.value or "",
            description=description.value or "",
            dosage=dosage.value or "",
            notes=notes.value or "",
            is_active=is_active.value,
            schedule=[]
        )

        # Save to the database.
        page.medication_repo.add(med)

        # Navigate back to the medications screen
        page.show_medications()

        # Show confirmation after navigation.
        page.snack_bar = ft.SnackBar(ft.Text("Medication saved"))
        page.snack_bar.open = True

        # Refresh page
        page.update()
    
    # UI Layout.
    return ft.View(
        route="/add_medication",
        controls=[
            ft.AppBar(
                title=ft.Text("Add Medication"),
                bgcolor=ft.Colors.GREEN,
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    on_click=lambda _: page.show_medications()
                ),
            ),
            ft.Column(
                [
                    name,
                    description,
                    dosage,
                    notes,
                    is_active,
                    ft.ElevatedButton(
                        "Save Medication",
                        icon=ft.Icons.SAVE,
                        bgcolor=ft.Colors.GREEN_100,
                        color=ft.Colors.WHITE,
                        on_click=save_medication
                    ),
                ],
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
            )
        ]
    )
