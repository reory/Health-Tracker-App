# Used to run the scheduler in the background.
import threading
# Provide the sleep() function for the minute by minute loop.
import time
from datetime import datetime

# Imports from Data.
from data.database import get_connection
from data.schedule_repository import ScheduleRepository
from data.reminder_repository import ReminderRepository
from data.medication_repository import MedicationRepository
from data.intake_log_repository import IntakeLogRepository

# Imports from services.
from services.reminders import ReminderService
from services.notification_service import NotificationService
from services.schedule_engine import ScheduleEngine


class SchedulerService:
    """
    Background scheduler that checks for due reminders every minute
    and triggers notifications.
    """

    def __init__(self, notifier: NotificationService):
        """Set up the object with the notifier used to send notifications."""
        
        # Store notification service.
        self.notifier = notifier
        # Engine starts inactive. (False)
        self.running = False
        # Background thread placeholder.
        self.thread = None

    def start(self):
        """Starts the background scheduler loop."""
        
        # Prevent duplicate worker threads.
        if self.running:
            return
        # Set engine state to running.
        self.running = True
        # Intialize daemon thread for schedule processing.
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        # Kicks off the schedule processing thread.
        self.thread.start()

    def stop(self):
        """Stops the scheduler loop."""

        self.running = False

    def _run_loop(self):
        """Continuously check for and handle due schedules."""

        # All DB objects are created Inside the scheduler thread.
        conn = get_connection()

        # Thread safe repositories.
        schedule_repo = ScheduleRepository(conn)
        medication_repo = MedicationRepository(conn, schedule_repo)
        reminder_repo = ReminderRepository(conn)
        intake_repo = IntakeLogRepository(conn)

        # Thread safe schedule engine.
        schedule_engine = ScheduleEngine(
            medication_repo=medication_repo,
            schedule_repo=schedule_repo
        )

        # Thread safe reminder service.
        reminder_service = ReminderService(
            schedule_repo=schedule_repo,
            reminder_repo=reminder_repo,
            medication_repo=medication_repo,
            intake_repo=intake_repo,
            schedule_engine=schedule_engine
        )

        while self.running:
            
            # ReminderService already uses datetime.now() internally.
            due_events = reminder_service.get_due()

            
            # Process each scheduled due event.
            for event in due_events:

                # Trigger UI notifications
                self.notifier.send_notification(event)

            # Sleep until the next minute
            time.sleep(60)

            
