from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

AccommodationType = Literal["camping", "hostel", "hotel", "guesthouse"]


class Accommodation(BaseModel):
    name: str
    type: AccommodationType
    location: str
    price_per_night_eur: float
    amenities: list[str]
    cycling_friendly: bool
    rating: float
    notes: str


_DATA: dict[str, dict[str, list[dict]]] = {
    "berlin": {
        "camping": [
            {
                "name": "Camping Krossinsee",
                "type": "camping",
                "location": "Berlin Southeast",
                "price_per_night_eur": 18.0,
                "amenities": ["shower", "kitchen", "Wi-Fi", "bike storage"],
                "cycling_friendly": True,
                "rating": 4.2,
                "notes": "Well-equipped campsite near the Müggelspree forest",
            }
        ],
        "hostel": [
            {
                "name": "Generator Berlin Mitte",
                "type": "hostel",
                "location": "Mitte",
                "price_per_night_eur": 28.0,
                "amenities": ["shower", "lockers", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "Central location, secure bike room available",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Indigo Berlin Mitte",
                "type": "hotel",
                "location": "Mitte",
                "price_per_night_eur": 120.0,
                "amenities": ["shower", "restaurant", "bar", "parking", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Bike hire available, central location",
            }
        ],
        "guesthouse": [
            {
                "name": "Pension Funk",
                "type": "guesthouse",
                "location": "Charlottenburg",
                "price_per_night_eur": 65.0,
                "amenities": ["shower", "breakfast", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Charming 1920s style, excellent breakfast",
            }
        ],
    },
    "prague": {
        "camping": [
            {
                "name": "Camping Trojská",
                "type": "camping",
                "location": "Prague North",
                "price_per_night_eur": 14.0,
                "amenities": ["shower", "kitchen", "bike storage"],
                "cycling_friendly": True,
                "rating": 4.0,
                "notes": "Near the Vltava riverside cycling path",
            }
        ],
        "hostel": [
            {
                "name": "Czech Inn Hostel",
                "type": "hostel",
                "location": "Vinohrady",
                "price_per_night_eur": 20.0,
                "amenities": ["shower", "kitchen", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Award-winning hostel, bike rental nearby",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Questenberk",
                "type": "hotel",
                "location": "Hradčany",
                "price_per_night_eur": 95.0,
                "amenities": ["shower", "restaurant", "terrace", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.7,
                "notes": "Historic building with stunning castle views",
            }
        ],
        "guesthouse": [
            {
                "name": "Pension Arbes",
                "type": "guesthouse",
                "location": "Smíchov",
                "price_per_night_eur": 50.0,
                "amenities": ["shower", "breakfast", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.2,
                "notes": "Family-run, good cycling location near the Vltava path",
            }
        ],
    },
    "dresden": {
        "camping": [
            {
                "name": "Camping Mockritz",
                "type": "camping",
                "location": "Dresden South",
                "price_per_night_eur": 15.0,
                "amenities": ["shower", "kitchen", "bike storage"],
                "cycling_friendly": True,
                "rating": 4.1,
                "notes": "On the Elbe cycle route, great facilities",
            }
        ],
        "hostel": [
            {
                "name": "Hostel Mondpalast",
                "type": "hostel",
                "location": "Neustadt",
                "price_per_night_eur": 22.0,
                "amenities": ["shower", "kitchen", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "Friendly hostel in the hip Neustadt district",
            }
        ],
        "hotel": [
            {
                "name": "Innside Dresden",
                "type": "hotel",
                "location": "Altstadt",
                "price_per_night_eur": 100.0,
                "amenities": ["shower", "restaurant", "parking", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Modern hotel near the Elbe banks",
            }
        ],
        "guesthouse": [
            {
                "name": "Gästehaus Altstadt",
                "type": "guesthouse",
                "location": "Altstadt",
                "price_per_night_eur": 55.0,
                "amenities": ["shower", "breakfast", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.0,
                "notes": "Convenient to all sights",
            }
        ],
    },
    "amsterdam": {
        "camping": [
            {
                "name": "Camping Zeeburg",
                "type": "camping",
                "location": "East Amsterdam",
                "price_per_night_eur": 22.0,
                "amenities": ["shower", "kitchen", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Ferry access to city centre, ideal for cyclists",
            }
        ],
        "hostel": [
            {
                "name": "Stayokay Amsterdam Vondelpark",
                "type": "hostel",
                "location": "Oud-West",
                "price_per_night_eur": 35.0,
                "amenities": ["shower", "restaurant", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Set in a listed building by Vondelpark",
            }
        ],
        "hotel": [
            {
                "name": "Hotel V Nesplein",
                "type": "hotel",
                "location": "Centrum",
                "price_per_night_eur": 140.0,
                "amenities": ["shower", "bar", "bike hire", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Amsterdam's most cycling-friendly hotel",
            }
        ],
        "guesthouse": [
            {
                "name": "B&B Le Coin",
                "type": "guesthouse",
                "location": "Jordaan",
                "price_per_night_eur": 80.0,
                "amenities": ["shower", "breakfast", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Charming canal house with excellent breakfast",
            }
        ],
    },
    "paris": {
        "camping": [
            {
                "name": "Camping Paris Est",
                "type": "camping",
                "location": "Champigny-sur-Marne",
                "price_per_night_eur": 25.0,
                "amenities": ["shower", "restaurant", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.0,
                "notes": "30 min by RER to Paris centre",
            }
        ],
        "hostel": [
            {
                "name": "Generator Paris",
                "type": "hostel",
                "location": "10th arrondissement",
                "price_per_night_eur": 38.0,
                "amenities": ["shower", "bar", "lockers", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.2,
                "notes": "Design hostel with secure bike storage",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Fabric",
                "type": "hotel",
                "location": "11th arrondissement",
                "price_per_night_eur": 150.0,
                "amenities": ["shower", "bar", "bike hire", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Converted textile factory, excellent access to Canal Saint-Martin",
            }
        ],
        "guesthouse": [
            {
                "name": "Mama Shelter Paris East",
                "type": "guesthouse",
                "location": "20th arrondissement",
                "price_per_night_eur": 90.0,
                "amenities": ["shower", "restaurant", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Trendy neighbourhood, good Vélib' bike access",
            }
        ],
    },
    "munich": {
        "camping": [
            {
                "name": "Campingplatz München-Thalkirchen",
                "type": "camping",
                "location": "Thalkirchen",
                "price_per_night_eur": 20.0,
                "amenities": ["shower", "kitchen", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "On the Isar river, excellent cycling access",
            }
        ],
        "hostel": [
            {
                "name": "Wombat's Munich",
                "type": "hostel",
                "location": "Central",
                "price_per_night_eur": 30.0,
                "amenities": ["shower", "kitchen", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Well-equipped hostel, bike rental available nearby",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Laimer Hof",
                "type": "hotel",
                "location": "Nymphenburg",
                "price_per_night_eur": 110.0,
                "amenities": ["shower", "breakfast", "garden", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Charming hotel near Nymphenburg cycling paths",
            }
        ],
        "guesthouse": [
            {
                "name": "Pension Westfalia",
                "type": "guesthouse",
                "location": "Schwabing",
                "price_per_night_eur": 70.0,
                "amenities": ["shower", "breakfast", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.2,
                "notes": "Family-run, excellent location for cycling",
            }
        ],
    },
    "vienna": {
        "camping": [
            {
                "name": "Camping Wien West",
                "type": "camping",
                "location": "Hütteldorf",
                "price_per_night_eur": 22.0,
                "amenities": ["shower", "kitchen", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Near Vienna Woods cycling routes",
            }
        ],
        "hostel": [
            {
                "name": "Wombat's Vienna Naschmarkt",
                "type": "hostel",
                "location": "Mariahilf",
                "price_per_night_eur": 28.0,
                "amenities": ["shower", "kitchen", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Great location near the Naschmarkt",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Rathaus Wein & Design",
                "type": "hotel",
                "location": "Josefstadt",
                "price_per_night_eur": 130.0,
                "amenities": ["shower", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.7,
                "notes": "Boutique hotel in the Ringstrasse area",
            }
        ],
        "guesthouse": [
            {
                "name": "Pension Aviano",
                "type": "guesthouse",
                "location": "Innere Stadt",
                "price_per_night_eur": 75.0,
                "amenities": ["shower", "breakfast", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "Central location near the Danube cycling path",
            }
        ],
    },
    "budapest": {
        "camping": [
            {
                "name": "Camping Római",
                "type": "camping",
                "location": "Aquincum",
                "price_per_night_eur": 12.0,
                "amenities": ["shower", "kitchen", "bike storage"],
                "cycling_friendly": True,
                "rating": 4.0,
                "notes": "On the Danube cycle path, great value",
            }
        ],
        "hostel": [
            {
                "name": "Maverick City Lodge",
                "type": "hostel",
                "location": "Pest Centre",
                "price_per_night_eur": 18.0,
                "amenities": ["shower", "kitchen", "bar", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Fun atmosphere, close to ruin bars",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Clark Budapest",
                "type": "hotel",
                "location": "Buda",
                "price_per_night_eur": 85.0,
                "amenities": ["shower", "restaurant", "spa", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.7,
                "notes": "At the foot of Castle Hill, Danube views",
            }
        ],
        "guesthouse": [
            {
                "name": "Corvin Inn",
                "type": "guesthouse",
                "location": "Józsefváros",
                "price_per_night_eur": 40.0,
                "amenities": ["shower", "breakfast", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Quiet street, good cycling access",
            }
        ],
    },
    "salzburg": {
        "camping": [
            {
                "name": "Camping Nord-Sam",
                "type": "camping",
                "location": "Salzburg North",
                "price_per_night_eur": 20.0,
                "amenities": ["shower", "kitchen", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.2,
                "notes": "On the Salzach river cycling route",
            }
        ],
        "hostel": [
            {
                "name": "YoHo International Youth Hostel",
                "type": "hostel",
                "location": "Linzergasse",
                "price_per_night_eur": 26.0,
                "amenities": ["shower", "kitchen", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "Popular Sound of Music screening nights",
            }
        ],
        "hotel": [
            {
                "name": "Hotel Stein",
                "type": "hotel",
                "location": "Altstadt",
                "price_per_night_eur": 115.0,
                "amenities": ["shower", "restaurant", "rooftop bar", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Rooftop views of the old city and castle",
            }
        ],
        "guesthouse": [
            {
                "name": "Pension Katarina",
                "type": "guesthouse",
                "location": "Schallmoos",
                "price_per_night_eur": 60.0,
                "amenities": ["shower", "breakfast", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.1,
                "notes": "Quiet area, 10 min cycle to Altstadt",
            }
        ],
    },
    "copenhagen": {
        "camping": [
            {
                "name": "Copenhagen Camping Bellahøj",
                "type": "camping",
                "location": "Bellahøj",
                "price_per_night_eur": 24.0,
                "amenities": ["shower", "kitchen", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.1,
                "notes": "3km from city centre, on cycling superhighway",
            }
        ],
        "hostel": [
            {
                "name": "Generator Copenhagen",
                "type": "hostel",
                "location": "Nørreport",
                "price_per_night_eur": 36.0,
                "amenities": ["shower", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "Excellent cycling city, Copenhagen is the bike capital",
            }
        ],
        "hotel": [
            {
                "name": "CPH Living",
                "type": "hotel",
                "location": "Harbour",
                "price_per_night_eur": 145.0,
                "amenities": ["shower", "breakfast", "harbour views", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Floating hotel, unique Copenhagen experience",
            }
        ],
        "guesthouse": [
            {
                "name": "Absalon Hotel",
                "type": "guesthouse",
                "location": "Vesterbro",
                "price_per_night_eur": 85.0,
                "amenities": ["shower", "breakfast", "bike hire", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "Family-run, free bike hire included",
            }
        ],
    },
    "bruges": {
        "camping": [
            {
                "name": "Camping Memling",
                "type": "camping",
                "location": "Sint-Michiels",
                "price_per_night_eur": 20.0,
                "amenities": ["shower", "kitchen", "bike storage"],
                "cycling_friendly": True,
                "rating": 4.0,
                "notes": "Flat Flanders cycling from the door",
            }
        ],
        "hostel": [
            {
                "name": "Charlie Rockets",
                "type": "hostel",
                "location": "City Centre",
                "price_per_night_eur": 28.0,
                "amenities": ["shower", "bar", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.3,
                "notes": "American diner/hostel combo in the heart of Bruges",
            }
        ],
        "hotel": [
            {
                "name": "Hotel De Orangerie",
                "type": "hotel",
                "location": "Canal Side",
                "price_per_night_eur": 135.0,
                "amenities": ["shower", "restaurant", "canal views", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.7,
                "notes": "15th century canalside gem",
            }
        ],
        "guesthouse": [
            {
                "name": "B&B Bariseele",
                "type": "guesthouse",
                "location": "City Centre",
                "price_per_night_eur": 75.0,
                "amenities": ["shower", "breakfast", "garden", "bike storage", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.8,
                "notes": "Beautiful historic house, excellent breakfast",
            }
        ],
    },
    "lisbon": {
        "camping": [
            {
                "name": "Orbitur Guincho",
                "type": "camping",
                "location": "Cascais",
                "price_per_night_eur": 18.0,
                "amenities": ["shower", "kitchen", "bike storage"],
                "cycling_friendly": True,
                "rating": 4.0,
                "notes": "Near the Atlantic coast cycling route",
            }
        ],
        "hostel": [
            {
                "name": "Lisbon Lounge Hostel",
                "type": "hostel",
                "location": "Chiado",
                "price_per_night_eur": 25.0,
                "amenities": ["shower", "kitchen", "terrace", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Award-winning hostel in historic district",
            }
        ],
        "hotel": [
            {
                "name": "Bairro Alto Hotel",
                "type": "hotel",
                "location": "Bairro Alto",
                "price_per_night_eur": 160.0,
                "amenities": ["shower", "restaurant", "bar", "spa", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.8,
                "notes": "Luxury boutique hotel in the cultural heart",
            }
        ],
        "guesthouse": [
            {
                "name": "Casa Amora",
                "type": "guesthouse",
                "location": "Mouraria",
                "price_per_night_eur": 70.0,
                "amenities": ["shower", "breakfast", "terrace", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Fado neighbourhood, excellent breakfast",
            }
        ],
    },
    "rome": {
        "camping": [
            {
                "name": "Camping Fabulous",
                "type": "camping",
                "location": "Rome Southwest",
                "price_per_night_eur": 18.0,
                "amenities": ["shower", "pool", "restaurant", "bike storage"],
                "cycling_friendly": True,
                "rating": 3.9,
                "notes": "Near the Via Appia Antica cycling route",
            }
        ],
        "hostel": [
            {
                "name": "The Beehive",
                "type": "hostel",
                "location": "Termini",
                "price_per_night_eur": 32.0,
                "amenities": ["shower", "kitchen", "garden", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Charming eco-friendly hostel near Termini",
            }
        ],
        "hotel": [
            {
                "name": "Hotel de Russie",
                "type": "hotel",
                "location": "Piazza del Popolo",
                "price_per_night_eur": 350.0,
                "amenities": ["shower", "restaurant", "spa", "garden", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.9,
                "notes": "Luxury with stunning gardens, bike hire available",
            }
        ],
        "guesthouse": [
            {
                "name": "Relais di Campagna",
                "type": "guesthouse",
                "location": "Prati",
                "price_per_night_eur": 90.0,
                "amenities": ["shower", "breakfast", "terrace", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.5,
                "notes": "Near the Vatican, on the Tiber cycling path",
            }
        ],
    },
    "florence": {
        "camping": [
            {
                "name": "Camping Michelangelo",
                "type": "camping",
                "location": "Piazzale Michelangelo",
                "price_per_night_eur": 20.0,
                "amenities": ["shower", "restaurant", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.2,
                "notes": "Stunning views over Florence",
            }
        ],
        "hostel": [
            {
                "name": "Plus Florence",
                "type": "hostel",
                "location": "Santa Croce",
                "price_per_night_eur": 28.0,
                "amenities": ["shower", "pool", "bar", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.4,
                "notes": "Great amenities, central location",
            }
        ],
        "hotel": [
            {
                "name": "AdAstra Florence",
                "type": "hotel",
                "location": "Oltrarno",
                "price_per_night_eur": 120.0,
                "amenities": ["shower", "breakfast", "courtyard", "bike hire", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.7,
                "notes": "Artisan neighbourhood, excellent bike hire",
            }
        ],
        "guesthouse": [
            {
                "name": "Soprarno Suites",
                "type": "guesthouse",
                "location": "Oltrarno",
                "price_per_night_eur": 80.0,
                "amenities": ["shower", "kitchen", "terrace", "Wi-Fi"],
                "cycling_friendly": True,
                "rating": 4.6,
                "notes": "Stylish Oltrarno apartments",
            }
        ],
    },
}


def _find_key(location: str) -> str | None:
    loc = location.lower().strip()
    for key in _DATA:
        if key in loc or loc in key:
            return key
    return None


def find_accommodation(location: str, type: AccommodationType) -> list[Accommodation]:
    """Find accommodation options at a given location filtered by type."""
    key = _find_key(location)
    if key and type in _DATA[key]:
        return [Accommodation(**a) for a in _DATA[key][type]]

    # Fallback
    price_map: dict[str, float] = {
        "camping": 18.0,
        "hostel": 28.0,
        "hotel": 110.0,
        "guesthouse": 65.0,
    }
    return [
        Accommodation(
            name=f"{location.title()} {type.title()}",
            type=type,
            location=location,
            price_per_night_eur=price_map[type],
            amenities=["shower", "Wi-Fi"],
            cycling_friendly=True,
            rating=3.8,
            notes=f"Estimated {type} accommodation in {location}. Book in advance.",
        )
    ]
