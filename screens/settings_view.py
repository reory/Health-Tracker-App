import flet as ft
from typing import Any

def settings_view(page: Any) -> ft.View:
    """Construct the settings view using the shared page context."""

    def toggle_theme(e):
        """Callback to update the app's theme and refresh the UI."""

        page.theme_mode = (
            ft.ThemeMode.DARK 
            if page.theme_mode == ft.ThemeMode.LIGHT 
            else ft.ThemeMode.LIGHT
        )
        page.update()

    def toggle_notifications(e):
        """Callback to updates the app's notification state and refresh the UI."""

        # Reflect the users toggle choice in the app's notification settings.
        page.notifier.enabled = e.control.value

        # Update the existing snack bar from the NotificationService.
        page.notifier.snack_bar.content = ft.Text(
            "Notifications" + ("enabled" if e.control.value else "disabled")
        )
        page.notifier.snack_bar.open = True
        page.update()
    
    # UI Layout.
    return ft.View(
        route="/settings",
        controls=[
            ft.AppBar(
                title=ft.Text("Settings"),
                bgcolor=ft.Colors.GREEN,
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda e: page.show_dashboard()
                ),
            ),
            ft.Column([
                ft.Text("Customize your experience", size=18, weight=ft.FontWeight.BOLD),
                ft.Switch(label="Dark Mode", value=False, on_change=toggle_theme),
                ft.Switch(label="Enable Notifications", value=True, on_change=toggle_notifications),
                ft.Divider(),
                ft.Text("More settings coming soon...", italic=True),
            ], spacing=20, 
               expand=True
        ),
    ],
)