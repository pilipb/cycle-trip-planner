from __future__ import annotations

import pytest

from src.tools.weather import WeatherResult, get_weather


def test_known_location_and_month():
    result = get_weather("Berlin", "September")
    assert isinstance(result, WeatherResult)
    assert result.location == "Berlin"
    assert result.month == "September"
    assert result.cycling_suitability == "excellent"
    assert result.avg_temp_celsius > 0


def test_case_insensitive_month():
    result_lower = get_weather("Berlin", "september")
    result_upper = get_weather("Berlin", "SEPTEMBER")
    assert result_lower.avg_temp_celsius == result_upper.avg_temp_celsius


def test_month_abbreviation():
    result = get_weather("Prague", "Sep")
    assert result.month == "September"


def test_winter_month_is_challenging():
    result = get_weather("Berlin", "January")
    assert result.cycling_suitability == "challenging"
    assert result.avg_temp_celsius < 5


def test_summer_month_is_excellent():
    result = get_weather("Vienna", "July")
    assert result.cycling_suitability == "excellent"
    assert result.avg_temp_celsius > 20


def test_unknown_location_returns_fallback():
    result = get_weather("Timbuktu", "June")
    assert isinstance(result, WeatherResult)
    assert result.avg_temp_celsius > 0
    assert result.cycling_suitability in {"excellent", "good", "fair", "challenging"}


def test_lisbon_dry_summer():
    result = get_weather("Lisbon", "July")
    assert result.rainfall_mm < 10
    assert result.cycling_suitability in {"excellent", "good"}


@pytest.mark.parametrize("month", [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
])
def test_all_months_for_berlin(month):
    result = get_weather("Berlin", month)
    assert isinstance(result, WeatherResult)
    assert result.sunny_days >= 0
    assert result.rainfall_mm >= 0


def test_weather_result_has_all_fields():
    result = get_weather("Amsterdam", "May")
    assert result.min_temp_celsius <= result.avg_temp_celsius <= result.max_temp_celsius
    assert result.sunny_days > 0
    assert result.wind_speed_kmh > 0
    assert result.conditions
