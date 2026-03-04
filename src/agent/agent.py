from __future__ import annotations
from datetime import datetime

import logging

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModelSettings
from pydantic_ai.output import DeferredToolRequests
from pydantic_ai.exceptions import CallDeferred

from src.agent.prompts import SYSTEM_PROMPT
from src.tools.accommodation import AccommodationType, Accommodation, find_accommodation as _find_accommodation
from src.tools.budget import BudgetResult, estimate_budget as _estimate_budget
from src.tools.elevation import ElevationResult, get_elevation_profile as _get_elevation_profile
from src.tools.poi import POICategory, PointOfInterest, get_points_of_interest as _get_points_of_interest
from src.tools.route import RouteResult, geocode as _geocode, get_route as _get_route
from src.tools.visa import VisaResult, check_visa_requirements as _check_visa_requirements
from src.tools.weather import WeatherResult, get_weather as _get_weather

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

agent: Agent[None, str | DeferredToolRequests] = Agent(
    model="anthropic:claude-sonnet-4-6",
    model_settings=AnthropicModelSettings(anthropic_thinking={"type": "adaptive"}),
    system_prompt=f"{SYSTEM_PROMPT}\n\nToday's date is {datetime.now().strftime('%d %B %Y')}",
    output_type=[str, DeferredToolRequests],
)

# plain tools do not take in agent context
@agent.tool_plain
def ask_user(question: str, options: list[str] | None = None) -> str:
    """Ask the user a question. Use options for multiple choice (e.g. accommodation type, daily distance range), omit for free text (e.g. dates, place names). The user's answer will be returned as the tool result."""
    raise CallDeferred(metadata={"question": question, "options": options or []})


@agent.tool_plain
def geocode(place_name: str) -> dict:
    logger.info(f"Geocoding {place_name}")
    """Convert a place name (e.g. city, address) to longitude and latitude coordinates. Returns {'lon': float, 'lat': float} or {'error': str} if not found."""
    result = _geocode(place_name)
    if result is None:
        return {"error": f"Could not find coordinates for '{place_name}'"}
    return {"lon": result[0], "lat": result[1]}


@agent.tool_plain
def get_route(
    start_lon: float,
    start_lat: float,
    end_lon: float,
    end_lat: float,
) -> RouteResult:
    logger.info(f"Getting route from {start_lon}, {start_lat} to {end_lon}, {end_lat}")
    """Get cycling route details between two coordinate points. Returns distance, estimated_days, and waypoint_names — place names along the actual route. Use waypoint_names for overnight stops, accommodation, and points of interest. Coordinates are in longitude, latitude order (e.g. Berlin: 13.4050, 52.5200)."""
    return _get_route((start_lon, start_lat), (end_lon, end_lat))


@agent.tool_plain
def get_elevation_profile(origin: str, destination: str) -> ElevationResult:
    logger.info(f"Getting elevation profile from {origin} to {destination}")
    """Get the elevation profile for a cycling route, including total ascent/descent and challenging sections."""
    return _get_elevation_profile(origin, destination)

@agent.tool_plain
def get_weather(location: str, month: str) -> WeatherResult:
    logger.info(f"Getting weather for {location} in {month}")
    """Get weather conditions and cycling suitability for a location in a given month."""
    return _get_weather(location, month)


@agent.tool_plain
def find_accommodation(location: str, type: AccommodationType) -> list[Accommodation]:
    logger.info(f"Finding accommodation for {location} of type {type}")
    """Find accommodation options at a location filtered by type (camping/hostel/hotel/guesthouse)."""
    return _find_accommodation(location, type)


@agent.tool_plain
def get_points_of_interest(location: str, category: POICategory) -> list[PointOfInterest]:
    logger.info(f"Getting points of interest for {location} of category {category}")
    """Find points of interest near the cycling route at a given location by category."""
    return _get_points_of_interest(location, category)


@agent.tool_plain
def check_visa_requirements(passport_country: str, destination_country: str) -> VisaResult:
    logger.info(f"Checking visa requirements for {passport_country} to {destination_country}")
    """Check visa and entry requirements for a given passport holder travelling to a destination country."""
    return _check_visa_requirements(passport_country, destination_country)


@agent.tool_plain
def estimate_budget(
    distance_km: float,
    days: int,
    accommodation_type: AccommodationType,
    country: str,
) -> BudgetResult:
    logger.info(f"Estimating budget for {distance_km}km over {days} days in {country} with {accommodation_type}")
    """Estimate the total trip budget including food, accommodation, and miscellaneous costs."""
    return _estimate_budget(distance_km, days, accommodation_type, country)
