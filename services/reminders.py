from datetime import datetime, timedelta
from typing import List
# Import Models.
from models.reminder_event import ReminderEvent
# Import Data.
from data.medication_repository import MedicationRepository
from data.schedule_repository import ScheduleRepository
from data.intake_log_repository import IntakeLogRepository
from data.reminder_repository import ReminderRepository
# Import Services.
from services.schedule_engine import ScheduleEngine


class ReminderService:
    """
    Generates runtime reminder events based on schedules, 
    reminder settings, and intake logs.
    """

    def __init__(
        self,
        medication_repo: MedicationRepository,
        schedule_repo: ScheduleRepository,
        intake_repo: IntakeLogRepository,
        reminder_repo: ReminderRepository,
        schedule_engine: ScheduleEngine
    ):  # Wire up medication, schedule, intake, reminders and scheduling engine.
        self.medication_repo = medication_repo
        self.schedule_repo = schedule_repo
        self.intake_repo = intake_repo
        self.reminder_repo = reminder_repo
        self.schedule_engine = schedule_engine

    def generate_events(self) -> List[ReminderEvent]:
        """Generate all reminder events for all schedules."""

        events = []

        schedules = self.schedule_repo.get_all()

        for schedule in schedules:
            reminders = self.reminder_repo.get_by_schedule(schedule.id)

            # If no reminder settings exist, skip
            if not reminders:
                continue

            # Expand schedule into actual times
            dose_times = self.schedule_engine.generate_dose_events(schedule)

            for scheduled_time in dose_times:
                for reminder in reminders:
                    if not reminder.enabled:
                        continue

                    reminder_time = scheduled_time - timedelta(
                        minutes=reminder.reminder_offset_minutes
                    )

                    # Check if taken
                    taken = self._is_taken(
                        medication_id=schedule.medication_id,
                        scheduled_time=scheduled_time
                    )

                    # Determine overdue
                    now = datetime.now()
                    overdue = (scheduled_time < now) and not taken

                    events.append(
                        ReminderEvent(
                            medication_id=schedule.medication_id,
                            schedule_id=schedule.id,
                            schedule_time=scheduled_time,
                            reminder_time=reminder_time,
                            is_taken=taken,
                            is_overdue=overdue,
                        )
                    )

        return events

    
    # Helper method.
    def _is_taken(self, medication_id: str, scheduled_time: datetime) -> bool:
        """Return True if an intake log exists for this medication/time."""

        logs = self.intake_repo.get_by_medication(medication_id)
        for log in logs:
            if log.scheduled_time == scheduled_time:
                return True
        return False


    # Filtered views
    def get_upcoming(self) -> List[ReminderEvent]:
        """Return reminders whose reminder_time is in the future."""

        now = datetime.now()
        return [
            e for e in self.generate_events()
            if e.reminder_time > now and not e.is_taken
        ]

    def get_due(self) -> List[ReminderEvent]:
        """Return reminders whose reminder_time 
        has passed but scheduled_time has not."""

        now = datetime.now()
        return [
            e for e in self.generate_events()
            if e.reminder_time <= now <= e.schedule_time and not e.is_taken
        ]

    def get_overdue(self) -> List[ReminderEvent]:
        """
        Return reminders where the scheduled time has passed 
        and the dose was not taken.
        """
        return [e for e in self.generate_events() if e.is_overdue]
    

    def get_next_for_medication(self, medication_id: str):
        """Return the next upcoming reminder for a specific medication."""
        
        upcoming = [
            e for e in self.get_upcoming()
            if e.medication_id == medication_id
        ]
        
        # Select the next schedule reminder based on the reminder_time.
        return min(upcoming, key=lambda e: e.reminder_time)if upcoming else None
