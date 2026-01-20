import flet as ft
from typing import Any

def quick_action(icon, label, on_click):
    """This fades in label on hover over the buttons."""

    text = ft.Text(
        label,
        opacity=0,
        animate_opacity=100,
        size=16,
        weight=ft.FontWeight.W_900,
    )

    def on_hover(e):
        """Show text while hovering over a button."""

        text.opacity = 1 if e.data == "true" else 0
        text.update()

    return ft.Row(
       [
            ft.IconButton(
                icon=icon,
                on_click=on_click,
                on_hover=on_hover,
                icon_size=22,
            ),
            text,
        ],
        spacing=5,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

def dashboard_view(page: Any):
    """
    Main dashboard screen.
    Consistent with the rest of the apps architecture and styling.
    It contains an AppBar and a list of controls.
    """

    # Pull basic stats from repositories.
    meds = page.medication_repo.get_all()
    active_meds = [m for m in meds if m.is_active]

    total_meds = len(meds)
    active_count = len(active_meds)

    # Small helper for consistent stat cards.
    def stat_card(title: str, value: str, icon: str, color: str):
        """A factory for a reusable analytics stat card component."""

        return ft.Container(
            padding=15,
            bgcolor=color,
            border_radius=10,
            content=ft.Row(
                [
                    ft.Icon(icon, size=32, color=ft.Colors.WHITE),
                    ft.Column(
                        [
                            ft.Text(title, size=14, color=ft.Colors.WHITE),
                            ft.Text(
                                value,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        )
    
    # Quick navigation buttons.
    quick_actions = ft.Column(
        [
            quick_action(
                ft.Icons.MEDICATION,
                "Medications",
                lambda _: page.show_medications(),
            ),
            quick_action(
                ft.Icons.EVENT,
                "Appointments",
                lambda _: page.show_appointments(),
            ),
            quick_action(
                ft.Icons.SETTINGS,
                "Settings",
                lambda _: page.show_settings(),
            ),
            quick_action(
                ft.Icons.PERSON_PIN,
                "User Profile",
                lambda _: page.show_user_profile(),
            ),
            quick_action(
                ft.Icons.SHOW_CHART_ROUNDED,
                "Analytics",
                lambda _: page.show_analytics(),
            ),
        ],
        spacing=5,
    )
    
    # UI Layout.
    return ft.View(
        route="/",
        controls=[
            ft.AppBar(
                title=ft.Text("Dashboard"),
                bgcolor=ft.Colors.GREEN,
                center_title=True,
            ),
            ft.Container(
                padding=ft.Padding(20,20,20,80), # Padding added to lift buttons.
                content=ft.Column(
                    [   
                        # Welcome header.
                        ft.Text(
                            "Welcome to your Health Tracker.",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Here's a quick overview of your health activity.",
                            size=16,
                            italic=True,
                            color=ft.Colors.GREY,
                        ),

                        ft.Divider(
                            color=ft.Colors.GREEN,
                            thickness=20,
                            leading_indent=0,
                            trailing_indent=860,
                        ),

                        # Stats section.
                        ft.Text(
                            "Your Stats",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Container(
                            padding=ft.Padding(0, 0, 860, -25),
                            content=stat_card(
                                     "Active Medications",
                                     str(active_count),
                                     ft.Icons.CHECK_CIRCLE,
                                     ft.Colors.GREEN,
                            ),
                        ),
                        
                        ft.Divider(
                            color=ft.Colors.GREEN,
                            thickness=20,
                            leading_indent=0,
                            trailing_indent=860,
                        ),

                        # Quick actions.
                        ft.Text(
                            "Quick Actions",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Hover over an icon to see its label",
                            size=14,
                            italic=True,
                            color=ft.Colors.GREY,    
                        ),
                        quick_actions,
                    ],
                    spacing=20,
                    expand=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        ],
    )
