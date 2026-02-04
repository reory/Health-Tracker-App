import uuid
from datetime import date, time, datetime
from models.schedule import Schedule


def test_schedule_generates_unique_id():
    s1 = Schedule()
    s2 = Schedule()

    assert isinstance(s1.id, str)
    assert isinstance(uuid.UUID(s1.id), uuid.UUID)
    assert s1.id != s2.id


def test_schedule_defaults():
    s = Schedule()

    assert s.medication_id == ""
    assert s.frequency == "daily"
    assert s.days_of_week == []
    assert s.times == []
    assert s.is_active is True
    assert s.end_date is None


def test_schedule_times_are_independent_lists():
    s1 = Schedule()
    s2 = Schedule()

    s1.times.append(time(8, 0))

    assert s2.times == []


def test_schedule_days_of_week_are_independent_lists():
    s1 = Schedule()
    s2 = Schedule()

    s1.days_of_week.append(0)

    assert s2.days_of_week == []


def test_schedule_accepts_times_and_days():
    t1 = time(9, 0)
    t2 = time(21, 30)

    s = Schedule(
        times=[t1, t2],
        days_of_week=[0, 2, 4]
    )

    assert s.times == [t1, t2]
    assert s.days_of_week == [0, 2, 4]


def test_schedule_start_and_end_dates():
    start = date(2025, 1, 1)
    end = date(2025, 12, 31)

    s = Schedule(start_date=start, end_date=end)

    assert s.start_date == start
    assert s.end_date == end


def test_schedule_created_at_timestamp():
    s = Schedule()

    assert isinstance(s.created_at, datetime)
