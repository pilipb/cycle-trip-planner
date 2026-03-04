from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

WeatherSuitability = Literal["excellent", "good", "fair", "challenging"]


class WeatherResult(BaseModel):
    location: str
    month: str
    avg_temp_celsius: float
    min_temp_celsius: float
    max_temp_celsius: float
    rainfall_mm: float
    sunny_days: int
    wind_speed_kmh: float
    conditions: str
    cycling_suitability: WeatherSuitability


# Month name normalisation
_MONTH_MAP: dict[str, str] = {
    "january": "january", "jan": "january", "1": "january",
    "february": "february", "feb": "february", "2": "february",
    "march": "march", "mar": "march", "3": "march",
    "april": "april", "apr": "april", "4": "april",
    "may": "may", "5": "may",
    "june": "june", "jun": "june", "6": "june",
    "july": "july", "jul": "july", "7": "july",
    "august": "august", "aug": "august", "8": "august",
    "september": "september", "sep": "september", "sept": "september", "9": "september",
    "october": "october", "oct": "october", "10": "october",
    "november": "november", "nov": "november", "11": "november",
    "december": "december", "dec": "december", "12": "december",
}

# (avg, min, max, rain_mm, sunny_days, wind_kmh, conditions, suitability)
_W = tuple[float, float, float, float, int, float, str, WeatherSuitability]

