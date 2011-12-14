"""ISO 8601 date time string parsing

Basic usage:
>>> import iso8601
>>> iso8601.parse_date("2007-01-25T12:00:00Z")
datetime.datetime(2007, 1, 25, 12, 0, tzinfo=<iso8601.iso8601.Utc ...>)
>>>
"""

from datetime import datetime, timedelta, tzinfo
import re

__all__ = ["parse_date", "ParseError"]


# Adapted from http://delete.me.uk/2005/03/iso8601.html
ISO8601_REGEX = re.compile('''
    (?P<year>[0-9]{4})
    (-
        (?P<month>[0-9]{1,2})
        (-
            (?P<day>[0-9]{1,2})
            (
                (?P<separator>.)
                (?P<hour>[0-9]{2})
                :
                (?P<minute>[0-9]{2})
                (:
                    (?P<second>[0-9]{2})
                    (\.(?P<fraction>[0-9]+))?
                )?
                (?P<timezone>Z
                            |(
                                ([-+])
                                ([0-9]{2})
                                :?([0-9]{2})?
                             )
                )?
            )?
        )?
    )?
''', re.VERBOSE)

TIMEZONE_REGEX = re.compile('''
    (?P<prefix>[+-])
    (?P<hours>[0-9]{2})
    .?
    (?P<minutes>[0-9]{2})
''', re.VERBOSE)


class ParseError(Exception):
    """Raised when there is a problem parsing a date string"""


ZERO = timedelta(0)

class Utc(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO

UTC = Utc()


class FixedOffset(tzinfo):
    """Fixed offset in hours and minutes from UTC"""

    def __init__(self, offset_hours, offset_minutes, name):
        self.__offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO
    
    def __repr__(self):
        return "<FixedOffset {0!r}>".format(self.__name)


def parse_timezone(tzstring, default_timezone=UTC):
    """Parses ISO 8601 time zone specs into tzinfo offsets"""
    # This isn't strictly correct when a time is included (according to the ISO
    # standard), but we don't know here if the time is included.
    if tzstring == "Z" or tzstring is None:
        return default_timezone

    m = TIMEZONE_REGEX.match(tzstring)
    prefix, hours, minutes = m.groups()
    hours = int(hours)
    minutes = int(minutes) if minutes is not None else 0

    if prefix == "-":
        hours = -hours
        minutes = -minutes

    return FixedOffset(hours, minutes, tzstring)


def parse_date(datestring, default_timezone=UTC):
    """Parses ISO 8601 dates into datetime objects
    
    The timezone is parsed from the date string. However it is quite
    common to have dates without a timezone (not strictly correct). In
    this case the default timezone specified in default_timezone is
    used. This is UTC by default.
    """
    if not isinstance(datestring, basestring):
        raise ParseError("Expecting a string {0!r}".format(datestring))

    m = ISO8601_REGEX.match(datestring)

    if not m:
        raise ParseError("Unable to parse date string {0!r}".format(datestring))

    groups = m.groupdict()
    tz = parse_timezone(groups["timezone"], default_timezone=default_timezone)

    if groups["fraction"] is None:
        fraction = 0
    else:
        fraction = int(float("0.{0}".format(groups["fraction"])) * 1e6)
    
    default = lambda k, d=0: int(groups[k]) if groups[k] is not None else d

    return datetime(
        default('year'),
        default('month', 1),
        default('day', 1),
        default('hour'),
        default('minute'),
        default('second'),
        fraction,
        tz)
