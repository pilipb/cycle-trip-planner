from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class VisaResult(BaseModel):
    passport_country: str
    destination_country: str
    visa_required: bool
    visa_type: str | None
    max_stay_days: int | None
    requirements: list[str]
    notes: str
    status: Literal["found", "estimated"]


# Schengen Area countries (for visa-free travel logic)
_SCHENGEN = {
    "austria", "belgium", "croatia", "czechia", "czech republic", "denmark",
    "estonia", "finland", "france", "germany", "greece", "hungary", "iceland",
    "italy", "latvia", "liechtenstein", "lithuania", "luxembourg", "malta",
    "netherlands", "norway", "poland", "portugal", "slovakia", "slovenia",
    "spain", "sweden", "switzerland",
}

# EU citizens who can travel freely in Schengen + EU
_EU_EEA = _SCHENGEN | {"ireland", "bulgaria", "cyprus", "romania"}

# Countries with 90/180 day Schengen visa-free access
_SCHENGEN_VISA_FREE = {
    "united kingdom", "uk", "britain",
    "united states", "usa", "us",
    "canada",
    "australia",
    "new zealand",
    "japan",
    "south korea",
    "singapore",
    "brazil",
    "argentina",
    "chile",
    "mexico",
    "israel",
    "hong kong",
    "taiwan",
}

_SPECIFIC_RULES: list[dict] = [
    {
        "passport": ("united kingdom", "uk", "britain"),
        "destination": ("france", "germany", "spain", "italy", "netherlands",
                        "belgium", "austria", "portugal", "czech republic", "czechia",
                        "switzerland", "denmark", "sweden", "norway", "finland",
                        "poland", "hungary", "croatia"),
        "data": {
            "visa_required": False,
            "visa_type": None,
            "max_stay_days": 90,
            "requirements": [
                "Valid British passport (must be valid for duration of stay)",
                "Proof of accommodation booked",
                "Proof of sufficient funds (approx €100/day recommended)",
                "Return or onward travel evidence if asked",
            ],
            "notes": (
                "Post-Brexit: UK passport holders can visit Schengen for up to 90 days "
                "in any 180-day period without a visa. ETIAS (European Travel Information "
                "and Authorisation System) is planned but not yet required as of 2026. "
                "No border restrictions for cyclists crossing between Schengen countries."
            ),
            "status": "found",
        },
    },
    {
        "passport": ("united states", "usa", "us", "american"),
        "destination": ("france", "germany", "spain", "italy", "netherlands",
                        "belgium", "austria", "portugal", "czech republic", "czechia",
                        "switzerland", "denmark", "sweden", "norway", "finland",
                        "poland", "hungary", "croatia"),
        "data": {
            "visa_required": False,
            "visa_type": None,
            "max_stay_days": 90,
            "requirements": [
                "Valid US passport",
                "Proof of sufficient funds",
                "Onward or return travel documentation if requested",
            ],
            "notes": (
                "US citizens can visit the Schengen Area visa-free for up to 90 days "
                "in any 180-day rolling period. Once inside Schengen, you can cross "
                "internal borders freely — ideal for a multi-country cycling tour."
            ),
            "status": "found",
        },
    },
    {
        "passport": ("canada", "canadian"),
        "destination": ("france", "germany", "spain", "italy", "netherlands",
                        "belgium", "austria", "portugal", "czech republic", "czechia",
                        "switzerland", "denmark"),
        "data": {
            "visa_required": False,
            "visa_type": None,
            "max_stay_days": 90,
            "requirements": ["Valid Canadian passport", "Proof of accommodation and funds"],
            "notes": (
                "Canadian citizens enjoy visa-free access to the Schengen Area "
                "for up to 90 days in a 180-day period."
            ),
            "status": "found",
        },
    },
    {
        "passport": ("australia", "australian"),
        "destination": ("france", "germany", "spain", "italy", "netherlands",
                        "belgium", "austria", "portugal", "czech republic", "czechia"),
        "data": {
            "visa_required": False,
            "visa_type": None,
            "max_stay_days": 90,
            "requirements": ["Valid Australian passport", "Proof of sufficient funds"],
            "notes": (
                "Australian citizens have visa-free access to the Schengen Area "
                "for tourism purposes up to 90 days."
            ),
            "status": "found",
        },
    },
]


def _normalize(s: str) -> str:
    return s.lower().strip()


def check_visa_requirements(passport_country: str, destination_country: str) -> VisaResult:
    """Check visa requirements for a given passport and destination country."""
    passport = _normalize(passport_country)
    destination = _normalize(destination_country)

    # EU/EEA citizens within EU/EEA: free movement
    if passport in _EU_EEA and destination in _EU_EEA:
        return VisaResult(
            passport_country=passport_country,
            destination_country=destination_country,
            visa_required=False,
            visa_type=None,
            max_stay_days=None,
            requirements=["Valid EU/EEA passport or national ID card"],
            notes=(
                "As an EU/EEA citizen you enjoy freedom of movement throughout the EU "
                "and Schengen Area. No visa, no time limit for stays under 3 months "
                "for tourism. Simply cross borders — no border checks within Schengen."
            ),
            status="found",
        )

    # Check specific rules
    for rule in _SPECIFIC_RULES:
        if passport in rule["passport"]:
            dest_match = any(
                d in destination or destination in d
                for d in rule["destination"]
            )
            if dest_match:
                return VisaResult(
                    passport_country=passport_country,
                    destination_country=destination_country,
                    **rule["data"],
                )

    # Generic visa-free for known countries entering Schengen
    if passport in _SCHENGEN_VISA_FREE and destination in _SCHENGEN:
        return VisaResult(
            passport_country=passport_country,
            destination_country=destination_country,
            visa_required=False,
            visa_type=None,
            max_stay_days=90,
            requirements=[
                "Valid passport with at least 6 months validity",
                "Proof of accommodation and sufficient funds",
            ],
            notes=(
                f"Citizens of {passport_country} can generally enter Schengen countries "
                "visa-free for up to 90 days. Verify current requirements with the "
                f"{destination_country} embassy before travelling."
            ),
            status="estimated",
        )

    # Unknown combination — estimated fallback
    return VisaResult(
        passport_country=passport_country,
        destination_country=destination_country,
        visa_required=True,
        visa_type="Tourist visa (estimated)",
        max_stay_days=90,
        requirements=[
            "Valid passport",
            "Completed visa application form",
            "Proof of accommodation",
            "Travel insurance",
            "Proof of sufficient funds",
            "Return ticket",
        ],
        notes=(
            f"Visa requirements for {passport_country} passport holders travelling to "
            f"{destination_country} are not confirmed in our database. Please check with "
            f"the {destination_country} embassy or consulate in your country well in advance."
        ),
        status="estimated",
    )
