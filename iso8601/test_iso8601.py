import iso8601
import unittest


class TestRegexes(unittest.TestCase):
    def test_iso8601_regex(self):
        assert iso8601.ISO8601_REGEX.match("2006-10-11T00:14:33Z")
    
    def test_timezone_regex(self):
        assert iso8601.TIMEZONE_REGEX.match("+01:00")
        assert iso8601.TIMEZONE_REGEX.match("+00:00")
        assert iso8601.TIMEZONE_REGEX.match("+01:20")
        assert iso8601.TIMEZONE_REGEX.match("-01:00")
    

class TestParsing(unittest.TestCase):
    def test_no_timezone(self):
        d = iso8601.parse_date("2006-10-20T15:34:56Z")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 15
        assert d.minute == 34
        assert d.second == 56
        assert d.tzinfo == iso8601.UTC
        
    def test_date(self):
        d = iso8601.parse_date("2006-10-20")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 0
        assert d.minute == 0
        assert d.second == 0
        assert d.tzinfo == iso8601.UTC
    
    def test_second_fraction(self):
        d = iso8601.parse_date("2006-10-20T15:34:56.123Z")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 15
        assert d.minute == 34
        assert d.second == 56
        assert d.microsecond == 123000
        assert d.tzinfo == iso8601.UTC
    
    def test_single_digit_month_and_day(self):
        d = iso8601.parse_date("2007-5-7T11:43:55.328Z'")
        assert d.year == 2007
        assert d.month == 5
        assert d.day == 7
        assert d.hour == 11
        assert d.minute == 43
        assert d.second == 55
        assert d.microsecond == 328000
        assert d.tzinfo == iso8601.UTC

    def test_timezone(self):
        d = iso8601.parse_date("2006-10-20T15:34:56.123+02:30")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 15
        assert d.minute == 34
        assert d.second == 56
        assert d.microsecond == 123000
        assert d.tzinfo.tzname(None) == "+02:30"

        offset = d.tzinfo.utcoffset(None)
        assert offset.days == 0
        assert offset.seconds == 60 * 60 * 2.5

    def test_negative_timezone(self):
        d = iso8601.parse_date("2006-10-20T15:34:56.123-02:30")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 15
        assert d.minute == 34
        assert d.second == 56
        assert d.microsecond == 123000
        assert d.tzinfo.tzname(None) == "-02:30"

        offset = d.tzinfo.utcoffset(None)
        assert offset.days == -1
        assert offset.seconds == 86400 - 60 * 60 * 2.5

    def test_two_digit_time_zone(self):
        d = iso8601.parse_date("2010-07-01 00:01:20+07")
        assert d.year == 2010
        assert d.month == 7
        assert d.day == 1
        assert d.hour == 0
        assert d.minute == 1
        assert d.second == 20
        assert d.tzinfo.tzname(None) == "+07"

        offset = d.tzinfo.utcoffset(None)
        assert offset.days == 0
        assert offset.seconds == 60 * 60 * 7
        
    def test_two_digit_negative_timezone(self):
        d = iso8601.parse_date("2010-07-01 00:01:20-07")
        assert d.year == 2010
        assert d.month == 7
        assert d.day == 1
        assert d.hour == 0
        assert d.minute == 1
        assert d.second == 20
        assert d.tzinfo.tzname(None) == "-07"

        offset = d.tzinfo.utcoffset(None)
        assert offset.days == -1
        assert offset.seconds == 86400 - 60 * 60 * 7

    def test_fractional_seconds_and_two_digit_timezone(self):
        d = iso8601.parse_date("2011-07-27 21:05:12.843248+07")
        assert d.year == 2011
        assert d.month == 7
        assert d.day == 27
        assert d.hour == 21
        assert d.minute == 5
        assert d.second == 12
        assert d.microsecond == 843248
        assert d.tzinfo.tzname(None) == "+07"

        offset = d.tzinfo.utcoffset(None)
        assert offset.days == 0
        assert offset.seconds == 60 * 60 * 7

    def test_fractional_seconds_and_two_digit_negative_timezone(self):
        d = iso8601.parse_date("2011-07-27 21:05:12.843248-07")
        assert d.year == 2011
        assert d.month == 7
        assert d.day == 27
        assert d.hour == 21
        assert d.minute == 5
        assert d.second == 12
        assert d.microsecond == 843248
        assert d.tzinfo.tzname(None) == "-07"

        offset = d.tzinfo.utcoffset(None)
        assert offset.days == -1
        assert offset.seconds == 86400 - 60 * 60 * 7
    
    def test_none(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, None)
    
    def test_invalid_date(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "23")
    
    def test_time_without_timezone(self):
        """Handle datetime string without timezone
        
        This tests what happens when you parse a date with no
        timezone. While not strictly correct according to the
        standard, this is quite common. I'll assume UTC for the time
        zone in this case.
        """
        d = iso8601.parse_date("2007-01-01T08:00:00")
        assert d.year == 2007
        assert d.month == 1
        assert d.day == 1
        assert d.hour == 8
        assert d.minute == 0
        assert d.second == 0
        assert d.microsecond == 0
        assert d.tzinfo == iso8601.UTC
    
    def test_no_timezone_different_default(self):
        tz = iso8601.FixedOffset(2, 0, "test offset")
        d = iso8601.parse_date("2007-01-01T08:00:00", default_timezone=tz)
        assert d.tzinfo == tz
    
    def test_space_separator(self):
        """Handle a separator other than T"""
        d = iso8601.parse_date("2007-06-23 06:40:34.00Z")
        assert d.year == 2007
        assert d.month == 6
        assert d.day == 23
        assert d.hour == 6
        assert d.minute == 40
        assert d.second == 34
        assert d.microsecond == 0
        assert d.tzinfo == iso8601.UTC


if __name__ == '__main__':
    unittest.main()
