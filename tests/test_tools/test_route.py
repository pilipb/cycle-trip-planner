from __future__ import annotations

import pytest
from unittest.mock import patch, MagicMock

from src.tools.route import RouteResult, get_route, geocode


# Berlin (13.4050, 52.5200) -> Prague (14.4378, 50.0755)
BERLIN = (13.4050, 52.5200)
PRAGUE = (14.4378, 50.0755)
MUNICH = (11.5761, 48.1374)
VIENNA = (16.3738, 48.2082)
BUDAPEST = (19.0402, 47.4979)


def _mock_ors_response(distance_m: float = 350000, duration_s: float = 50400):
    """Create a mock OpenRouteService GeoJSON response."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [13.4050, 52.5200],
                        [13.5, 52.0],
                        [14.0, 51.0],
                        [14.4378, 50.0755],
                    ],
                },
                "properties": {
                    "summary": {"distance": distance_m, "duration": duration_s},
                },
            }
        ],
    }


@patch("src.tools.route._reverse_geocode", return_value=None)
@patch("src.tools.route.httpx.Client")
def test_route_returns_found(mock_client_class, _mock_reverse_geocode):
    mock_response = MagicMock()
    mock_response.json.return_value = _mock_ors_response(350000, 50400)
    mock_response.raise_for_status = MagicMock()
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = mock_response
    mock_client_class.return_value = mock_client

    with patch.dict("os.environ", {"OPENROUTE_SERVICE_API_KEY": "test-key"}):
        result = get_route(BERLIN, PRAGUE)

    assert isinstance(result, RouteResult)
    assert result.status == "found"
    assert result.origin == "52.52000,13.40500"
    assert result.destination == "50.07550,14.43780"
    assert result.distance_km == pytest.approx(350.0)
    assert result.estimated_days == 4
    assert len(result.waypoints) > 0
    assert len(result.waypoint_names) == len(result.waypoints)
    assert result.surface
    assert result.route_type
    assert result.description


@patch("src.tools.route._reverse_geocode", return_value=None)
@patch("src.tools.route.httpx.Client")
def test_route_reverse_same_distance(mock_client_class, _mock_reverse_geocode):
    mock_response = MagicMock()
    mock_response.json.return_value = _mock_ors_response(280000, 40320)
    mock_response.raise_for_status = MagicMock()
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = mock_response
    mock_client_class.return_value = mock_client

    with patch.dict("os.environ", {"OPENROUTE_SERVICE_API_KEY": "test-key"}):
        forward = get_route(VIENNA, BUDAPEST)
        reverse = get_route(BUDAPEST, VIENNA)

    assert forward.status == "found"
    assert reverse.status == "found"
    assert forward.distance_km == reverse.distance_km


def test_route_missing_api_key():
    with pytest.raises(ValueError, match="OPENROUTE_SERVICE_API_KEY"):
        with patch.dict("os.environ", {}, clear=True):
            get_route(BERLIN, PRAGUE)


@patch("src.tools.route.httpx.Client")
def test_route_api_error_returns_estimated(mock_client_class):
    import httpx
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.side_effect = httpx.HTTPStatusError(
        "No route", request=MagicMock(), response=MagicMock(status_code=404)
    )
    mock_client_class.return_value = mock_client

    with patch.dict("os.environ", {"OPENROUTE_SERVICE_API_KEY": "test-key"}):
        result = get_route(BERLIN, PRAGUE)

    assert isinstance(result, RouteResult)
    assert result.status == "estimated"
    assert result.distance_km > 0
    assert result.waypoint_names == []
    assert result.estimated_days >= 1


@patch("src.tools.route.httpx.Client")
def test_route_empty_response_returns_estimated(mock_client_class):
    mock_response = MagicMock()
    mock_response.json.return_value = {"features": []}
    mock_response.raise_for_status = MagicMock()
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.post.return_value = mock_response
    mock_client_class.return_value = mock_client

    with patch.dict("os.environ", {"OPENROUTE_SERVICE_API_KEY": "test-key"}):
        result = get_route(BERLIN, PRAGUE)

    assert result.status == "estimated"
    assert result.distance_km > 0
    assert result.waypoint_names == []


@patch("src.tools.route.httpx.Client")
def test_geocode_returns_coords(mock_client_class):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "features": [
            {"geometry": {"coordinates": [13.4050, 52.5200]}}
        ]
    }
    mock_response.raise_for_status = MagicMock()
    mock_client = MagicMock()
    mock_client.__enter__ = MagicMock(return_value=mock_client)
    mock_client.__exit__ = MagicMock(return_value=False)
    mock_client.get.return_value = mock_response
    mock_client_class.return_value = mock_client

    with patch.dict("os.environ", {"OPENROUTE_SERVICE_API_KEY": "test-key"}):
        result = geocode("Berlin")

    assert result == (13.4050, 52.5200)


def test_geocode_no_api_key_returns_none():
    with patch.dict("os.environ", {}, clear=True):
        assert geocode("Berlin") is None
