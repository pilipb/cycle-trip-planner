from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class ElevationResult(BaseModel):
    origin: str
    destination: str
    total_ascent_m: int
    total_descent_m: int
    max_elevation_m: int
    min_elevation_m: int
    profile_description: str
    challenging_sections: list[str]
    status: Literal["found", "estimated"]


_ELEVATION_DB: list[dict] = [
    {
        "keys": ("berlin", "prague"),
        "data": {
            "total_ascent_m": 1800,
            "total_descent_m": 1950,
            "max_elevation_m": 420,
            "min_elevation_m": 35,
            "profile_description": (
                "Mostly flat through the German lowlands, then gently rolling into "
                "the Saxon hills. The Saxon Switzerland section has some moderate climbs."
            ),
            "challenging_sections": ["Saxon Switzerland gorge section (~50m climb)", "Decin valley descent"],
        },
    },
    {
        "keys": ("berlin", "amsterdam"),
        "data": {
            "total_ascent_m": 800,
            "total_descent_m": 800,
            "max_elevation_m": 120,
            "min_elevation_m": 0,
            "profile_description": "Very flat route across the North German and Dutch lowlands. Near sea level throughout.",
            "challenging_sections": ["Slight headwinds common on exposed sections"],
        },
    },
    {
        "keys": ("amsterdam", "paris"),
        "data": {
            "total_ascent_m": 1200,
            "total_descent_m": 1100,
            "max_elevation_m": 280,
            "min_elevation_m": 0,
            "profile_description": "Flat through Belgium, gentle rolling hills in northern France.",
            "challenging_sections": ["Ardennes foothills near Namur (optional detour)"],
        },
    },
    {
        "keys": ("paris", "lyon"),
        "data": {
            "total_ascent_m": 2200,
            "total_descent_m": 1800,
            "max_elevation_m": 350,
            "min_elevation_m": 70,
            "profile_description": (
                "Generally flat along the Loire valley, with more undulating terrain "
                "towards Burgundy and Lyon."
            ),
            "challenging_sections": ["Côtes du Rhône approach to Lyon (~200m ascent)"],
        },
    },
    {
        "keys": ("lyon", "barcelona"),
        "data": {
            "total_ascent_m": 5800,
            "total_descent_m": 5600,
            "max_elevation_m": 1600,
            "min_elevation_m": 0,
            "profile_description": (
                "Significant climbing involved, especially through the Pyrenees. "
                "Coastal sections are easier but some steep headlands."
            ),
            "challenging_sections": [
                "Col du Perthus (Pyrenees crossing, 290m)",
                "Cap de Creus coastal section",
                "Montpellier to Narbonne coastal hills",
            ],
        },
    },
    {
        "keys": ("munich", "vienna"),
        "data": {
            "total_ascent_m": 2400,
            "total_descent_m": 2500,
            "max_elevation_m": 620,
            "min_elevation_m": 180,
            "profile_description": (
                "Rolling terrain following the Salzach and Danube valleys. "
                "Some steady climbs leaving Munich and near Salzburg."
            ),
            "challenging_sections": [
                "Munich to Rosenheim hill section (~150m)",
                "Salzburg city approach",
            ],
        },
    },
    {
        "keys": ("vienna", "budapest"),
        "data": {
            "total_ascent_m": 600,
            "total_descent_m": 650,
            "max_elevation_m": 290,
            "min_elevation_m": 100,
            "profile_description": "Flat Danube plain. One of Europe's easiest long-distance routes.",
            "challenging_sections": ["Bratislava urban navigation"],
        },
    },
    {
        "keys": ("budapest", "krakow"),
        "data": {
            "total_ascent_m": 4200,
            "total_descent_m": 3900,
            "max_elevation_m": 1200,
            "min_elevation_m": 95,
            "profile_description": (
                "Significant Carpathian mountain crossing required. "
                "Spectacular but demanding terrain."
            ),
            "challenging_sections": [
                "Tatra foothills near Poprad (~600m total ascent)",
                "Miskolc to Kosice border section",
                "High Tatra approaches",
            ],
        },
    },
    {
        "keys": ("berlin", "warsaw"),
        "data": {
            "total_ascent_m": 1400,
            "total_descent_m": 1400,
            "max_elevation_m": 200,
            "min_elevation_m": 20,
            "profile_description": "Flat to gently rolling across the North European Plain.",
            "challenging_sections": ["Slight morainic hills near Poznań"],
        },
    },
    {
        "keys": ("warsaw", "vilnius"),
        "data": {
            "total_ascent_m": 1600,
            "total_descent_m": 1500,
            "max_elevation_m": 310,
            "min_elevation_m": 90,
            "profile_description": "Rolling glacial landscape with lakes and forests. Moderate terrain.",
            "challenging_sections": ["Suwałki Landscape Park ridge section"],
        },
    },
    {
        "keys": ("tallinn", "riga"),
        "data": {
            "total_ascent_m": 800,
            "total_descent_m": 780,
            "max_elevation_m": 120,
            "min_elevation_m": 0,
            "profile_description": "Flat coastal plain with gentle forest undulations.",
            "challenging_sections": ["Sandy tracks near the coast (soft going)"],
        },
    },
    {
        "keys": ("riga", "vilnius"),
        "data": {
            "total_ascent_m": 1100,
            "total_descent_m": 1050,
            "max_elevation_m": 280,
            "min_elevation_m": 20,
            "profile_description": "Gently rolling Baltic countryside.",
            "challenging_sections": ["Aukštaitija uplands section"],
        },
    },
    {
        "keys": ("zurich", "geneva"),
        "data": {
            "total_ascent_m": 3200,
            "total_descent_m": 3100,
            "max_elevation_m": 850,
            "min_elevation_m": 370,
            "profile_description": (
                "Rolling Swiss Mittelland with regular climbs and descents. "
                "Backdrop of Alps throughout."
            ),
            "challenging_sections": [
                "Bern to Fribourg Sense valley (~250m)",
                "Lausanne approach from the lake (~200m)",
            ],
        },
    },
    {
        "keys": ("lisbon", "porto"),
        "data": {
            "total_ascent_m": 2800,
            "total_descent_m": 2700,
            "max_elevation_m": 320,
            "min_elevation_m": 0,
            "profile_description": "Rolling Atlantic coast and river valleys with some coastal climbs.",
            "challenging_sections": [
                "Serra da Lousã foothills (inland route)",
                "Aveiro lagoon coastal approach",
            ],
        },
    },
    {
        "keys": ("florence", "rome"),
        "data": {
            "total_ascent_m": 5500,
            "total_descent_m": 5300,
            "max_elevation_m": 750,
            "min_elevation_m": 15,
            "profile_description": (
                "The Tuscan and Lazio hills make this a genuinely challenging route "
                "with repeated rolling climbs through stunning scenery."
            ),
            "challenging_sections": [
                "Chianti hills south of Florence (~400m spread over 30km)",
                "Siena city approach",
                "Val d'Orcia undulations",
                "Monte Amiata foothills",
            ],
        },
    },
    {
        "keys": ("florence", "venice"),
        "data": {
            "total_ascent_m": 2200,
            "total_descent_m": 2300,
            "max_elevation_m": 640,
            "min_elevation_m": 0,
            "profile_description": (
                "Apennine crossing near Bologna, then flat Po valley to Venice."
            ),
            "challenging_sections": [
                "Apennine crossing: Futa Pass (903m, 18km climb)",
                "Bologna to Ferrara transition",
            ],
        },
    },
    {
        "keys": ("copenhagen", "hamburg"),
        "data": {
            "total_ascent_m": 1200,
            "total_descent_m": 1200,
            "max_elevation_m": 170,
            "min_elevation_m": 0,
            "profile_description": "Flat to gently rolling Jutland and Schleswig-Holstein landscape.",
            "challenging_sections": ["Flensburg fjord section", "Kiel Canal crossing"],
        },
    },
    {
        "keys": ("brussels", "amsterdam"),
        "data": {
            "total_ascent_m": 400,
            "total_descent_m": 400,
            "max_elevation_m": 80,
            "min_elevation_m": 0,
            "profile_description": "Almost completely flat Benelux plains. Perfect for beginners.",
            "challenging_sections": ["Rotterdam bridge approaches"],
        },
    },
]


