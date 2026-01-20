import flet as ft
from typing import Any
# Import Models.
from models.user_profile import UserProfile

def user_profile_view(page: Any) -> ft.View:
    """Generates a User profile screen."""

    # Load default profile.
    profile = page.db.user_profile.get_profile()
    if profile is None:
        profile = UserProfile(
            name=None,
            timezone="UTC",
            preferred_units={},
            date_of_birth=None,
            emergency_contact=None,
            notes=None,
        )
        page.db.user_profile.save_profile(profile)


    # Form fields
    name_field = ft.TextField(
         label="Display Name",
         value=profile.name or "",
    )

    dob_field = ft.TextField(
            label="Date of Birth (YYYY-MM-DD)",
            value=profile.date_of_birth or "",
    )
        
    timezone_field = ft.TextField(
         label="Timezone",
         value=profile.timezone,
    )

    weight_dropdown = ft.Dropdown(
        label="Weight Units",
        options=[
            ft.dropdown.Option("kg"),
            ft.dropdown.Option("lbs"),
        ],
        value=(profile.preferred_units.get("weight") 
               if profile.preferred_units else "kg"),
    )

    height_dropdown = ft.Dropdown(
        label="Height Units",
        options=[
            ft.dropdown.Option("cm"),
            ft.dropdown.Option("ft/in"),
        ],
        value=(profile.preferred_units.get("height") 
               if profile. preferred_units
               else "cm"),
    )

    emergency_contact_field = ft.TextField(
         label="Emergency Contact",
         value=profile.emergency_contact or "",
    )

    notes_field = ft.TextField(
         label="Health Notes",
         value=profile.notes or "",
         multiline=True,
    )

    # Save logic
    def save_changes(e):
        """Save the users changes to the database."""

        parsed_units = {
            "weight": weight_dropdown.value or "kg",
            "height": height_dropdown.value or "ft/in",
        }
            
        updated = UserProfile(
            name=name_field.value,
            timezone=timezone_field.value or "",
            preferred_units=parsed_units,
            date_of_birth=dob_field.value,
            emergency_contact=emergency_contact_field.value,
            notes=notes_field.value,
        )

        page.db.user_profile.save_profile(updated)

        page.snack_bar = ft.SnackBar(ft.Text("Profile updated"))
        page.snack_bar.open = True
        page.update()

        # Go back to dashboard view after making the saved changes.
        page.show_dashboard()

    def cancel(e):
        """Cancel a User's profile returns back to the dashboard."""

        page.show_dashboard()

    def reset_profile(e):
        """Handles profile reset and reapplies default config values."""

        default_name = UserProfile(
            name="",
            timezone="UTC",
            preferred_units={
                "height": "cm",
                "weight": "kg",
            },
            date_of_birth="",
            emergency_contact="",
            notes="",
        )

    # UI layout
    return ft.View(
        route="/user_profile",
        controls=[
            ft.AppBar(
                title=ft.Text("User Profile"),
                bgcolor=ft.Colors.GREEN,
                center_title=True,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: page.show_dashboard()
                ),
            ),
            ft.Column(
                [
                    ft.Text(
                        "Your information",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    name_field,
                    dob_field,
                    timezone_field,

                    ft.Text(
                        "Preferences",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    weight_dropdown,
                    height_dropdown,

                    ft.Text(
                        "Emergency & Notes",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                    ),
                    emergency_contact_field,
                    notes_field,

                    ft.ElevatedButton(
                        "Save Changes",
                        icon=ft.Icons.SAVE,
                        on_click=save_changes,
                    ),

                    ft.ElevatedButton(
                        "Cancel",
                        icon=ft.Icons.CLOSE,
                        on_click=cancel,
                    ),
                    ft.ElevatedButton(
                        "Reset User Porfile",
                        icon=ft.Icons.RESTORE,
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.BLACK,
                        on_click=reset_profile,
                    ),
                ],
                spacing=20,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
        ],
    )