# This is a Flet test file.
# Stripped-down version to isolate UI behaviour.

import flet as ft
from ui_types.typed_page import TypedPage
from data.database import Database


def medications_view(page: TypedPage) -> ft.View:
    def load_medications():
        meds = page.medication_repo.get_all()
        items = []

        if not meds:
            items.append(ft.Text("No medications added yet"))
            return items

        for med in meds:
            items.append(
                ft.Column(
                    [
                        ft.Text(f"Name: {med.name}"),
                        ft.Text(f"Dosage: {med.dosage}"),
                        ft.Text(f"Status: {'Active' if med.is_active else 'Inactive'}"),
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.Icons.EDIT),
                                ft.IconButton(icon=ft.Icons.DELETE),
                            ]
                        ),
                    ],
                    spacing=5,
                )
            )

        return items

    return ft.View(
        route="/medications",
        controls=[
            ft.Text("Your Medications", size=20, weight=ft.FontWeight.BOLD),
            ft.Column(load_medications(), spacing=10),
        ],
    )


def main(page: ft.Page):
    print(">>> TEST FILE IS RUNNING")

    # Upgrade the Flet page object to your custom class
    page.__class__ = TypedPage

    # Load your real database
    db = Database()
    page.medication_repo = db.medications

    # Fake navigation functions (not needed for the test)
    page.show_edit_medication = lambda mid: print("Edit", mid)
    page.show_add_medication = lambda: print("Add")

    # Show the stripped medications view
    page.views.append(medications_view(page))
    page.update()


ft.app(target=main)


