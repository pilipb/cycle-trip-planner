from __future__ import annotations

from pydantic import BaseModel

from src.tools.accommodation import AccommodationType


class BudgetResult(BaseModel):
    daily_food_eur: float
    daily_accommodation_eur: float
    total_food_eur: float
    total_accommodation_eur: float
    miscellaneous_eur: float
    total_eur: float
    currency: str
    breakdown: list[str]
    notes: str


# Daily food budget by country (EUR)
_FOOD_COST: dict[str, float] = {
    "germany": 28.0,
    "france": 32.0,
    "netherlands": 30.0,
    "belgium": 28.0,
    "czech republic": 18.0,
    "czechia": 18.0,
    "austria": 28.0,
    "switzerland": 45.0,
    "italy": 26.0,
    "spain": 24.0,
    "portugal": 22.0,
    "hungary": 16.0,
    "poland": 15.0,
    "denmark": 38.0,
    "sweden": 36.0,
    "norway": 45.0,
    "finland": 34.0,
    "estonia": 20.0,
    "latvia": 18.0,
    "lithuania": 17.0,
    "slovakia": 17.0,
    "croatia": 20.0,
    "slovenia": 22.0,
}

# Base accommodation cost by type (EUR/night) — adjusted by country modifier
_ACCOMMODATION_BASE: dict[str, float] = {
    "camping": 18.0,
    "hostel": 28.0,
    "hotel": 110.0,
    "guesthouse": 65.0,
}

# Country cost modifier (1.0 = average West European prices)
_COST_MODIFIER: dict[str, float] = {
    "germany": 1.0,
    "france": 1.1,
    "netherlands": 1.1,
    "belgium": 1.0,
    "czech republic": 0.7,
    "czechia": 0.7,
    "austria": 1.05,
    "switzerland": 1.6,
    "italy": 0.95,
    "spain": 0.9,
    "portugal": 0.85,
    "hungary": 0.65,
    "poland": 0.65,
    "denmark": 1.3,
    "sweden": 1.25,
    "norway": 1.5,
    "finland": 1.2,
    "estonia": 0.8,
    "latvia": 0.75,
    "lithuania": 0.72,
    "slovakia": 0.68,
    "croatia": 0.85,
    "slovenia": 0.9,
}

# Miscellaneous daily cost by accommodation type (cycling gear, entries, transport)
_MISC_DAILY: dict[str, float] = {
    "camping": 8.0,
    "hostel": 10.0,
    "hotel": 15.0,
    "guesthouse": 12.0,
}


def _normalize(s: str) -> str:
    return s.lower().strip()


def _get_modifier(country: str) -> float:
    c = _normalize(country)
    for key, mod in _COST_MODIFIER.items():
        if key in c or c in key:
            return mod
    return 1.0  # default West European


def _get_food_cost(country: str) -> float:
    c = _normalize(country)
    for key, cost in _FOOD_COST.items():
        if key in c or c in key:
            return cost
    return 25.0  # default


def estimate_budget(
    distance_km: float,
    days: int,
    accommodation_type: AccommodationType,
    country: str,
) -> BudgetResult:
    """Estimate total trip budget based on distance, duration, accommodation, and country."""
    modifier = _get_modifier(country)
    daily_food = _get_food_cost(country)
    daily_accom = _ACCOMMODATION_BASE[accommodation_type] * modifier
    daily_misc = _MISC_DAILY[accommodation_type]

    total_food = daily_food * days
    total_accom = daily_accom * days
    total_misc = daily_misc * days
    total = total_food + total_accom + total_misc

    breakdown = [
        f"Food & drink: €{daily_food:.0f}/day × {days} days = €{total_food:.0f}",
        f"{accommodation_type.title()}: €{daily_accom:.0f}/night × {days} nights = €{total_accom:.0f}",
        f"Misc (entries, repairs, transport): €{daily_misc:.0f}/day × {days} days = €{total_misc:.0f}",
        f"Distance: {distance_km:.0f} km over {days} days (~{distance_km/days:.0f} km/day)",
    ]

    accom_tips = {
        "camping": "Camping keeps costs low. Wild camping is legal in some countries (check local rules).",
        "hostel": "Hostels offer great value with social atmosphere. Book ahead in peak season.",
        "hotel": "Hotels provide comfort but add significantly to costs. Consider mix with other options.",
        "guesthouse": "Guesthouses often include breakfast and local knowledge — good value mid-range.",
    }

    notes = (
        f"Budget estimate for {country}. "
        f"{accom_tips[accommodation_type]} "
        "Budget excludes: flights/trains to/from start/end, bike transport, travel insurance. "
        "Add 15–20% contingency for unexpected costs."
    )

    return BudgetResult(
        daily_food_eur=round(daily_food, 2),
        daily_accommodation_eur=round(daily_accom, 2),
        total_food_eur=round(total_food, 2),
        total_accommodation_eur=round(total_accom, 2),
        miscellaneous_eur=round(total_misc, 2),
        total_eur=round(total, 2),
        currency="EUR",
        breakdown=breakdown,
        notes=notes,
    )
