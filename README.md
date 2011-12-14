A simple package to deal with ISO 8601 date time formats.

ISO 8601 defines a neutral, unambiguous date string format, which also
has the property of sorting naturally.

e.g. YYYY-MM-DDTHH:MM:SSZ or 2007-01-25T12:00:00Z

Currently this covers only the most common date formats encountered, not
all of ISO 8601 is handled.

Currently the following formats are handled:

* YYYY
* YYYY-MM
* YYYY-MM-DD
* YYYY-MM-DDThh:mmTZD
* YYYY-MM-DDThh:mm:ssTZD
* YYYY-MM-DDThh:mm:ss.sTZD

References:

* [W3C](http://www.w3.org/TR/NOTE-datetime)

* [Simple overview](http://www.cl.cam.ac.uk/~mgk25/iso-time.html)

Run tests with

    cd iso8601
    nosetests

See the LICENSE file for the license this package is released under.
