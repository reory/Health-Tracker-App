from datetime import datetime, timedelta
# Used to annotate functions returning a listof items.
from typing import List
# Import Data.
from data.reminder_repository import ReminderRepository
from data.schedule_repository import ScheduleRepository
# Import Models.
from models.reminder import Reminder


class ScheduleService:
    """
    Combines schedules + reminders to determine which reminders
    are due at the current moment.
    """

    def __init__(self, reminder_repo: ReminderRepository, schedule_repo: ScheduleRepository):
        """Inject reminders and scheduling files for operations."""

        self.reminder_repo = reminder_repo
        self.schedule_repo = schedule_repo

    def get_due_reminders(self, now: datetime) -> List[Reminder]:
        """Compute which reminder are due based on the provided timestamp."""

        # A list to collect due reminders.
        due: List[Reminder] = []

        #Fetch all reminders.
        reminders = self.reminder_repo.get_all()
        # Build a lookup table of schedules.
        schedules = {s.id: s for s in self.schedule_repo.get_all()}

        # Produce the current time in specified format for comparison with reminders.
        current_time_str = now.strftime("%H:%M")
        # "Mon", "Tue", etc.
        current_day = now.strftime("%a")  
        
        # Iterate through all reminders.
        for reminder in reminders:
            # Bypass reminders that are not active.
            if not reminder.enabled:
                continue
            
            # Lookup schedule for this reminder.
            schedule = schedules.get(reminder.scheduled_id)
            # Ignore reminders that are inactive or missing schedules.
            if not schedule or not schedule.is_active:
                continue

            # Check date range
            if schedule.start_date > now.date():
                continue
            if schedule.end_date and schedule.end_date < now.date():
                continue

            # Check day of week
            if current_day not in schedule.days_of_week:
                continue

            # Check each scheduled time
            for t in schedule.times:
                scheduled_dt = datetime.combine(now.date(), t)

                # Apply reminder offset
                reminder_dt = scheduled_dt - timedelta(minutes=reminder.reminder_offset_minutes)
                
                # Compare scheduled reminder time with current timestamp.
                if reminder_dt.strftime("%H:%M") == current_time_str:
                    # Collect reminder that are ready to fire.
                    due.append(reminder)

        return due