def _normalize(s: str) -> str:
    return s.lower().strip()


def _match(s: str, key: str) -> bool:
    return key in s or s in key


def get_elevation_profile(origin: str, destination: str) -> ElevationResult:
    """Get elevation profile and difficulty assessment for a cycling route."""
    o = _normalize(origin)
    d = _normalize(destination)

    for entry in _ELEVATION_DB:
        k1, k2 = entry["keys"]
        if _match(o, k1) and _match(d, k2):
            return ElevationResult(
                origin=origin,
                destination=destination,
                status="found",
                **entry["data"],
            )
        if _match(o, k2) and _match(d, k1):
            data = dict(entry["data"])
            # Swap ascent/descent for reverse direction
            data["total_ascent_m"], data["total_descent_m"] = (
                data["total_descent_m"],
                data["total_ascent_m"],
            )
            return ElevationResult(
                origin=origin,
                destination=destination,
                status="found",
                **data,
            )

    # Fallback estimate
    return ElevationResult(
        origin=origin,
        destination=destination,
        total_ascent_m=2000,
        total_descent_m=2000,
        max_elevation_m=400,
        min_elevation_m=50,
        profile_description=(
            f"Estimated elevation profile for {origin} to {destination}. "
            "Expect moderate rolling terrain typical of European cycling routes."
        ),
        challenging_sections=["Unknown — check local maps for detailed profile"],
        status="estimated",
    )
