# Import common typing helpers for functions signatures.
from collections.abc import Callable
from typing import Any

import flet as ft


class TypedPage(ft.Page):
    """Extend ft.Page with typed helpers and attributes."""

    # Database
    db: Any = None

    # Navigation callbacks
    show_dashboard: Callable | None = None
    
    show_appointments: Callable | None = None
    show_edit_appointment: Callable | None = None
    show_add_appointment: Callable | None = None

    show_medications: Callable | None = None
    show_add_medication: Callable | None = None
    show_edit_medication: Callable | None = None

    show_schedule: Callable | None = None
    show_add_schedule: Callable | None = None
    show_edit_schedule: Callable | None = None

    show_user_profile: Callable | None = None
    show_settings: Callable | None = None
    show_analytics: Callable | None = None

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
    start: Callable | None = None

    # Window properties
    window_width: int | None = None
    window_height: int | None = None