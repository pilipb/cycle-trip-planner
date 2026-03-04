from __future__ import annotations

import pytest

from src.tools.accommodation import Accommodation, find_accommodation


def test_known_location_camping():
    results = find_accommodation("Berlin", "camping")
    assert len(results) > 0
    acc = results[0]
    assert isinstance(acc, Accommodation)
    assert acc.type == "camping"
    assert acc.cycling_friendly is True
    assert acc.price_per_night_eur > 0


def test_known_location_hostel():
    results = find_accommodation("Prague", "hostel")
    assert len(results) > 0
    assert all(a.type == "hostel" for a in results)


def test_known_location_hotel():
    results = find_accommodation("Amsterdam", "hotel")
    assert len(results) > 0
    assert all(a.type == "hotel" for a in results)


def test_known_location_guesthouse():
    results = find_accommodation("Vienna", "guesthouse")
    assert len(results) > 0
    assert all(a.type == "guesthouse" for a in results)


def test_case_insensitive_lookup():
    results_lower = find_accommodation("berlin", "hostel")
    results_upper = find_accommodation("BERLIN", "hostel")
    assert len(results_lower) == len(results_upper)
    assert results_lower[0].name == results_upper[0].name


def test_unknown_location_returns_fallback():
    results = find_accommodation("Atlantis", "hostel")
    assert len(results) > 0
    acc = results[0]
    assert acc.type == "hostel"
    assert acc.price_per_night_eur > 0
    assert "Atlantis" in acc.location or "atlantis" in acc.location.lower()


@pytest.mark.parametrize("acc_type", ["camping", "hostel", "hotel", "guesthouse"])
def test_all_types_return_results(acc_type):
    results = find_accommodation("Munich", acc_type)
    assert len(results) > 0
    assert results[0].type == acc_type


def test_accommodation_has_all_fields():
    results = find_accommodation("Budapest", "hostel")
    acc = results[0]
    assert acc.name
    assert acc.location
    assert isinstance(acc.amenities, list)
    assert acc.rating > 0
    assert acc.notes
