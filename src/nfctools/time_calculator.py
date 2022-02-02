from __future__ import annotations  # Fixes compatibility issues from earlier version of Python
import datetime
import logging
from time import time

import pytz  # Add to requirements
from tzwhere import tzwhere  # Add to requirements
from skyfield import almanac  # Add to requirements
from skyfield.api import load, wgs84  # Add to requirements
from .types import StartEvent, EndEvent, UnexpectedLengthError


def timezone_from_coordinates(latitude: float, longitude: float) -> str:  # Returns time zone as string
    timezone = tzwhere.tzwhere()
    return timezone.tzNameAt(latitude, longitude)


def time_delta_from_string(delta: str) -> datetime.timedelta:
    split_delta = [int(i) for i in delta.split(":")]

    # If time delta is negative (ex. -01:00:00), set all time fields to negative:
    if split_delta[0] < 0:
        split_delta = [-abs(i) for i in split_delta]

    if len(split_delta) == 3:  # 00:00:00, assume HH:MM:SS
        return datetime.timedelta(hours=split_delta[0], minutes=split_delta[1], seconds=split_delta[2])
    elif len(split_delta) == 2:  # 00:00, assume MM:SS
        return datetime.timedelta(minutes=split_delta[0], seconds=split_delta[1])
    elif len(split_delta) == 1:  # 00, assume MM
        return datetime.timedelta(minutes=split_delta[0])
    else:
        raise ValueError("Invalid Time Delta")


def seconds_until(futuretime: datetime.datetime) -> int:
    delta = futuretime - datetime.datetime.now()
    if delta.total_seconds() <= 0:  # If time is in the past.
        return 0
    else:
        return round(delta.total_seconds(), 0)


def today_sun_times(latitude: float, longitude: float, timezone: str = None, day: datetime.datetime = datetime.datetime.now()) -> tuple[dict, dict]:
    """
    Gather dark_twilight_day events occuring from noon on the current day until noon the next day.
    Should return two dicts containing times which match up with StartEvent and EndEvent values.
    """
    zone = pytz.timezone(timezone)
    now = zone.localize(datetime.datetime.now())
    noon = now.replace(hour=12, minute=0, second=0, microsecond=0)  # Today @ noon
    next_noon = noon + datetime.timedelta(days=1)  # Tomorrow @ noon

    ts = load.timescale()
    t0 = ts.from_datetime(noon)
    t1 = ts.from_datetime(next_noon)
    eph = load('de421.bsp')
    location = wgs84.latlon(latitude, longitude)

    f = almanac.dark_twilight_day(eph, location)
    times, events = almanac.find_discrete(t0, t1, f)
    logging.debug(f"{times=}\n{events=}")

    local_times = []
    for sky_time in times:
        local_times.append(sky_time.astimezone(zone))

    # Simple loop to print times in debug strings:
    previous_e = f(t0).item()
    for t, e in zip(times, events):
        tstr = str(t.astimezone(zone))[:16]
        if previous_e < e:
            logging.debug(tstr, ' ', almanac.TWILIGHTS[e], 'starts', e)
        else:
            logging.debug(tstr, ' ', almanac.TWILIGHTS[previous_e], 'ends', e)
        previous_e = e

    return format_solar_events(local_times, events)


def format_solar_events(times: list[datetime.datetime], events: list[int]) -> tuple(dict, dict):
    expected_length = len(StartEvent) + len(EndEvent)
    if len(times) != expected_length:
        raise UnexpectedLengthError

    start_times = {}
    end_times = {}
    i = 0
    for start_event in StartEvent:
        start_times[start_event.value] = times[i]
        i += 0
    for end_event in EndEvent:
        end_times[end_event.value] = times[i]
        i += 0
    return start_times, end_times
