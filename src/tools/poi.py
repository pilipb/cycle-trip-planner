from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

POICategory = Literal["cultural", "restaurants", "viewpoints", "cycling_shops", "water_sources"]


class PointOfInterest(BaseModel):
    name: str
    category: POICategory
    location: str
    description: str
    distance_from_route_km: float
    opening_hours: str | None
    price_eur: float | None
    cycling_accessible: bool
    notes: str


_POI_DB: dict[str, dict[str, list[dict]]] = {
    "berlin": {
        "cultural": [
            {
                "name": "Brandenburg Gate",
                "category": "cultural",
                "location": "Mitte, Berlin",
                "description": "Iconic 18th-century neoclassical monument, symbol of German reunification",
                "distance_from_route_km": 0.2,
                "opening_hours": "24/7 (exterior)",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "Excellent bike parking nearby, central cycling hub",
            },
            {
                "name": "East Side Gallery",
                "category": "cultural",
                "location": "Friedrichshain, Berlin",
                "description": "1.3km open-air gallery on remaining Berlin Wall section",
                "distance_from_route_km": 0.0,
                "opening_hours": "24/7",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "Right on the riverside cycling path",
            },
        ],
        "cycling_shops": [
            {
                "name": "Fahrradstation Berlin",
                "category": "cycling_shops",
                "location": "Friedrichstraße, Berlin",
                "description": "Full-service bike shop with repair, parts, and hire",
                "distance_from_route_km": 0.3,
                "opening_hours": "Mon-Sat 09:00-19:00",
                "price_eur": None,
                "cycling_accessible": True,
                "notes": "Excellent for panniers, gear repairs before long trip",
            }
        ],
        "water_sources": [
            {
                "name": "Trinkwasserbrunnen Tiergarten",
                "category": "water_sources",
                "location": "Tiergarten, Berlin",
                "description": "Drinking water fountains throughout Tiergarten park",
                "distance_from_route_km": 0.1,
                "opening_hours": "April-October",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "Free drinking water, multiple locations in the park",
            }
        ],
        "viewpoints": [
            {
                "name": "Teufelsberg",
                "category": "viewpoints",
                "location": "Grunewald, Berlin",
                "description": "Cold War listening station on artificial hill, panoramic city views",
                "distance_from_route_km": 5.0,
                "opening_hours": "Varies",
                "price_eur": 8.0,
                "cycling_accessible": True,
                "notes": "Worthwhile detour for Berlin panorama",
            }
        ],
        "restaurants": [
            {
                "name": "Markthalle Neun",
                "category": "restaurants",
                "location": "Kreuzberg, Berlin",
                "description": "Historic covered market with street food, local produce and craft beer",
                "distance_from_route_km": 0.5,
                "opening_hours": "Thu 17:00-22:00, Sat 10:00-18:00",
                "price_eur": 15.0,
                "cycling_accessible": True,
                "notes": "Thursday street food market is unmissable",
            }
        ],
    },
    "prague": {
        "cultural": [
            {
                "name": "Prague Castle",
                "category": "cultural",
                "location": "Hradčany, Prague",
                "description": "World's largest ancient castle complex, home to St. Vitus Cathedral",
                "distance_from_route_km": 0.8,
                "opening_hours": "Daily 06:00-22:00 (grounds)",
                "price_eur": 15.0,
                "cycling_accessible": False,
                "notes": "Lock bike at base, walk up — very steep approach",
            }
        ],
        "cycling_shops": [
            {
                "name": "Praha Bike",
                "category": "cycling_shops",
                "location": "Nové Město, Prague",
                "description": "City cycle hire and repairs, route advice for Vltava trail",
                "distance_from_route_km": 0.2,
                "opening_hours": "Daily 09:00-19:00",
                "price_eur": None,
                "cycling_accessible": True,
                "notes": "Helpful staff with local cycling knowledge",
            }
        ],
        "viewpoints": [
            {
                "name": "Vyšehrad",
                "category": "viewpoints",
                "location": "Vyšehrad, Prague",
                "description": "Historic fortress with stunning views over the Vltava and old town",
                "distance_from_route_km": 0.3,
                "opening_hours": "Daily 09:30-18:00",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "On the Vltava cycling path, excellent sunset views",
            }
        ],
        "restaurants": [
            {
                "name": "Lokál",
                "category": "restaurants",
                "location": "Staré Město, Prague",
                "description": "Classic Czech pub with tank-fresh Pilsner Urquell and hearty food",
                "distance_from_route_km": 0.4,
                "opening_hours": "Mon-Sat 11:00-01:00, Sun 12:00-22:00",
                "price_eur": 12.0,
                "cycling_accessible": True,
                "notes": "Essential Czech experience, try svíčková",
            }
        ],
        "water_sources": [
            {
                "name": "Vltava River Fountains",
                "category": "water_sources",
                "location": "Vltava embankment, Prague",
                "description": "Drinking fountains along the Vltava cycling path",
                "distance_from_route_km": 0.0,
                "opening_hours": "May-September",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "On-route water, regular fountains",
            }
        ],
    },
    "amsterdam": {
        "cultural": [
            {
                "name": "Rijksmuseum",
                "category": "cultural",
                "location": "Museumplein, Amsterdam",
                "description": "Dutch national museum with Rembrandt and Vermeer masterpieces",
                "distance_from_route_km": 0.3,
                "opening_hours": "Daily 09:00-17:00",
                "price_eur": 22.5,
                "cycling_accessible": True,
                "notes": "Famous underpass designed for cyclists",
            }
        ],
        "cycling_shops": [
            {
                "name": "MacBike",
                "category": "cycling_shops",
                "location": "Multiple locations, Amsterdam",
                "description": "Amsterdam's largest cycle hire with city and touring bikes",
                "distance_from_route_km": 0.1,
                "opening_hours": "Daily 09:00-17:30",
                "price_eur": None,
                "cycling_accessible": True,
                "notes": "Central Station and Leidseplein locations",
            }
        ],
        "viewpoints": [
            {
                "name": "A'DAM Tower Lookout",
                "category": "viewpoints",
                "location": "Noord, Amsterdam",
                "description": "360° panoramic views from 22nd floor, with Europe's highest swing",
                "distance_from_route_km": 0.5,
                "opening_hours": "Daily 10:00-22:00",
                "price_eur": 17.5,
                "cycling_accessible": True,
                "notes": "Free ferry from Centraal Station, bike-friendly",
            }
        ],
        "restaurants": [
            {
                "name": "Foodhallen",
                "category": "restaurants",
                "location": "Oud-West, Amsterdam",
                "description": "Indoor food market with diverse street food from around the world",
                "distance_from_route_km": 0.6,
                "opening_hours": "Sun-Thu 11:00-23:30, Fri-Sat 11:00-01:00",
                "price_eur": 15.0,
                "cycling_accessible": True,
                "notes": "Great post-ride meal spot",
            }
        ],
        "water_sources": [
            {
                "name": "Vondelpark Fountains",
                "category": "water_sources",
                "location": "Vondelpark, Amsterdam",
                "description": "Drinking fountains throughout Vondelpark",
                "distance_from_route_km": 0.2,
                "opening_hours": "Year-round",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "On the main cycling path through the park",
            }
        ],
    },
    "vienna": {
        "cultural": [
            {
                "name": "Kunsthistorisches Museum",
                "category": "cultural",
                "location": "Ringstrasse, Vienna",
                "description": "Imperial art museum with one of Europe's finest collections",
                "distance_from_route_km": 0.4,
                "opening_hours": "Tue-Sun 10:00-18:00",
                "price_eur": 21.0,
                "cycling_accessible": True,
                "notes": "Excellent bike parking on the Ringstrasse",
            }
        ],
        "cycling_shops": [
            {
                "name": "Rad & Tat",
                "category": "cycling_shops",
                "location": "Mariahilfer Straße, Vienna",
                "description": "Full-service bike shop with touring equipment",
                "distance_from_route_km": 0.3,
                "opening_hours": "Mon-Fri 09:00-18:00, Sat 09:00-17:00",
                "price_eur": None,
                "cycling_accessible": True,
                "notes": "Good for Danube route preparation",
            }
        ],
        "viewpoints": [
            {
                "name": "Kahlenberg",
                "category": "viewpoints",
                "location": "Vienna Woods, Vienna",
                "description": "484m hill with panoramic views over Vienna and the Danube",
                "distance_from_route_km": 8.0,
                "opening_hours": "24/7",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "Classic Viennese cycling climb, 400m ascent from city",
            }
        ],
        "restaurants": [
            {
                "name": "Café Central",
                "category": "restaurants",
                "location": "Innere Stadt, Vienna",
                "description": "Historic Habsburg-era coffee house with original Viennese atmosphere",
                "distance_from_route_km": 0.5,
                "opening_hours": "Mon-Sat 07:30-22:00, Sun 10:00-22:00",
                "price_eur": 18.0,
                "cycling_accessible": True,
                "notes": "Essential Viennese coffee house experience",
            }
        ],
        "water_sources": [
            {
                "name": "Danube Cycle Path Fountains",
                "category": "water_sources",
                "location": "Danube Island, Vienna",
                "description": "Regular drinking water points along the Danube cycle path",
                "distance_from_route_km": 0.0,
                "opening_hours": "April-October",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "On-route every ~10km on the Danube path",
            }
        ],
    },
    "munich": {
        "cultural": [
            {
                "name": "Deutsches Museum",
                "category": "cultural",
                "location": "Museum Island, Munich",
                "description": "World's largest science and technology museum",
                "distance_from_route_km": 0.5,
                "opening_hours": "Daily 09:00-17:00",
                "price_eur": 15.0,
                "cycling_accessible": True,
                "notes": "On the Isar river cycling path",
            }
        ],
        "cycling_shops": [
            {
                "name": "Radius Bikes",
                "category": "cycling_shops",
                "location": "Central Station, Munich",
                "description": "Touring bike hire and advice for Danube and Alpine routes",
                "distance_from_route_km": 0.2,
                "opening_hours": "Apr-Oct daily 09:00-18:00",
                "price_eur": None,
                "cycling_accessible": True,
                "notes": "Excellent for panniers and route maps",
            }
        ],
        "viewpoints": [
            {
                "name": "Olympiaberg",
                "category": "viewpoints",
                "location": "Olympiapark, Munich",
                "description": "Artificial hill with views over Munich and Alps on clear days",
                "distance_from_route_km": 2.0,
                "opening_hours": "24/7",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "Free, on cycling route through Olympiapark",
            }
        ],
        "restaurants": [
            {
                "name": "Englischer Garten Biergarten",
                "category": "restaurants",
                "location": "Englischer Garten, Munich",
                "description": "One of the world's largest beer gardens, 7,000 seats under chestnut trees",
                "distance_from_route_km": 0.3,
                "opening_hours": "Daily 10:00-22:00 (weather permitting)",
                "price_eur": 12.0,
                "cycling_accessible": True,
                "notes": "On the Isar cycling path, perfect post-ride Maßkrug",
            }
        ],
        "water_sources": [
            {
                "name": "Isar River Fountains",
                "category": "water_sources",
                "location": "Isar riverside, Munich",
                "description": "Drinking fountains along the Isar river cycling path",
                "distance_from_route_km": 0.0,
                "opening_hours": "May-September",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "On-route throughout the Isar cycle path",
            }
        ],
    },
    "budapest": {
        "cultural": [
            {
                "name": "Buda Castle",
                "category": "cultural",
                "location": "Castle Hill, Budapest",
                "description": "Historic castle complex with National Gallery and History Museum",
                "distance_from_route_km": 0.8,
                "opening_hours": "Grounds 24/7, museums 10:00-18:00",
                "price_eur": 8.0,
                "cycling_accessible": False,
                "notes": "Lock bike at base; funicular or walk up",
            }
        ],
        "cycling_shops": [
            {
                "name": "Cycling Hungary",
                "category": "cycling_shops",
                "location": "Belvárosi, Budapest",
                "description": "Specialist touring shop with Danube route expertise",
                "distance_from_route_km": 0.3,
                "opening_hours": "Mon-Fri 09:00-18:00, Sat 10:00-16:00",
                "price_eur": None,
                "cycling_accessible": True,
                "notes": "Great for Danube route maps and repairs",
            }
        ],
        "viewpoints": [
            {
                "name": "Gellért Hill",
                "category": "viewpoints",
                "location": "Gellért Hill, Budapest",
                "description": "Citadel and Liberty Statue with stunning Danube panoramas",
                "distance_from_route_km": 0.3,
                "opening_hours": "24/7",
                "price_eur": 0.0,
                "cycling_accessible": False,
                "notes": "Push bike up or lock at base; unforgettable views",
            }
        ],
        "restaurants": [
            {
                "name": "Great Market Hall",
                "category": "restaurants",
                "location": "Fővám tér, Budapest",
                "description": "Historic covered market with Hungarian food stalls and lángos",
                "distance_from_route_km": 0.3,
                "opening_hours": "Mon-Sat 06:00-18:00",
                "price_eur": 8.0,
                "cycling_accessible": True,
                "notes": "Best Hungarian street food, very cheap",
            }
        ],
        "water_sources": [
            {
                "name": "Danube Promenade Fountains",
                "category": "water_sources",
                "location": "Danube embankment, Budapest",
                "description": "Drinking fountains along the Danube cycling promenade",
                "distance_from_route_km": 0.0,
                "opening_hours": "Year-round",
                "price_eur": 0.0,
                "cycling_accessible": True,
                "notes": "Regular fountains along the riverside path",
            }
        ],
    },
}


def _find_key(location: str) -> str | None:
    loc = location.lower().strip()
    for key in _POI_DB:
        if key in loc or loc in key:
            return key
    return None


def get_points_of_interest(location: str, category: POICategory) -> list[PointOfInterest]:
    """Find points of interest near the cycling route at a given location."""
    key = _find_key(location)
    if key and category in _POI_DB[key]:
        return [PointOfInterest(**p) for p in _POI_DB[key][category]]

    # Fallback
    return [
        PointOfInterest(
            name=f"{location.title()} {category.replace('_', ' ').title()}",
            category=category,
            location=location,
            description=f"Explore {category.replace('_', ' ')} options in {location}",
            distance_from_route_km=0.5,
            opening_hours=None,
            price_eur=None,
            cycling_accessible=True,
            notes="Check local listings for current options",
        )
    ]
