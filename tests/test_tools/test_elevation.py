from __future__ import annotations

import pytest

from src.tools.elevation import ElevationResult, get_elevation_profile


def test_known_route_berlin_prague():
    result = get_elevation_profile("Berlin", "Prague")
    assert isinstance(result, ElevationResult)
    assert result.status == "found"
    assert result.total_ascent_m > 0
    assert result.total_descent_m > 0
    assert result.max_elevation_m > result.min_elevation_m


def test_flat_route_amsterdam_berlin():
    result = get_elevation_profile("Berlin", "Amsterdam")
    assert result.status == "found"
    assert result.max_elevation_m < 200  # flat route
    assert result.total_ascent_m < 1500


def test_challenging_route_florence_rome():
    result = get_elevation_profile("Florence", "Rome")
    assert result.status == "found"
    assert result.total_ascent_m > 4000  # Tuscany is hilly
    assert len(result.challenging_sections) > 0


def test_reverse_route_swaps_ascent_descent():
    forward = get_elevation_profile("Berlin", "Prague")
    reverse = get_elevation_profile("Prague", "Berlin")
    assert forward.status == "found"
    assert reverse.status == "found"
    # Ascent and descent swap when direction reverses
    assert forward.total_ascent_m == reverse.total_descent_m
    assert forward.total_descent_m == reverse.total_ascent_m


def test_unknown_route_returns_estimate():
    result = get_elevation_profile("Timbuktu", "Shangri-La")
    assert isinstance(result, ElevationResult)
    assert result.status == "estimated"
    assert result.total_ascent_m > 0
    assert len(result.challenging_sections) > 0


def test_danube_is_very_flat():
    result = get_elevation_profile("Vienna", "Budapest")
    assert result.status == "found"
    assert result.total_ascent_m < 1000
    assert result.max_elevation_m < 400


def test_elevation_result_fields():
    result = get_elevation_profile("Munich", "Vienna")
    assert result.profile_description
    assert isinstance(result.challenging_sections, list)
    assert result.origin
    assert result.destination
