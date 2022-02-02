import argparse
import logging
import os
import sys

from .types import StartEvent, EndEvent


logging.basicConfig(level=logging.DEBUG)


def valid_startevent(event: str) -> str:
    return StartEvent(event).value


def valid_endevent(event: str) -> str:
    return EndEvent(event).value


def valid_lattitude(lattitude: str) -> float:
    if not -90.0 <= float(lattitude) <= 90.0:
        raise ValueError(f"Invalid Lattitude: {lattitude}")
    else:
        return float(lattitude)


def valid_longitude(longitude: str) -> float:
    if not -180.0 <= float(longitude) <= 180.0:
        raise ValueError(f"Invalid Lattitude: {longitude}")
    else:
        return float(longitude)


def parse_args(args: list):
    """Parse arguments passed to the CLI"""
    parser = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.HelpFormatter
        )

    parser.add_argument(
        "LATTITUDE",
        type=valid_lattitude,
        help="Rough lattitude of recording location. Used for calculating solar event time."
    )

    parser.add_argument(
        "LONGITUDE",
        type=valid_longitude,
        help="Rough longitude of recording location. Used for calculating solar event time."
    )

    parser.add_argument(
        "-trigger",
        "-t",
        nargs="?",
        default="astrotwilight",
        type=valid_startevent,
        choices=[event.value for event in list(StartEvent)],
        required=False,
        help="Event type to base recording start time off of. Ex: '-t sunset'"
        )

    parser.add_argument(
        "-end_trigger",
        "-e",
        default="astrotwilight",
        type=valid_endevent,
        choices=[event.value for event in list(EndEvent)],
        required=False,
        help="Event type to base recording end time off of. Ex: '-e sunrise'"
        )

    parser.add_argument(
        "-start_offset",
        "-so",
        required=False,
        help="Amount of time after/before event trigger to start recording. Use '-so=-00:00:00' syntax for negative (before) numbers.",
        )
    parser.add_argument(
        "-end_offset",
        "-eo",
        required=False,
        help="Amount of time after/before event trigger to end recording. Use '-eo=-00:00:00' syntax for negative (before) numbers.",
        )

    logging.debug(f"Parsing: {args}")
    return parser.parse_args(args)


def main() -> None:
    """
    Assists in recording and processing the Nocternal Flight Calls of migrating birds.
    Integrates with tools such as SoX (http://sox.sourceforge.net/) and
    BirdVoxDetect (https://github.com/BirdVox/birdvoxdetect) to automate NFC processes.
    """
    args = parse_args(sys.argv[1:])
    logging.debug(f"{args=}")


if __name__ == "__main__":
    main()
