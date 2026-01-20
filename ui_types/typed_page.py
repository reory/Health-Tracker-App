import flet as ft
# Import common typing helpers for functions signatures.
from typing import Callable, Optional, Any

class TypedPage(ft.Page):
    """Extend ft.Page with typed helpers and attributes."""

    # Database
    db: Any = None

    # Navigation callbacks
    show_dashboard: Optional[Callable] = None
    
    show_appointments: Optional[Callable] = None
    show_edit_appointment: Optional[Callable] = None
    show_add_appointment: Optional[Callable] = None

    show_medications: Optional[Callable] = None
    show_add_medication: Optional[Callable] = None
    show_edit_medication: Optional[Callable] = None

    show_schedule: Optional[Callable] = None
    show_add_schedule: Optional[Callable] = None
    show_edit_schedule: Optional[Callable] = None

    show_user_profile: Optional[Callable] = None
    show_settings: Optional[Callable] = None
    show_analytics: Optional[Callable] = None

    # Repositories
    appointment_repo: Any = None
    medication_repo: Any = None
    reminder_repo: Any = None
    schedule_repo: Any = None

    # Services
    schedule_service: Any = None
    scheduler: Any = None
    notifier: Any = None

    # UI elements
    snack_bar: Any = None

    # App start callback
    start: Optional[Callable] = None

    # Window properties
    window_width: Optional[int] = None
    window_height: Optional[int] = None