_WEATHER_DB: dict[str, dict[str, _W]] = {
    "berlin": {
        "january":   (1.0, -3.0, 5.0,   42, 5,  15.0, "Cold, possible snow and frost",          "challenging"),
        "february":  (2.5, -2.0, 7.0,   33, 7,  14.0, "Cold and variable",                       "challenging"),
        "march":     (7.0,  2.0, 13.0,  38, 11, 13.0, "Cool, improving conditions",              "fair"),
        "april":     (13.0, 6.0, 20.0,  40, 15, 12.0, "Mild and pleasant",                       "good"),
        "may":       (18.0,10.0, 25.0,  48, 18, 11.0, "Warm, occasional showers",                "good"),
        "june":      (21.0,13.0, 28.0,  62, 19, 10.0, "Warm with afternoon thunderstorms",       "good"),
        "july":      (23.0,15.0, 30.0,  56, 20,  9.0, "Warm, some heat waves",                   "excellent"),
        "august":    (22.0,14.0, 29.0,  55, 19,  9.0, "Warm and pleasant",                       "excellent"),
        "september": (17.0,10.0, 24.0,  45, 16, 10.0, "Mild, ideal cycling weather",             "excellent"),
        "october":   (12.0, 6.0, 18.0,  37, 12, 12.0, "Cool and crisp",                          "good"),
        "november":  (6.0,  1.0, 11.0,  42, 7,  13.0, "Cold and wet",                            "fair"),
        "december":  (2.0, -2.0, 6.0,   43, 4,  14.0, "Cold, possible frost",                    "challenging"),
    },
    "prague": {
        "january":   (0.0, -4.0, 4.0,   21, 4,  13.0, "Cold, possible snow",                    "challenging"),
        "february":  (1.5, -3.0, 6.0,   18, 6,  12.0, "Cold with occasional thaw",              "challenging"),
        "march":     (6.0,  0.0, 12.0,  27, 10, 13.0, "Cool and variable",                      "fair"),
        "april":     (12.0, 5.0, 19.0,  35, 14, 12.0, "Mild, pleasant cycling",                 "good"),
        "may":       (17.0, 9.0, 25.0,  52, 17, 11.0, "Warm, some showers",                     "good"),
        "june":      (21.0,13.0, 28.0,  67, 18, 10.0, "Warm with thunderstorms",                "good"),
        "july":      (23.0,15.0, 30.0,  64, 19,  9.0, "Warm, best month for cycling",           "excellent"),
        "august":    (22.0,14.0, 29.0,  65, 18,  9.0, "Warm and pleasant",                      "excellent"),
        "september": (17.0,10.0, 24.0,  42, 15, 10.0, "Mild, excellent cycling",                "excellent"),
        "october":   (11.0, 5.0, 17.0,  30, 11, 12.0, "Cool, autumnal colours",                 "good"),
        "november":  (5.0,  0.0, 10.0,  32, 6,  13.0, "Cold and wet",                           "fair"),
        "december":  (1.0, -3.0, 5.0,   23, 4,  13.0, "Cold, possibly snowy",                   "challenging"),
    },
    "amsterdam": {
        "january":   (4.0,  1.0, 7.0,   63, 4,  18.0, "Cold and damp, windy",                   "challenging"),
        "february":  (4.5,  1.0, 8.0,   48, 6,  17.0, "Cold, variable",                         "challenging"),
        "march":     (8.0,  3.0, 12.0,  60, 9,  16.0, "Cool and showery",                       "fair"),
        "april":     (12.0, 6.0, 17.0,  45, 13, 15.0, "Mild, tulip season",                     "good"),
        "may":       (16.0,10.0, 21.0,  52, 16, 14.0, "Warm and pleasant",                      "good"),
        "june":      (19.0,13.0, 24.0,  68, 17, 13.0, "Warm, occasional rain",                  "good"),
        "july":      (21.0,15.0, 26.0,  75, 18, 12.0, "Warm, best cycling month",               "excellent"),
        "august":    (21.0,15.0, 26.0,  83, 17, 12.0, "Warm, some rain",                        "excellent"),
        "september": (17.0,11.0, 22.0,  70, 14, 13.0, "Mild, pleasant",                         "good"),
        "october":   (13.0, 7.0, 18.0,  80, 10, 15.0, "Cool and wet",                           "fair"),
        "november":  (8.0,  4.0, 13.0,  83, 5,  17.0, "Cold and very wet",                      "challenging"),
        "december":  (5.0,  1.0, 8.0,   73, 3,  18.0, "Cold, short days",                       "challenging"),
    },
    "paris": {
        "january":   (5.0,  2.0, 9.0,   51, 5,  14.0, "Cold and grey",                          "challenging"),
        "february":  (6.0,  2.0, 10.0,  41, 7,  13.0, "Cold, variable",                         "fair"),
        "march":     (10.0, 5.0, 15.0,  48, 11, 13.0, "Mild and variable",                      "fair"),
        "april":     (14.0, 8.0, 19.0,  52, 14, 12.0, "Pleasant, some showers",                 "good"),
        "may":       (18.0,12.0, 24.0,  64, 17, 11.0, "Warm and lovely",                        "good"),
        "june":      (21.0,15.0, 27.0,  55, 19, 10.0, "Warm, best month",                       "excellent"),
        "july":      (24.0,17.0, 30.0,  63, 21,  9.0, "Hot, can be very warm",                  "excellent"),
        "august":    (24.0,17.0, 30.0,  43, 21,  9.0, "Hot and dry",                            "excellent"),
        "september": (20.0,13.0, 26.0,  55, 17, 10.0, "Mild, excellent cycling",                "excellent"),
        "october":   (14.0, 9.0, 20.0,  59, 12, 12.0, "Cool, autumnal",                         "good"),
        "november":  (9.0,  5.0, 13.0,  55, 6,  13.0, "Cold and wet",                           "fair"),
        "december":  (6.0,  2.0, 9.0,   55, 4,  13.0, "Cold, festive",                          "challenging"),
    },
    "munich": {
        "january":   (-1.0,-6.0, 4.0,   57, 4,  11.0, "Cold, snowy, Alps visible",              "challenging"),
        "february":  (1.0, -5.0, 7.0,   46, 6,  12.0, "Cold with possible snow",                "challenging"),
        "march":     (6.0, -1.0, 13.0,  55, 10, 13.0, "Cool, warming up",                       "fair"),
        "april":     (11.0, 4.0, 18.0,  68, 14, 12.0, "Mild, some rain",                        "good"),
        "may":       (16.0, 8.0, 23.0,  87, 17, 11.0, "Warm, occasional storms",                "good"),
        "june":      (19.0,12.0, 26.0,  122, 17, 10.0, "Warm with thunderstorms",               "good"),
        "july":      (21.0,14.0, 28.0,  124, 18,  9.0, "Warm, thunderstorm risk",               "good"),
        "august":    (21.0,14.0, 28.0,  110, 18,  9.0, "Warm, pleasant",                        "excellent"),
        "september": (16.0,10.0, 23.0,  78, 15, 10.0, "Mild, Oktoberfest time",                 "excellent"),
        "october":   (10.0, 5.0, 16.0,  60, 11, 12.0, "Cool, colourful foliage",                "good"),
        "november":  (4.0, -1.0, 9.0,   63, 5,  12.0, "Cold and grey",                          "fair"),
        "december":  (0.0, -5.0, 5.0,   65, 3,  12.0, "Cold, Christmas markets",                "challenging"),
    },
    "vienna": {
        "january":   (1.0, -3.0, 5.0,   37, 5,  12.0, "Cold, possible snow",                   "challenging"),
        "february":  (3.0, -2.0, 8.0,   36, 7,  13.0, "Cold and variable",                     "challenging"),
        "march":     (8.0,  2.0, 14.0,  44, 11, 14.0, "Cool, improving",                       "fair"),
        "april":     (14.0, 7.0, 20.0,  45, 15, 13.0, "Mild, pleasant",                        "good"),
        "may":       (19.0,12.0, 26.0,  65, 18, 12.0, "Warm, some storms",                     "good"),
        "june":      (22.0,16.0, 28.0,  75, 19, 11.0, "Warm with thunderstorms",               "good"),
        "july":      (24.0,18.0, 30.0,  70, 20, 10.0, "Hot and sunny",                         "excellent"),
        "august":    (24.0,17.0, 30.0,  68, 20, 10.0, "Hot and pleasant",                      "excellent"),
        "september": (19.0,13.0, 25.0,  47, 16, 11.0, "Mild, best cycling month",              "excellent"),
        "october":   (13.0, 7.0, 19.0,  45, 12, 12.0, "Cool, autumnal",                        "good"),
        "november":  (7.0,  3.0, 11.0,  44, 6,  13.0, "Cold and damp",                         "fair"),
        "december":  (2.0, -2.0, 6.0,   45, 4,  12.0, "Cold, Christmas markets",               "challenging"),
    },
    "budapest": {
        "january":   (2.0, -2.0, 6.0,   37, 4,  10.0, "Cold, possible snow",                   "challenging"),
        "february":  (4.0, -1.0, 9.0,   33, 6,  11.0, "Cold and variable",                     "challenging"),
        "march":     (10.0, 3.0, 17.0,  30, 11, 12.0, "Cool, warming fast",                    "fair"),
        "april":     (16.0, 8.0, 23.0,  43, 15, 11.0, "Mild and pleasant",                     "good"),
        "may":       (21.0,13.0, 28.0,  60, 18, 10.0, "Warm, some storms",                     "good"),
        "june":      (24.0,17.0, 31.0,  68, 19,  9.0, "Warm with afternoon storms",            "good"),
        "july":      (26.0,18.0, 33.0,  50, 22,  8.0, "Hot, possible heat wave",               "excellent"),
        "august":    (26.0,18.0, 33.0,  55, 21,  8.0, "Hot and sunny",                         "excellent"),
        "september": (20.0,13.0, 27.0,  38, 17,  9.0, "Warm, ideal cycling",                   "excellent"),
        "october":   (14.0, 7.0, 20.0,  37, 13, 10.0, "Mild and pleasant",                     "good"),
        "november":  (7.0,  2.0, 12.0,  47, 6,  11.0, "Cold and damp",                         "fair"),
        "december":  (3.0, -1.0, 7.0,   43, 3,  10.0, "Cold, festive",                         "challenging"),
    },
    "copenhagen": {
        "january":   (2.0, -1.0, 5.0,   49, 4,  17.0, "Cold, windy and damp",                  "challenging"),
        "february":  (2.0, -1.0, 5.0,   36, 6,  16.0, "Cold and variable",                     "challenging"),
        "march":     (5.0,  1.0, 9.0,   44, 9,  16.0, "Cool and showery",                      "fair"),
        "april":     (10.0, 4.0, 15.0,  40, 14, 14.0, "Mild, pleasant",                        "good"),
        "may":       (15.0, 8.0, 20.0,  43, 17, 13.0, "Warm and lovely",                       "good"),
        "june":      (18.0,12.0, 23.0,  52, 18, 12.0, "Warm, long days",                       "excellent"),
        "july":      (20.0,14.0, 25.0,  65, 19, 11.0, "Warm, best month",                      "excellent"),
        "august":    (20.0,14.0, 25.0,  66, 18, 11.0, "Warm and pleasant",                     "excellent"),
        "september": (16.0,10.0, 21.0,  62, 14, 13.0, "Mild, still good",                      "good"),
        "october":   (11.0, 6.0, 15.0,  66, 9,  14.0, "Cool and wet",                          "fair"),
        "november":  (6.0,  3.0, 9.0,   65, 5,  16.0, "Cold and dark",                         "challenging"),
        "december":  (3.0,  0.0, 6.0,   51, 3,  17.0, "Cold, very short days",                 "challenging"),
    },
    "lisbon": {
        "january":   (12.0, 8.0, 16.0,  96, 13, 14.0, "Mild, rainy season",                    "fair"),
        "february":  (13.0, 9.0, 17.0,  75, 14, 14.0, "Mild, some rain",                       "fair"),
        "march":     (15.0,11.0, 19.0,  68, 17, 15.0, "Mild and pleasant",                     "good"),
        "april":     (17.0,12.0, 21.0,  64, 18, 14.0, "Warm, spring flowers",                  "good"),
        "may":       (20.0,15.0, 25.0,  44, 21, 13.0, "Warm and sunny",                        "excellent"),
        "june":      (23.0,18.0, 28.0,  16, 25, 14.0, "Hot and dry",                           "excellent"),
        "july":      (26.0,20.0, 31.0,   3, 28, 16.0, "Hot, dry and sunny",                    "excellent"),
        "august":    (26.0,21.0, 32.0,   4, 27, 16.0, "Very hot and dry",                      "good"),
        "september": (24.0,19.0, 29.0,  35, 23, 14.0, "Warm and pleasant",                     "excellent"),
        "october":   (20.0,15.0, 25.0,  80, 19, 13.0, "Mild, some rain",                       "good"),
        "november":  (15.0,11.0, 20.0, 100, 14, 14.0, "Mild, wet",                             "fair"),
        "december":  (13.0, 9.0, 17.0,  93, 11, 14.0, "Mild, rainy",                           "fair"),
    },
    "rome": {
        "january":   (8.0,  4.0, 13.0,  71, 11, 12.0, "Cool and sometimes rainy",              "fair"),
        "february":  (9.0,  4.0, 14.0,  62, 12, 13.0, "Cool, variable",                        "fair"),
        "march":     (12.0, 6.0, 18.0,  57, 15, 14.0, "Mild and pleasant",                     "good"),
        "april":     (16.0,10.0, 22.0,  51, 17, 13.0, "Warm, spring time",                     "good"),
        "may":       (20.0,13.0, 27.0,  38, 21, 12.0, "Warm and sunny",                        "excellent"),
        "june":      (24.0,17.0, 30.0,  22, 24, 11.0, "Hot and dry",                           "excellent"),
        "july":      (27.0,20.0, 33.0,  15, 28, 11.0, "Very hot and dry",                      "good"),
        "august":    (27.0,20.0, 33.0,  21, 27, 11.0, "Very hot, can be oppressive",           "fair"),
        "september": (23.0,17.0, 29.0,  68, 22, 11.0, "Warm and pleasant",                     "excellent"),
        "october":   (18.0,13.0, 24.0,  93, 17, 12.0, "Mild, some rain",                       "good"),
        "november":  (13.0, 8.0, 18.0, 103, 11, 12.0, "Cool and wet",                          "fair"),
        "december":  (9.0,  5.0, 14.0,  81, 10, 12.0, "Cool, festive",                         "fair"),
    },
    "barcelona": {
        "january":   (9.0,  5.0, 14.0,  42, 12, 13.0, "Mild and sometimes sunny",              "good"),
        "february":  (10.0, 6.0, 15.0,  36, 13, 14.0, "Mild, variable",                        "good"),
        "march":     (12.0, 8.0, 17.0,  48, 16, 15.0, "Mild, pleasant",                        "good"),
        "april":     (15.0,11.0, 20.0,  48, 17, 14.0, "Warm, spring",                          "excellent"),
        "may":       (19.0,14.0, 24.0,  51, 20, 13.0, "Warm and pleasant",                     "excellent"),
        "june":      (23.0,18.0, 28.0,  37, 23, 13.0, "Hot and sunny",                         "excellent"),
        "july":      (26.0,21.0, 31.0,  20, 27, 13.0, "Hot and dry",                           "good"),
        "august":    (26.0,21.0, 31.0,  46, 25, 13.0, "Hot, some storms",                      "good"),
        "september": (23.0,18.0, 28.0,  83, 20, 13.0, "Warm, good for cycling",                "excellent"),
        "october":   (18.0,14.0, 23.0,  91, 17, 13.0, "Mild, some rain",                       "good"),
        "november":  (13.0, 9.0, 18.0,  57, 13, 13.0, "Mild",                                  "good"),
        "december":  (10.0, 6.0, 14.0,  51, 11, 13.0, "Mild, festive",                         "good"),
    },
}


