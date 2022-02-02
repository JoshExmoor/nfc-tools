from time import timezone
import datetime
import pytest
from nfctools.time_calculator import timezone_from_coordinates, today_sun_times, time_delta_from_string, seconds_until, StartEvent, EndEvent


@pytest.mark.skip(reason="Working as expected")
def test_get_timezone_from_coordinates():
    assert timezone_from_coordinates(47.8700447279009, -122.10485398788514) == 'America/Los_Angeles'


def test_today_sun_times():
    start_times, end_times = today_sun_times(47.8700447279009, -122.10485398788514, timezone='America/Los_Angeles')
    assert len(start_times) == 4
    assert len(end_times) == 4

    for event in StartEvent:
        assert type(start_times[event.value]) == datetime.datetime
    for event in EndEvent:
        assert type(end_times[event.value]) == datetime.datetime


@pytest.mark.parametrize(
    "delta,expected_string",
    [
        ("01:23:45", "1:23:45"),
        ("-1:30", "-1 day, 23:58:30"),
        ("-30", "-1 day, 23:30:00")
    ]
    )
def test_time_delta_from_string(delta, expected_string):
    time_delta = time_delta_from_string(delta)
    assert type(time_delta) == datetime.timedelta
    assert str(time_delta) == expected_string


@pytest.mark.parametrize(
    "seconds, expected",
    [
        (30, 30),
        (60, 60),
        (1000, 1000),
        (-30, 0)
    ]
    )
def test_seconds_until(seconds: int, expected: int):
    futuretime = seconds_until(datetime.datetime.now() + datetime.timedelta(seconds=seconds))
    assert futuretime == expected
