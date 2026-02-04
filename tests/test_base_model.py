import pytest
from datetime import datetime, timezone
from models.base import BaseModel
import uuid
import time


def test_base_model_generates_unique_id():
    m1 = BaseModel()
    m2 = BaseModel()

    # IDs should be strings and valid UUIDs
    assert isinstance(m1.id, str)
    assert isinstance(uuid.UUID(m1.id), uuid.UUID)

    assert m1.id != m2.id


def test_base_model_has_valid_timestamps():
    m = BaseModel()

    assert isinstance(m.created_at, datetime)
    assert isinstance(m.updated_at, datetime)

    # Both should be timezone-aware and in UTC
    assert m.created_at.tzinfo == timezone.utc
    assert m.updated_at.tzinfo == timezone.utc


def test_to_dict_serializes_datetimes_to_iso():
    m = BaseModel()
    data = m.to_dict()

    assert isinstance(data["created_at"], str)
    assert isinstance(data["updated_at"], str)

    # ISO format check
    datetime.fromisoformat(data["created_at"])
    datetime.fromisoformat(data["updated_at"])


def test_from_dict_restores_datetime_objects():
    m = BaseModel()
    data = m.to_dict()

    restored = BaseModel.from_dict(data)

    assert isinstance(restored.created_at, datetime)
    assert isinstance(restored.updated_at, datetime)
    assert restored.created_at == m.created_at
    assert restored.updated_at == m.updated_at
    assert restored.id == m.id


def test_mark_updated_changes_timestamp():
    m = BaseModel()
    old_timestamp = m.updated_at

    time.sleep(0.01)  # ensure measurable difference
    m.mark_updated()

    assert m.updated_at > old_timestamp
    assert m.updated_at.tzinfo == timezone.utc
