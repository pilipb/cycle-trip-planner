from __future__ import annotations

import pytest

from src.tools.route import RouteResult, get_route


def test_known_route_berlin_prague():
    result = get_route("Berlin", "Prague")
    assert isinstance(result, RouteResult)
    assert result.status == "found"
    assert result.origin == "Berlin"
    assert result.destination == "Prague"
    assert result.distance_km == pytest.approx(350.0)
    assert result.estimated_days == 4
    assert "Dresden" in result.waypoints
    assert len(result.waypoints) > 0


def test_known_route_case_insensitive():
    result = get_route("berlin", "prague")
    assert result.status == "found"
    assert result.distance_km > 0


def test_known_route_munich_vienna():
    result = get_route("Munich", "Vienna")
    assert result.status == "found"
    assert result.distance_km > 0
    assert "Salzburg" in result.waypoints


def test_reverse_route():
    forward = get_route("Vienna", "Budapest")
    reverse = get_route("Budapest", "Vienna")
    assert forward.status == "found"
    assert reverse.status == "found"
    # Same distance, reversed waypoints
    assert forward.distance_km == reverse.distance_km
    assert forward.waypoints == list(reversed(reverse.waypoints))


def test_unknown_route_returns_estimate():
    result = get_route("Timbuktu", "Shangri-La")
    assert isinstance(result, RouteResult)
    assert result.status == "estimated"
    assert result.distance_km > 0
    assert result.estimated_days >= 1


def test_result_fields_are_populated():
    result = get_route("Amsterdam", "Paris")
    assert result.surface
    assert result.route_type
    assert result.description
    assert result.estimated_days >= 1


def test_danube_route():
    result = get_route("Vienna", "Budapest")
    assert result.status == "found"
    assert result.distance_km == pytest.approx(280.0)
