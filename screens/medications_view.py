import flet as ft
from ui_types.typed_page import TypedPage

def medication_card(med, on_click):
    """
    A clean and modern look medication title with,
    icon, name, dosage, status badge and chevron
    """

    status_label = "Active" if med.is_active else "Inactive"
    status_color = ft.Colors.GREEN if med.is_active else ft.Colors.GREY
    bg_color = ft.Colors.GREEN_100 if med.is_active else ft.Colors.GREY_100
    
    # UI Layout.
    return ft.Container(
        bgcolor=bg_color,
        border_radius=12,
        padding=12,
        margin=ft.margin.only(bottom=10),
        on_click=on_click,
        content=ft.Row(
            [
                ft.Icon(ft.Icons.MEDICATION, size=32, color=ft.Colors.BLUE),
                ft.Column(
                    [
                        ft.Text(
                            med.name,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            med.dosage,
                            size=16,
                            color=ft.Colors.GREY,
                        ),    
                        ft.Text(
                            med.description,
                            size=14,
                            color=ft.Colors.GREY,
                        ),
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=8, vertical=4),
                            bgcolor=status_color,
                            border_radius=20,
                            content=ft.Text(
                                status_label,
                                size=12,
                                color=ft.Colors.WHITE,
                            ),
                        )
                    ],
                    spacing=3,
                    expand=True,
                ),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20, color=ft.Colors.GREY),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
    )

def medications_view(page: TypedPage) -> ft.View:
    """Construct the medication view using the typed page context."""

    def load_medications():
        """Retrieve medication records from the repository."""
        
        meds = page.medication_repo.get_all()
        
        if not meds:
            return [
                ft.Text(
                    "No medications added yet.",
                    size=16,
                    color=ft.Colors.GREY,
                    italic=True,
                )
            ]

        return [
            medication_card(
                med,
                lambda e, m=med: page.show_edit_medication(m.id) #type:ignore
            )
            for med in meds
        ]   
    
    # UI Layout.
    return ft.View(
        route="/medications",
        controls=[
            ft.AppBar(
                title=ft.Text("Your Medications"),
                bgcolor=ft.Colors.GREEN,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_dashboard(), #type:ignore
                ),
            ),

            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text(
                            "Medication List",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Tap a medication to view or edit details.",
                            size=14,
                            italic=True,
                            color=ft.Colors.GREY,
                        ),
                        ft.Divider(
                            color=ft.Colors.GREEN_100,
                            thickness=4,
                            leading_indent=0,
                            trailing_indent=200,
                        ),
                        ft.Column(
                            load_medications(),
                            spacing=10,
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        ft.FloatingActionButton(
                            icon=ft.Icons.ADD,
                            autofocus=True,
                            bgcolor=ft.Colors.GREEN,
                            on_click=lambda e: page.show_add_medication(), #type:ignore
                        ),
                    ],
                    spacing=20,
                ),
            ),
        ],
    )