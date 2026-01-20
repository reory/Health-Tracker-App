# 8.1.25.
import flet as ft
# Import Data.
from data.database import Database
# Trying to silence the linter as the flet code accpets dynamic attributes.
from ui_types.typed_page import TypedPage

# Import screens.
from screens.dashboard_view import dashboard_view
from screens.appointments_view import appointments_view
from screens.add_appointment_view import add_appointment_view
from screens.edit_appointment_view import edit_appointment_view
from screens.medications_view import medications_view
from screens.add_medication_view import add_medication_view
from screens.edit_medication_view import edit_medication_view
from screens.add_schedule_view import add_schedule_view
from screens.edit_schedule_view import edit_schedule_view
from screens.settings_view import settings_view
from screens.user_profile_view import user_profile_view
from screens.analytics_view import analytics_view
# Import services
from services.notification_service import NotificationService
from services.reminders import ReminderService
from services.schedule_engine import ScheduleEngine
from services.schedule_service import ScheduleService
from services.scheduler_service import SchedulerService



# App configuration
def main(page: TypedPage):
    """Construct the root UI and wire up Navigation/context."""
    
    page.__class__ = TypedPage
    page.title = "Health Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Window width and height of the app.(customizable)
    page.window_width = 500
    page.window_height = 500

    # Initialize database (all repos created inside)
    page.db = Database() 

    # Initialize services - business logic layer.
    schedule_service = ScheduleService(
        reminder_repo=page.db.reminders,
        schedule_repo=page.db.schedules 
    )

    # Notification service needs the page
    notifier = NotificationService(page, page.db.medications)


    schedule_engine = ScheduleEngine(
        medication_repo=page.db.medications,
        schedule_repo=page.db.schedules
    )

    reminder_service = ReminderService(
        medication_repo=page.db.medications,
        schedule_repo=page.db.schedules,
        intake_repo=page.db.intake_logs,
        reminder_repo=page.db.reminders,
        schedule_engine=schedule_engine
    )

    # Background scheduler (Thread safe)
    page.scheduler = SchedulerService(notifier=notifier)
    page.scheduler.start()

    # Router - handles navigation.
    def show(view_func):
        """Central for rendering views within the navigation flow."""

        view = view_func(page)
        page.views.clear()
        page.views.append(view)
        page.update()

    # Expose navigation functions to screens
    page.show_dashboard = lambda: show(dashboard_view) 
    page.show_user_profile = lambda: show(user_profile_view)
    page.show_medications = lambda: show(medications_view)
    page.show_add_medication = lambda: show(add_medication_view) 
    page.show_edit_medication = lambda med_id: show(
        lambda p: edit_medication_view(p, str(med_id)))
    page.show_appointments = lambda: show(appointments_view) 
    page.show_add_appointment = lambda: show(add_appointment_view)
    page.show_edit_appointment = lambda appt_id: show(
        lambda p: edit_appointment_view(p, str(appt_id)))
    page.show_add_schedule = lambda med_id: show(
        lambda p: add_schedule_view(p, med_id)
    )
    page.show_edit_schedule = lambda sched_id: show(
        lambda p: edit_schedule_view(p, str(sched_id))) 
    
    page.show_settings = lambda: show(settings_view) 
    page.show_analytics = lambda: show(analytics_view)

    # Show services to screens, so screens can access repos/services if needed.
    page.appointment_repo = page.db.appointments 
    page.medication_repo = page.db.medications 
    page.notifier = notifier 
    page.reminder_repo = page.db.reminders 
    page.schedule_repo = page.db.schedules 
    page.schedule_service = schedule_service 
    


    # Start at dashboard
    show(dashboard_view)
   
# Launch the app.
ft.app(main)