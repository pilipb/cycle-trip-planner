from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class RouteResult(BaseModel):
    origin: str
    destination: str
    distance_km: float
    estimated_days: int
    waypoints: list[str]
    surface: str
    route_type: str
    description: str
    status: Literal["found", "estimated"]


_ROUTES: list[dict] = [
    {
        "keys": ("berlin", "prague"),
        "data": {
            "origin": "Berlin",
            "destination": "Prague",
            "distance_km": 350.0,
            "estimated_days": 4,
            "waypoints": ["Dresden", "Bad Schandau", "Decin", "Usti nad Labem"],
            "surface": "Paved cycle paths with some gravel forest sections",
            "route_type": "Elbe Cycle Route (EV7)",
            "description": (
                "A scenic route following the Elbe river through Saxon Switzerland "
                "national park. Gentle gradients make it suitable for all levels."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("berlin", "amsterdam"),
        "data": {
            "origin": "Berlin",
            "destination": "Amsterdam",
            "distance_km": 650.0,
            "estimated_days": 7,
            "waypoints": ["Magdeburg", "Hanover", "Osnabrück", "Groningen"],
            "surface": "Excellent dedicated cycle paths throughout",
            "route_type": "North Sea Cycle Route (EV12)",
            "description": (
                "Classic European cycling connecting Germany and the Netherlands "
                "through low-lying countryside and historic cities."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("amsterdam", "paris"),
        "data": {
            "origin": "Amsterdam",
            "destination": "Paris",
            "distance_km": 500.0,
            "estimated_days": 5,
            "waypoints": ["Antwerp", "Brussels", "Lille", "Compiègne"],
            "surface": "Mix of dedicated cycle paths and quiet roads",
            "route_type": "EV5 Via Romea Francigena",
            "description": (
                "Connecting two iconic European capitals through Belgium "
                "and northern France."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("paris", "lyon"),
        "data": {
            "origin": "Paris",
            "destination": "Lyon",
            "distance_km": 465.0,
            "estimated_days": 5,
            "waypoints": ["Fontainebleau", "Montargis", "Briare", "Nevers"],
            "surface": "Mostly paved, Loire Valley cycle paths",
            "route_type": "Loire à Vélo / EV6",
            "description": (
                "Following the Loire river valley through French château country. "
                "Gently undulating terrain."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("lyon", "barcelona"),
        "data": {
            "origin": "Lyon",
            "destination": "Barcelona",
            "distance_km": 720.0,
            "estimated_days": 8,
            "waypoints": ["Montpellier", "Perpignan", "Girona"],
            "surface": "Mix of cycle paths, coastal roads, and mountain passes",
            "route_type": "Mediterranean Route (EV8)",
            "description": (
                "The Mediterranean coast route from France into Spain, "
                "with stunning coastal scenery and some challenging climbs."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("munich", "vienna"),
        "data": {
            "origin": "Munich",
            "destination": "Vienna",
            "distance_km": 460.0,
            "estimated_days": 5,
            "waypoints": ["Salzburg", "Linz", "St. Pölten"],
            "surface": "High quality cycle paths along the Danube and Salzach",
            "route_type": "Danube Cycle Route (EV6)",
            "description": (
                "One of Europe's most popular cycling routes, following the Danube "
                "through Austria's most scenic landscapes."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("vienna", "budapest"),
        "data": {
            "origin": "Vienna",
            "destination": "Budapest",
            "distance_km": 280.0,
            "estimated_days": 3,
            "waypoints": ["Bratislava", "Györ"],
            "surface": "Excellent Danube cycle paths throughout",
            "route_type": "Danube Cycle Route (EV6)",
            "description": (
                "A short and spectacular ride through three capital cities along the Danube. "
                "Mostly flat with excellent facilities."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("budapest", "krakow"),
        "data": {
            "origin": "Budapest",
            "destination": "Krakow",
            "distance_km": 420.0,
            "estimated_days": 5,
            "waypoints": ["Miskolc", "Kosice", "Poprad"],
            "surface": "Mix of paved roads and forest trails, some challenging sections",
            "route_type": "Iron Curtain Trail (EV13)",
            "description": (
                "Crossing the Carpathian mountains through Slovakia "
                "with dramatic highland scenery."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("berlin", "warsaw"),
        "data": {
            "origin": "Berlin",
            "destination": "Warsaw",
            "distance_km": 570.0,
            "estimated_days": 6,
            "waypoints": ["Frankfurt (Oder)", "Poznań", "Łódź"],
            "surface": "Paved roads with dedicated cycle lanes in cities",
            "route_type": "Oder-Neisse Cycle Route",
            "description": (
                "Following the German-Polish border before heading east "
                "through the Polish heartland."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("warsaw", "vilnius"),
        "data": {
            "origin": "Warsaw",
            "destination": "Vilnius",
            "distance_km": 470.0,
            "estimated_days": 5,
            "waypoints": ["Białystok", "Suwałki", "Kaunas"],
            "surface": "Quiet rural roads through forest and lake regions",
            "route_type": "Iron Curtain Trail (EV13)",
            "description": (
                "Traversing the Białowieża Forest region and Baltic states borderlands."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("tallinn", "riga"),
        "data": {
            "origin": "Tallinn",
            "destination": "Riga",
            "distance_km": 310.0,
            "estimated_days": 4,
            "waypoints": ["Pärnu", "Saulkrasti"],
            "surface": "Excellent Baltic coast cycle path with pine forest sections",
            "route_type": "EuroVelo 10 Baltic Sea Cycle Route",
            "description": (
                "Stunning coastal cycling along the Baltic Sea "
                "with pine forests and historic towns."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("riga", "vilnius"),
        "data": {
            "origin": "Riga",
            "destination": "Vilnius",
            "distance_km": 290.0,
            "estimated_days": 3,
            "waypoints": ["Jēkabpils", "Panevėžys"],
            "surface": "Paved roads with variable cycle infrastructure",
            "route_type": "Iron Curtain Trail (EV13)",
            "description": (
                "Connecting Latvia and Lithuania through the scenic Baltic countryside."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("zurich", "geneva"),
        "data": {
            "origin": "Zurich",
            "destination": "Geneva",
            "distance_km": 310.0,
            "estimated_days": 4,
            "waypoints": ["Bern", "Fribourg", "Lausanne"],
            "surface": "Switzerland's premium cycle infrastructure, national route 5",
            "route_type": "Mittelland Route (National Route 5)",
            "description": (
                "Through the Swiss Mittelland with views of the Alps. "
                "Well-signposted and with excellent facilities."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("lisbon", "porto"),
        "data": {
            "origin": "Lisbon",
            "destination": "Porto",
            "distance_km": 380.0,
            "estimated_days": 4,
            "waypoints": ["Peniche", "Aveiro"],
            "surface": "Atlantic coast paths and quiet rural roads",
            "route_type": "Atlantic Route (EV1)",
            "description": (
                "Portugal's beautiful western coast from capital to second city, "
                "with dramatic Atlantic scenery."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("florence", "rome"),
        "data": {
            "origin": "Florence",
            "destination": "Rome",
            "distance_km": 310.0,
            "estimated_days": 4,
            "waypoints": ["Siena", "Orvieto", "Viterbo"],
            "surface": "Tuscany gravel roads (strade bianche) and paved provincial roads",
            "route_type": "Via Francigena",
            "description": (
                "The ancient pilgrimage route through Tuscany and Lazio, "
                "with rolling hills and medieval towns."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("florence", "venice"),
        "data": {
            "origin": "Florence",
            "destination": "Venice",
            "distance_km": 260.0,
            "estimated_days": 3,
            "waypoints": ["Bologna", "Ferrara", "Padua"],
            "surface": "Po Valley cycle paths with some urban sections",
            "route_type": "Po Valley Cycle Route",
            "description": (
                "From the Tuscan hills to the Venetian lagoon "
                "through the flat Po river plain."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("copenhagen", "hamburg"),
        "data": {
            "origin": "Copenhagen",
            "destination": "Hamburg",
            "distance_km": 380.0,
            "estimated_days": 4,
            "waypoints": ["Roskilde", "Odense", "Flensburg", "Kiel"],
            "surface": "Excellent Danish and German cycle infrastructure",
            "route_type": "North Sea Cycle Route (EV12)",
            "description": (
                "Crossing from Denmark to Germany via ferry, "
                "through Jutland and Schleswig-Holstein."
            ),
            "status": "found",
        },
    },
    {
        "keys": ("brussels", "amsterdam"),
        "data": {
            "origin": "Brussels",
            "destination": "Amsterdam",
            "distance_km": 220.0,
            "estimated_days": 2,
            "waypoints": ["Antwerp", "Rotterdam"],
            "surface": "Flat terrain with excellent dedicated cycle infrastructure",
            "route_type": "North Sea Cycle Route (EV12)",
            "description": "A quick and easy flat ride through Belgium and the Netherlands.",
            "status": "found",
        },
    },
]


def _normalize(s: str) -> str:
    return s.lower().strip()


def _match(s: str, key: str) -> bool:
    return key in s or s in key





def get_route(origin: str, destination: str) -> RouteResult:
    """Get cycling route details between two locations."""
    o = _normalize(origin)
    d = _normalize(destination)

    for entry in _ROUTES:
        k1, k2 = entry["keys"]
        if _match(o, k1) and _match(d, k2):
            return RouteResult(**entry["data"])
        if _match(o, k2) and _match(d, k1):
            data = dict(entry["data"])
            data["origin"] = origin.title()
            data["destination"] = destination.title()
            data["waypoints"] = list(reversed(data["waypoints"]))
            return RouteResult(**data)

    # Fallback estimated route
    distance = 400.0
    days = max(1, round(distance / 80))
    return RouteResult(
        origin=origin,
        destination=destination,
        distance_km=distance,
        estimated_days=days,
        waypoints=[],
        surface="Mixed terrain, conditions unknown",
        route_type="Custom route",
        description=(
            f"Estimated cycling route from {origin} to {destination}. "
            "We recommend checking local cycling maps for detailed planning."
        ),
        status="estimated",
    )
