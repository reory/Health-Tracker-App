from datetime import datetime, time, timedelta, timezone

from models.medication import Medication
from models.schedule import Schedule
from services.schedule_engine import ScheduleEngine


# Fake repositories
class FakeMedicationRepo:
    def __init__(self, medications):
        self._medications = medications

    def get_all(self):
        return self._medications


class FakeScheduleRepo:
    def __init__(self, schedules_by_med_id):
        self._data = schedules_by_med_id

    def get_by_medication(self, med_id):
        return self._data.get(med_id, [])


# Tests
def test_generate_dose_events_basic():
    today_utc = datetime.now(timezone.utc).date()
    schedule = Schedule(
        times=[time(8, 0), time(20, 0)],
        start_date=today_utc,
        end_date=today_utc
    )

    engine = ScheduleEngine(None, None)
    events = engine.generate_dose_events(schedule)

    assert len(events) == 2
    assert events[0].time() == time(8, 0)
    assert events[1].time() == time(20, 0)


def test_generate_dose_events_no_end_date():
    today_utc = datetime.now(timezone.utc).date()
    schedule = Schedule(
        times=[time(9, 0)],
        start_date=today_utc,
        end_date=None
    )

    engine = ScheduleEngine(None, None)
    events = engine.generate_dose_events(schedule)

    assert events == []


def test_get_next_dose_returns_future_dose():
    now_utc = datetime.now(timezone.utc)
    later_today = (now_utc + timedelta(hours=2)).time()
    today_utc = now_utc.date()

    schedule = Schedule(
        times=[later_today],
        start_date=today_utc,
        end_date=today_utc
    )

    med = Medication(id="1", name="TestMed")

    med_repo = FakeMedicationRepo([med])
    sched_repo = FakeScheduleRepo({"1": [schedule]})

    engine = ScheduleEngine(med_repo, sched_repo)
    next_dose = engine.get_next_dose("1")

    assert next_dose is not None
    assert next_dose > now_utc


def test_get_next_dose_returns_none_if_no_future():
    now_utc = datetime.now(timezone.utc)
    past_time = (now_utc - timedelta(hours=2)).time()
    today_utc = now_utc.date()

    schedule = Schedule(
        times=[past_time],
        start_date=today_utc,
        end_date=today_utc
    )

    med = Medication(id="1")

    med_repo = FakeMedicationRepo([med])
    sched_repo = FakeScheduleRepo({"1": [schedule]})

    engine = ScheduleEngine(med_repo, sched_repo)

    assert engine.get_next_dose("1") is None


def test_get_today_schedule_returns_sorted_results():
    today_utc = datetime.now(timezone.utc).date()

    s1 = Schedule(times=[time(20, 0)], start_date=today_utc, end_date=today_utc)
    s2 = Schedule(times=[time(8, 0)], start_date=today_utc, end_date=today_utc)

    med = Medication(id="1", name="TestMed")

    med_repo = FakeMedicationRepo([med])
    sched_repo = FakeScheduleRepo({"1": [s1, s2]})

    engine = ScheduleEngine(med_repo, sched_repo)
    results = engine.get_today_schedule()

    assert len(results) == 2
    assert results[0][1].time() == time(8, 0)
    assert results[1][1].time() == time(20, 0)


def test_get_overdue_doses_returns_past_only():
    now_utc = datetime.now(timezone.utc)
    past_time = (now_utc - timedelta(hours=3)).time()
    future_time = (now_utc + timedelta(hours=3)).time()
    today_utc = now_utc.date()

    schedule = Schedule(
        times=[past_time, future_time],
        start_date=today_utc,
        end_date=today_utc
    )

    med = Medication(id="1")

    med_repo = FakeMedicationRepo([med])
    sched_repo = FakeScheduleRepo({"1": [schedule]})

    engine = ScheduleEngine(med_repo, sched_repo)
    overdue = engine.get_overdue_doses()

    assert len(overdue) == 1
    assert overdue[0][1] < now_utc