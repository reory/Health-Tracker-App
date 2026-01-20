import flet as ft
from ui_types.typed_page import TypedPage


def appointments_view(page: TypedPage) -> ft.View:
    """Build the main appointments screen."""

    def load_appointments():
        """Retrieve the appointment records from the appointment repository."""

        appts = page.appointment_repo.get_all()
        items = []

        if not appts:
            items.append(ft.Text("No appointments scheduled yet"))
            return items

        for appt in appts:
            items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Title: {appt.title}",
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(f"Date: {appt.date}"),
                            ft.Text(f"Time: {appt.time}"),
                            ft.Text(f"Location: {appt.location}"),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Edit",
                                        on_click=lambda e, aid=appt.id: page.show_edit_appointment(aid)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Delete",
                                        on_click=lambda e, aid=appt.id: delete_appointment(aid)
                                    ),
                                ]
                            ),
                        ],
                        spacing=5,
                    ),
                    padding=10,
                    bgcolor=ft.Colors.SURFACE,
                    border_radius=8,
                    margin=ft.margin.only(bottom=10),
                )
            )

        return items

    def delete_appointment(appt_id: str):
        """Repository: Delete the appointment record with the given ID."""
        
        page.appointment_repo.delete(appt_id)
        page.show_appointments()
    
    # UI Layout.
    return ft.View(
        route="/appointments",
        controls=[
            ft.AppBar(
                title=ft.Text("Your Appointments"),
                bgcolor=ft.Colors.GREEN,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_dashboard()
                ),
            ),
            ft.Column(load_appointments(), spacing=10),

            ft.ElevatedButton(
                "Add Appointment",
                icon=ft.Icons.ADD_CARD,
                on_click=lambda _: page.show_add_appointment(),
            ),
        ]
    )

