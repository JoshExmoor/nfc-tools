from datetime import timedelta
import pytest
from nfctools.cli import main, parse_args, StartEvent, EndEvent, valid_lattitude, valid_longitude


@pytest.mark.parametrize(
    "event",
    ["sunset", "astrotwilight", "nauticaltwilight", "civiltwilight"]
    )
def test_startevent(event):
    event_obj = StartEvent(event)
    assert event_obj


with pytest.raises(ValueError):
    test_startevent("night")


@pytest.mark.parametrize(
    "event",
    ["sunrise", "astrotwilight", "nauticaltwilight", "civiltwilight"]
    )
def test_endevent(event):
    event_obj = EndEvent(event)
    assert event_obj


with pytest.raises(ValueError):
    test_startevent("day")


@pytest.mark.parametrize(
    "lattitude",
    [0, 90, -90, -15.2502324, 69.420]
    )
def test_lattitude(lattitude):
    lattitude_obj = valid_lattitude(lattitude)
    assert lattitude_obj == lattitude


with pytest.raises(ValueError):
    test_lattitude(-91.9)


@pytest.mark.parametrize(
    "longitude",
    [0, 180, -180, -125.2502324, -90, -179.999]
    )
def test_longitude(longitude):
    longitude_obj = valid_longitude(longitude)
    assert longitude_obj == longitude


with pytest.raises(ValueError):
    longitude = test_longitude(191.1)


class cli_args_defaults:
    end_offset = None
    end_trigger = 'astrotwilight'
    start_offset = None
    trigger = 'astrotwilight'


@pytest.mark.parametrize(
    "args,expected",
    [
        ("40.781227991355486 -73.96703951393317".split(), [40.781227991355486, -73.96703951393317])
    ]
    )
def test_parse_args_simple_default(args, expected):
    args = parse_args(args)
    assert args.LATTITUDE == expected[0]
    assert args.LONGITUDE == expected[1]
    assert args.end_offset == cli_args_defaults.end_offset
    assert args.end_trigger == cli_args_defaults.end_trigger
    assert args.start_offset == cli_args_defaults.start_offset
    assert args.trigger == cli_args_defaults.trigger


@pytest.mark.parametrize(
    "args,expected",
    [
        (
            "40.781227991355486 -73.96703951393317 -t sunset".split(),
            {
                'LATTITUDE': 40.781227991355486,
                'LONGITUDE': -73.96703951393317,
                'trigger': 'sunset',
                'start_offset': cli_args_defaults.start_offset,
                'end_trigger': cli_args_defaults.end_trigger,
                'end_offset': cli_args_defaults.end_offset
            }
        ),
        (
            " -t sunset 40.781227991355486 -73.96703951393317".split(),
            {
                'LATTITUDE': 40.781227991355486,
                'LONGITUDE': -73.96703951393317,
                'trigger': 'sunset',
                'start_offset': cli_args_defaults.start_offset,
                'end_trigger': cli_args_defaults.end_trigger,
                'end_offset': cli_args_defaults.end_offset
            }
        ),
        (
            " -trigger astrotwilight -e sunrise 40.781227991355486 -73.96703951393317".split(),
            {
                'LATTITUDE': 40.781227991355486,
                'LONGITUDE': -73.96703951393317,
                'trigger': 'astrotwilight',
                'start_offset': cli_args_defaults.start_offset,
                'end_trigger': 'sunrise',
                'end_offset': cli_args_defaults.end_offset
            }
        ),
        (
            " -trigger astrotwilight -e sunrise -so=-15:30 40.781227991355486 -73.96703951393317".split(),
            {
                'LATTITUDE': 40.781227991355486,
                'LONGITUDE': -73.96703951393317,
                'trigger': 'astrotwilight',
                'start_offset': '-15:30',
                'end_trigger': 'sunrise',
                'end_offset': cli_args_defaults.end_offset
            }
        ),
        (
            " -trigger astrotwilight -e sunrise -so=-15:30 -eo 15:30 40.781227991355486 -73.96703951393317".split(),
            {
                'LATTITUDE': 40.781227991355486,
                'LONGITUDE': -73.96703951393317,
                'trigger': 'astrotwilight',
                'start_offset': '-15:30',
                'end_trigger': 'sunrise',
                'end_offset': '15:30'
            }
        )

    ]
    )
def test_parse_args_multitest(args, expected):
    args = parse_args(args)
    assert args.LATTITUDE == expected['LATTITUDE']
    assert args.LONGITUDE == expected['LONGITUDE']
    assert args.trigger == expected['trigger']
    assert args.end_offset == expected['end_offset']
    assert args.end_trigger == expected['end_trigger']
    assert args.start_offset == expected['start_offset']
