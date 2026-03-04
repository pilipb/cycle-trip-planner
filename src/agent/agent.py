from __future__ import annotations
from datetime import datetime

from pydantic_ai import Agent

from src.agent.prompts import SYSTEM_PROMPT
from src.tools.accommodation import AccommodationType, Accommodation, find_accommodation as _find_accommodation
from src.tools.budget import BudgetResult, estimate_budget as _estimate_budget
from src.tools.elevation import ElevationResult, get_elevation_profile as _get_elevation_profile
from src.tools.poi import POICategory, PointOfInterest, get_points_of_interest as _get_points_of_interest
from src.tools.route import RouteResult, get_route as _get_route
from src.tools.visa import VisaResult, check_visa_requirements as _check_visa_requirements
from src.tools.weather import WeatherResult, get_weather as _get_weather

agent: Agent[None, str] = Agent(
    model="anthropic:claude-sonnet-4-6",
    system_prompt=f"{SYSTEM_PROMPT}\n\nToday's date is {datetime.now().strftime('%d %B %Y')}",
)

# plain tools do not take in agent context
@agent.tool_plain
def get_route(origin: str, destination: str) -> RouteResult:
    """Get cycling route details between two locations, including distance, waypoints, and surface type."""
    return _get_route(origin, destination)


@agent.tool_plain
def get_elevation_profile(origin: str, destination: str) -> ElevationResult:
    """Get the elevation profile for a cycling route, including total ascent/descent and challenging sections."""
    return _get_elevation_profile(origin, destination)

@agent.tool_plain
def get_weather(location: str, month: str) -> WeatherResult:
    """Get weather conditions and cycling suitability for a location in a given month."""
    return _get_weather(location, month)


@agent.tool_plain
def find_accommodation(location: str, type: AccommodationType) -> list[Accommodation]:
    """Find accommodation options at a location filtered by type (camping/hostel/hotel/guesthouse)."""
    return _find_accommodation(location, type)


@agent.tool_plain
def get_points_of_interest(location: str, category: POICategory) -> list[PointOfInterest]:
    """Find points of interest near the cycling route at a given location by category."""
    return _get_points_of_interest(location, category)


@agent.tool_plain
def check_visa_requirements(passport_country: str, destination_country: str) -> VisaResult:
    """Check visa and entry requirements for a given passport holder travelling to a destination country."""
    return _check_visa_requirements(passport_country, destination_country)


@agent.tool_plain
def estimate_budget(
    distance_km: float,
    days: int,
    accommodation_type: AccommodationType,
    country: str,
) -> BudgetResult:
    """Estimate the total trip budget including food, accommodation, and miscellaneous costs."""
    return _estimate_budget(distance_km, days, accommodation_type, country)
