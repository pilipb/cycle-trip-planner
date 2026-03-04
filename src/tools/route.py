from __future__ import annotations

import math
import os
from contextvars import ContextVar
from typing import Literal

import httpx
from pydantic import BaseModel


class RouteResult(BaseModel):
    origin: str
    destination: str
    distance_km: float
    estimated_days: int
    waypoints: list[str]
    waypoint_names: list[str]
    surface: str
    route_type: str
    description: str
    status: Literal["found", "estimated"]

# GeoJSON stored here for frontend; never sent to the model (would exceed token limit).
# Keyed by session_id from _session_id_ctx.
_route_geojson_store: dict[str, dict] = {}
_session_id_ctx: ContextVar[str | None] = ContextVar("session_id", default=None)

ORS_BASE_URL = "https://api.openrouteservice.org"
PROFILE = "cycling-regular"
DEFAULT_KM_PER_DAY = 80


def geocode(place_name: str) -> tuple[float, float] | None:
    """Convert a place name to (longitude, latitude) using OpenRouteService Geocode API."""
    api_key = os.environ.get("OPENROUTE_SERVICE_API_KEY")
    if not api_key:
        return None
    try:
        with httpx.Client(timeout=10.0) as client:
            r = client.get(
                f"{ORS_BASE_URL}/geocode/search",
                params={"text": place_name, "size": 1},
                headers={"Authorization": api_key},
            )
            r.raise_for_status()
            data = r.json()
    except (httpx.HTTPError, KeyError):
        return None
    features = data.get("features", [])
    if not features:
        return None
    coords = features[0].get("geometry", {}).get("coordinates")
    if not coords or len(coords) < 2:
        return None
    return (float(coords[0]), float(coords[1]))


def _format_coords(lon: float, lat: float) -> str:
    return f"{lat:.5f},{lon:.5f}"


def _reverse_geocode(lon: float, lat: float) -> str | None:
    """Convert coordinates to a place name using OpenRouteService reverse geocode."""
    api_key = os.environ.get("OPENROUTE_SERVICE_API_KEY")
    if not api_key:
        return None
    try:
        with httpx.Client(timeout=5.0) as client:
            r = client.get(
                f"{ORS_BASE_URL}/geocode/reverse",
                params={"point.lon": lon, "point.lat": lat, "size": 1},
                headers={"Authorization": api_key},
            )
            r.raise_for_status()
            data = r.json()
    except (httpx.HTTPError, KeyError):
        return None
    features = data.get("features", [])
    if not features:
        return None
    props = features[0].get("properties", {})
    return props.get("label") or props.get("name") or props.get("locality")


def _sample_waypoints(coordinates: list[list[float]], max_waypoints: int = 10) -> list[str]:
    """Sample intermediate coordinates from the route geometry as waypoint strings."""
    if len(coordinates) <= 2:
        return []
    # Exclude first and last (start/end), sample evenly
    inner = coordinates[1:-1]
    if not inner:
        return []
    step = max(1, len(inner) // max_waypoints)
    sampled = inner[::step][:max_waypoints]
    return [_format_coords(lon, lat) for lon, lat in sampled]


def get_route(
    start_coords: tuple[float, float],
    end_coords: tuple[float, float],
) -> RouteResult:
    """Get cycling route details between two coordinate points using OpenRouteService.

    Coordinates are in (longitude, latitude) order (GeoJSON standard).
    """
    api_key = os.environ.get("OPENROUTE_SERVICE_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTE_SERVICE_API_KEY environment variable is required. "
            "Get a free API key at https://openrouteservice.org/dev/#/signup"
        )

    coords = [
        [start_coords[0], start_coords[1]],
        [end_coords[0], end_coords[1]],
    ]
    url = f"{ORS_BASE_URL}/v2/directions/{PROFILE}/geojson"

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                url,
                json={"coordinates": coords},
                headers={"Authorization": api_key},
            )
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404 or (
            e.response.status_code == 400
            and "No route found" in (e.response.text or "")
        ):
            return _estimated_fallback(start_coords, end_coords)
        raise
    except httpx.RequestError:
        return _estimated_fallback(start_coords, end_coords)

    features = data.get("features", [])
    if not features:
        return _estimated_fallback(start_coords, end_coords)

    feature = features[0]
    props = feature.get("properties", {})
    summary = props.get("summary", {})
    distance_m = summary.get("distance", 0)
    duration_s = summary.get("duration", 0)
    distance_km = distance_m / 1000
    estimated_days = max(1, round(distance_km / DEFAULT_KM_PER_DAY))

    coordinates = feature.get("geometry", {}).get("coordinates", [])
    waypoints = _sample_waypoints(coordinates)

    # Reverse geocode waypoints to place names for stop recommendations
    waypoint_names: list[str] = []
    for wp in waypoints:
        parts = wp.split(",")
        if len(parts) == 2:
            try:
                lat, lon = float(parts[0]), float(parts[1])  # format is "lat,lon"
                name = _reverse_geocode(lon, lat)
                waypoint_names.append(name or wp)
            except ValueError:
                waypoint_names.append(wp)
        else:
            waypoint_names.append(wp)

    # Store GeoJSON for frontend only; do not include in result (avoids token limit)
    session_id = _session_id_ctx.get()
    if session_id:
        _route_geojson_store[session_id] = data

    return RouteResult(
        origin=_format_coords(start_coords[0], start_coords[1]),
        destination=_format_coords(end_coords[0], end_coords[1]),
        distance_km=round(distance_km, 2),
        estimated_days=estimated_days,
        waypoints=waypoints,
        waypoint_names=waypoint_names,
        surface="Cycle route (cycling-regular profile)",
        route_type="OpenRouteService cycling route",
        description=(
            f"Cycling route from start to end. "
            f"Distance: {distance_km:.1f} km, estimated duration: {duration_s / 3600:.1f} hours."
        ),
        status="found",
    )


def _estimated_fallback(
    start_coords: tuple[float, float],
    end_coords: tuple[float, float],
) -> RouteResult:
    """Return an estimated result when the API cannot find a route."""
    lon1, lat1 = start_coords
    lon2, lat2 = end_coords
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = R * c
    estimated_days = max(1, round(distance_km / DEFAULT_KM_PER_DAY))

    return RouteResult(
        origin=_format_coords(lon1, lat1),
        destination=_format_coords(lon2, lat2),
        distance_km=round(distance_km, 2),
        estimated_days=estimated_days,
        waypoints=[],
        waypoint_names=[],
        surface="Mixed terrain, conditions unknown",
        route_type="Estimated route (no cycling route found)",
        description=(
            "No cycling route could be calculated. This is an estimated straight-line distance. "
            "Check local cycling maps or apps like Komoot for detailed planning."
        ),
        status="estimated",
    )
