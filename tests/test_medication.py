from models.medication import Medication
from models.schedule import Schedule
from datetime import time


def test_medication_inherits_base_model():
    m = Medication()

    # BaseModel fields should exist
    assert hasattr(m, "created_at")
    assert hasattr(m, "updated_at")
    assert hasattr(m, "to_dict")


def test_medication_defaults():
    m = Medication()

    assert m.id == ""
    assert m.name == ""
    assert m.description == ""
    assert m.dosage == ""
    assert m.schedule == []
    assert m.is_active is True
    assert m.notes == ""


def test_medication_schedule_is_independent_list():
    m1 = Medication()
    m2 = Medication()

    s = Schedule(times=[time(8, 0)])
    m1.schedule.append(s)

    assert m2.schedule == []


def test_medication_accepts_schedule_objects():
    s1 = Schedule(times=[time(9, 0)])
    s2 = Schedule(times=[time(21, 0)])

    m = Medication(schedule=[s1, s2])

    assert len(m.schedule) == 2
    assert m.schedule[0] is s1
    assert m.schedule[1] is s2


def test_medication_can_be_archived():
    m = Medication(is_active=False)

    assert m.is_active is False


def test_medication_notes_field():
    m = Medication(notes="Take with food")

    assert m.notes == "Take with food"
