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
    def test_year(self):
        d = iso8601.parse_date("2006")
        assert d.year == 2006
        assert d.month == 1
        assert d.day == 1
        assert d.hour == 0
        assert d.minute == 0
        assert d.second == 0
        assert d.tzinfo == iso8601.UTC

    def test_year_month(self):
        d = iso8601.parse_date("2006-10")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 1
        assert d.hour == 0
        assert d.minute == 0
        assert d.second == 0
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

    def test_hours_minutes(self):
        d = iso8601.parse_date("2006-10-20T11:30+10:00")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 11
        assert d.minute == 30
        assert d.second == 0
        assert d.tzinfo.tzname(None) == "+10:00"

    def test_seconds(self):
        d = iso8601.parse_date("2006-10-20T11:30:32+10:00")
        assert d.year == 2006
        assert d.month == 10
        assert d.day == 20
        assert d.hour == 11
        assert d.minute == 30
        assert d.second == 32
        assert d.tzinfo.tzname(None) == "+10:00"

    def test_fractional_second(self):
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


class TestInvalid(unittest.TestCase):
    def test_none(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, None)
    
    def test_bad_date(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "23")

    def test_long_second(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "2006-10-20T15:34:562Z")

    def test_long_minute(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "2006-10-20T15:342:56Z")

    def test_long_hour(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "2006-10-20T152:34:56Z")

    def test_long_day(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "2006-10-202T15:34:56Z")

    def test_long_month(self):
        self.assertRaises(iso8601.ParseError, iso8601.parse_date, "2006-102-20T15:34:56Z")
    

if __name__ == '__main__':
    unittest.main()
