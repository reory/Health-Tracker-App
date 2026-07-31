from datetime import datetime, time, timedelta, timezone

from models.reminder_event import ReminderEvent
from models.schedule import Schedule
from services.reminders import ReminderService
from services.schedule_engine import ScheduleEngine

# -------------------------
# Fake domain objects
# -------------------------

class FakeReminder:
    def __init__(self, offset_minutes, enabled=True):
        self.reminder_offset_minutes = offset_minutes
        self.enabled = enabled


class FakeIntakeLog:
    def __init__(self, scheduled_time):
        self.scheduled_time = scheduled_time


# -------------------------
# Fake repositories
# -------------------------

class FakeMedicationRepo:
    def __init__(self, meds):
        self._meds = meds

    def get_all(self):
        return self._meds


class FakeScheduleRepo:
    def __init__(self, schedules):
        self._schedules = schedules

    def get_all(self):
        return self._schedules

    def get_by_medication(self, med_id):
        return [s for s in self._schedules if s.medication_id == med_id]


class FakeReminderRepo:
    def __init__(self, reminders_by_schedule):
        self._data = reminders_by_schedule

    def get_by_schedule(self, schedule_id):
        return self._data.get(schedule_id, [])


class FakeIntakeRepo:
    def __init__(self, logs_by_med):
        self._data = logs_by_med

    def get_by_medication(self, med_id):
        return self._data.get(med_id, [])


# -------------------------
# Tests
# -------------------------

def test_generate_events_creates_reminder_event():
    now = datetime.now(timezone.utc)
    scheduled_time = (now + timedelta(hours=2)).time()
    today_utc = now.date()

    schedule = Schedule(
        id="sched1",
        medication_id="med1",
        times=[scheduled_time],
        start_date=today_utc,
        end_date=today_utc
    )

    reminder = FakeReminder(offset_minutes=30)

    service = ReminderService(
        medication_repo=FakeMedicationRepo([]),
        schedule_repo=FakeScheduleRepo([schedule]),
        intake_repo=FakeIntakeRepo({}),
        reminder_repo=FakeReminderRepo({"sched1": [reminder]}),
        schedule_engine=ScheduleEngine(None, None)
    )

    events = service.generate_events()

    assert len(events) == 1
    event = events[0]

    assert isinstance(event, ReminderEvent)
    assert event.reminder_time < event.schedule_time
    assert event.is_taken is False


def test_disabled_reminder_is_skipped():
    today_utc = datetime.now(timezone.utc).date()
    schedule = Schedule(
        id="sched1",
        medication_id="med1",
        times=[time(9, 0)],
        start_date=today_utc,
        end_date=today_utc
    )

    reminder = FakeReminder(offset_minutes=15, enabled=False)

    service = ReminderService(
        medication_repo=FakeMedicationRepo([]),
        schedule_repo=FakeScheduleRepo([schedule]),
        intake_repo=FakeIntakeRepo({}),
        reminder_repo=FakeReminderRepo({"sched1": [reminder]}),
        schedule_engine=ScheduleEngine(None, None)
    )

    assert service.generate_events() == []


def test_taken_dose_is_marked_taken():
    today_utc = datetime.now(timezone.utc).date()
    scheduled_dt = datetime.combine(today_utc, time(8, 0), tzinfo=timezone.utc)

    schedule = Schedule(
        id="sched1",
        medication_id="med1",
        times=[time(8, 0)],
        start_date=today_utc,
        end_date=today_utc
    )

    reminder = FakeReminder(offset_minutes=10)
    intake_log = FakeIntakeLog(scheduled_dt)

    service = ReminderService(
        medication_repo=FakeMedicationRepo([]),
        schedule_repo=FakeScheduleRepo([schedule]),
        intake_repo=FakeIntakeRepo({"med1": [intake_log]}),
        reminder_repo=FakeReminderRepo({"sched1": [reminder]}),
        schedule_engine=ScheduleEngine(None, None)
    )

    event = service.generate_events()[0]
    assert event.is_taken is True
    assert event.is_overdue is False


def test_get_overdue_returns_only_overdue():
    now_utc = datetime.now(timezone.utc)
    past_time = (now_utc - timedelta(hours=2)).time()
    today_utc = now_utc.date()

    schedule = Schedule(
        id="sched1",
        medication_id="med1",
        times=[past_time],
        start_date=today_utc,
        end_date=today_utc
    )

    reminder = FakeReminder(offset_minutes=5)

    service = ReminderService(
        medication_repo=FakeMedicationRepo([]),
        schedule_repo=FakeScheduleRepo([schedule]),
        intake_repo=FakeIntakeRepo({}),
        reminder_repo=FakeReminderRepo({"sched1": [reminder]}),
        schedule_engine=ScheduleEngine(None, None)
    )

    overdue = service.get_overdue()
    assert len(overdue) == 1
    assert overdue[0].is_overdue is True


def test_get_next_for_medication_returns_earliest():
    now = datetime.now(timezone.utc)

    s1 = Schedule(
        id="s1",
        medication_id="med1",
        times=[(now + timedelta(hours=3)).time()],
        start_date=now.date(),
        end_date=now.date()
    )

    s2 = Schedule(
        id="s2",
        medication_id="med1",
        times=[(now + timedelta(hours=1)).time()],
        start_date=now.date(),
        end_date=now.date()
    )

    reminder = FakeReminder(offset_minutes=10)

    service = ReminderService(
        medication_repo=FakeMedicationRepo([]),
        schedule_repo=FakeScheduleRepo([s1, s2]),
        intake_repo=FakeIntakeRepo({}),
        reminder_repo=FakeReminderRepo({
            "s1": [reminder],
            "s2": [reminder]
        }),
        schedule_engine=ScheduleEngine(None, None)
    )

    next_event = service.get_next_for_medication("med1")
    assert next_event is not None
    assert next_event.schedule_time.time() == s2.times[0]