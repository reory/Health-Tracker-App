from datetime import datetime, timedelta, timezone

# Import Data.
from data.medication_repository import MedicationRepository
from data.schedule_repository import ScheduleRepository
from models.medication import Medication

# Import Models.
from models.schedule import Schedule


class ScheduleEngine:
    """Core logic layer for generating dosages, calculating next dosages,
    detecting overdue doses and providing a timeline data for the UI."""

    def __init__(
        self, medication_repo: MedicationRepository, schedule_repo: ScheduleRepository
    ):
        """Provides access to medication and schedule storage layers."""

        self.medication_repo = medication_repo
        self.schedule_repo = schedule_repo

    def generate_dose_events(self, schedule: Schedule) -> list[datetime]:
        """
        Generate all dose times between start_date and end_date.
        supports frequencies: Daily or specific times per day.
        """

        if schedule.end_date is None:
            return []

        dose_times = []

        current = schedule.start_date
        end = schedule.end_date

        while current <= end:
            for dt in schedule.times:
                # Ensure combined datetime explicitly includes UTC timezone
                dose_dt = datetime.combine(current, dt, tzinfo=timezone.utc)
                dose_times.append(dose_dt)
            current += timedelta(days=1)

        return sorted(dose_times)

    def get_next_dose(self, medication_id: int) -> datetime | None:
        """Returns the next upcoming dose datetime for a given medication."""

        schedules = self.schedule_repo.get_by_medication(str(medication_id))
        now = datetime.now(timezone.utc)

        upcoming = []

        for schedule in schedules:
            dose_times = self.generate_dose_events(schedule)
            for dt in dose_times:
                if dt > now:
                    upcoming.append(dt)

        return min(upcoming) if upcoming else None

    def get_today_schedule(self) -> list[tuple[Medication, datetime]]:
        """Returns a list of all doses scheduled for today."""

        today = datetime.now(timezone.utc).date()
        results = []

        medications = self.medication_repo.get_all()

        for med in medications:
            # Skip medications that have not been saved yet.
            if med.id is None:
                continue

            schedules = self.schedule_repo.get_by_medication(med.id)
            for schedule in schedules:
                dose_times = self.generate_dose_events(schedule)
                for dt in dose_times:
                    if dt.date() == today:
                        results.append((med, dt))

        return sorted(results, key=lambda x: x[1])

    def get_overdue_doses(self) -> list[tuple]:
        """Returns a list of doses that should have occurred already."""

        now = datetime.now(timezone.utc)
        results = []

        medications = self.medication_repo.get_all()

        for med in medications:
            if med.id is None:
                continue

            schedules = self.schedule_repo.get_by_medication(med.id)
            for schedule in schedules:
                dose_events = self.generate_dose_events(schedule)
                for dt in dose_events:
                    if dt < now:
                        results.append((med, dt))

        return results