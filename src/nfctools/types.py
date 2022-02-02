from __future__ import annotations  # Fixes compatibility issues from earlier version of Python
import datetime
from enum import Enum
from dataclasses import dataclass


class UnexpectedLengthError(Exception):
    pass


class StartEvent(Enum):  # Important that these are ordered from earliest to latest event.
    SUNSET = "sunset"
    CIVILTWILIGHT = "civiltwilight"
    NAUTICALTWILIGHT = "nauticaltwilight"
    ASTROTWILIGHT = "astrotwilight"


class EndEvent(Enum):  # Important that these are ordered from earliest to latest event.
    ASTROTWILIGHT = "astrotwilight"
    NAUTICALTWILIGHT = "nauticaltwilight"
    CIVILTWILIGHT = "civiltwilight"
    SUNRISE = "sunrise"


@dataclass
class SunTimes(object):
    sunset: datetime.datetime
    end_civil_twilight: datetime.datetime
    end_nautical_twilight: datetime.datetime
    end_atro_twilight: datetime.datetime
    start_atro_twilight: datetime.datetime
    start_nautical_twilight: datetime.datetime
    start_civil_twilight: datetime.datetime
    sunrise: datetime.datetime

    @staticmethod
    def from_times_events(times: list[datetime.datetime], events: list[int]):
        return SunTimes(
            sunset=times[0],
            end_civil_twilight=times[1],
            end_nautical_twilight=times[2],
            end_atro_twilight=times[3],
            start_atro_twilight=times[4],
            start_nautical_twilight=times[5],
            start_civil_twilight=times[6],
            sunrise=times[7]
        )