def _normalize_month(month: str) -> str | None:
    return _MONTH_MAP.get(month.lower().strip())


def _find_location_key(location: str) -> str | None:
    loc = location.lower().strip()
    for key in _WEATHER_DB:
        if key in loc or loc in key:
            return key
    return None


def get_weather(location: str, month: str) -> WeatherResult:
    """Get weather forecast and cycling suitability for a location and month."""
    norm_month = _normalize_month(month)
    if norm_month is None:
        norm_month = "july"  # default to July if month unrecognised

    key = _find_location_key(location)
    if key and norm_month in _WEATHER_DB[key]:
        avg, mn, mx, rain, sunny, wind, cond, suit = _WEATHER_DB[key][norm_month]
        return WeatherResult(
            location=location,
            month=norm_month.capitalize(),
            avg_temp_celsius=avg,
            min_temp_celsius=mn,
            max_temp_celsius=mx,
            rainfall_mm=rain,
            sunny_days=sunny,
            wind_speed_kmh=wind,
            conditions=cond,
            cycling_suitability=suit,
        )

    # Fallback: generic temperate European estimate
    month_display = norm_month.capitalize() if norm_month else month.capitalize()
    return WeatherResult(
        location=location,
        month=month_display,
        avg_temp_celsius=15.0,
        min_temp_celsius=8.0,
        max_temp_celsius=22.0,
        rainfall_mm=55.0,
        sunny_days=14,
        wind_speed_kmh=12.0,
        conditions="Typical temperate European weather, variable conditions",
        cycling_suitability="good",
    )
