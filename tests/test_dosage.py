import pytest
from models.dosage import Dosage


def test_dosage_str_without_form():
    d = Dosage(amount=500, unit="mg")
    assert str(d) == "500|mg"


def test_dosage_str_with_form():
    d = Dosage(amount=2.5, unit="ml", form="tablet")
    assert str(d) == "2.5|ml|tablet"


def test_from_string_without_form():
    d = Dosage.from_string("500|mg")

    assert isinstance(d, Dosage)
    assert d.amount == 500
    assert d.unit == "mg"
    assert d.form is None


def test_from_string_with_form():
    d = Dosage.from_string("2.5|ml|capsule")

    assert isinstance(d, Dosage)
    assert d.amount == 2.5
    assert d.unit == "ml"
    assert d.form == "capsule"


def test_from_string_empty_returns_none():
    assert Dosage.from_string("") is None
    assert Dosage.from_string(None) is None #type:ignore


def test_round_trip_serialization():
    original = Dosage(amount=137.5, unit="mg", form="tablet")
    s = str(original)
    restored = Dosage.from_string(s)

    assert restored.amount == original.amount #type:ignore
    assert restored.unit == original.unit #type:ignore
    assert restored.form == original.form #type:ignore
