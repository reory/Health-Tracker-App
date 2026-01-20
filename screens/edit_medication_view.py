import flet as ft
# Import Models.
from models.medication import Medication


def edit_medication_view(page, med_id: str) -> ft.View:
    """Edit an existing medication entry and manage its schedule."""

    # Load medication from repository.
    med = page.medication_repo.get_by_id(med_id)

    # Load schedule (one schedule per medication)
    schedules = page.schedule_repo.get_by_medication(med_id)
    sched = schedules[0] if schedules else None

    # Pre-filled form fields medications only.
    name_field = ft.TextField(label="Medication Name", value=med.name)
    description_field = ft.TextField(
        label="Description / Instructions",
        multiline=True,
        value=med.description,
    )
    dosage_field = ft.TextField(label="Dosage", value=med.dosage)
    notes_field = ft.TextField(label="Notes", multiline=True, value=med.notes or "")
    is_active_switch = ft.Switch(label="Active Medication", value=med.is_active)

    def save_medication(e):
        """Triggered when the user submits edited medication data."""

        updated = Medication(
            id=med.id,
            name=name_field.value or "",
            description=description_field.value or "",
            dosage=dosage_field.value or "",
            notes=notes_field.value or "",
            is_active=is_active_switch.value,
            created_at=med.created_at,
        )

        page.medication_repo.update(updated)

        page.snack_bar = ft.SnackBar(ft.Text("Medication updated"))
        page.snack_bar.open = True
        page.update()

        page.show_medications()

    def cancel(e):
        """Navigation callback: route back to the medication screen."""

        page.show_medications()

    def delete_medication():
        """Handle a removal of a medication and refresh the medication view."""
        
        page.medication_repo.delete(med.id)
        page.schedule_repo.delete_by_medication(med.id)
        page.show_medications()

    # Show ADD Schedule or Edit Schedule depending on whether a schedule exists.
    if sched:
        schedule_button = ft.TextButton(
            "Edit Schedule",
            icon=ft.Icons.SCHEDULE,
            on_click=lambda _: page.show_edit_schedule(med.id),
        )
    else:
        schedule_button = ft.TextButton(
            "Add Schedule",
            icon=ft.Icons.ADD,
            on_click=lambda _:page.show_add_schedule(med.id),
        )
    
    # UI Layout.
    return ft.View(
        route="/edit_medication",
        controls=[
            ft.AppBar(
                title=ft.Text("Edit Medication"),
                bgcolor=ft.Colors.GREEN,
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_medications(),
                ),
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                   [
                       name_field,
                       description_field,
                       dosage_field,
                       notes_field,
                       is_active_switch,
                       
                       ft.Divider(),

                       schedule_button,

                       ft.Row(
                           [
                               ft.ElevatedButton(
                                   "Save Changes",
                                   icon=ft.Icons.SAVE,
                                   on_click=save_medication,
                               ),
                               ft.ElevatedButton(
                                   "Cancel",
                                   icon=ft.Icons.CLOSE,
                                   on_click=cancel,
                                ),
                                ft.ElevatedButton(
                                    "Delete Medication",
                                    icon=ft.Icons.DELETE,
                                    bgcolor=ft.Colors.RED,
                                    color=ft.Colors.BLACK,
                                    on_click=lambda _: delete_medication(),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                       ),
                            
                   ],
                   spacing=20,
                ),
            ),
        ],
    )
