# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Parses dates from the first page of a thesis.

TODO:
    Make parser more tolerant, if nothing matches, reduces accuracy due
    reduce the search pattern like Januar -> Janua, Janu, .. Jan..

    Refactor and think about new concept
"""

import calendar
import functools
import re

import german
import iamraw
import utila

re_search = functools.partial(re.search, flags=re.VERBOSE | re.IGNORECASE)  # pylint:disable=C0103


def parse(raw: str) -> iamraw.TitleDate:
    """Convert `raw` line to `TitleDate`

    Args:
        raw(str): extracted line of pdf document
    Returns:
        return parsed TitleDate - return None if parsing is not possible
    """

    # Require different regex
    # Judge function to decide when having multiple results
    simple_alpha_date_month_first = functools.partial(
        simple_alpha_date,
        month=german.MONTH,
        pattern=SIMPLE_ALPHA_DATE_MONTH_FIRST,
    )

    pattern = [
        location_comma_day_month_year,
        simple_alpha_date,
        simple_alpha_date_month_first,
        simple_month_year_date,
        simple_date,
        semester_year,
    ]
    for index in range(7):
        pattern.append(functools.partial(simple_alpha_date, reduce=index))

    parsed = [parser(raw) for parser in pattern]
    parsed = [item for item in parsed if item]  # remove non matches
    # use longest matching pattern
    parsed = sorted(parsed, key=lambda x: len(x.raw), reverse=True)
    if not parsed:
        return None
    return parsed[0]


def validate_date(year, month, day):
    """\
    >>> validate_date(2010, 8, 25)
    True
    """
    try:
        calendar.weekday(year, month, day)
    except ValueError:
        return False
    return True


MONTH_GROUP = r'(?P<month>%s)' % german.MONTH_REGEX[1:-1]

SIMPLE_DATE = r'(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})'

SIMPLE_ALPHA_DATE = r'(?P<day>\d{1,2})([\.|,])[ ]%s[ ](?P<year>\d{4})' % MONTH_GROUP
SIMPLE_ALPHA_DATE_MONTH_FIRST = r'%s[ ](?P<day>\d{1,2})([\.|,])[ ](?P<year>\d{4})' % MONTH_GROUP

SIMPLE_MONTH_YEAR = r'%s[ ](?P<year>\d{4})' % MONTH_GROUP

LOCATION_COMMA_DAY_MONTH_YEAR = r'(?P<location>\w+),[ ](den[ ]){0,1}(%s)' % SIMPLE_ALPHA_DATE


def simple_date(raw):
    """\
    >>> simple_date(' 21.05.1999  random')
    TitleDate(year=1999, month=5, day=21, location=None, valid=True, raw='21.05.1999')
    """
    parsed = re_search(SIMPLE_DATE, raw)
    if not parsed:
        return None
    valid = len(parsed['day']) == len(parsed['month']) == 2
    year, month, day = int(parsed['year']), int(parsed['month']), int(parsed['day']) # yapf:disable
    result = iamraw.TitleDate(
        year=year,
        month=month,
        day=day,
        location=None,
        valid=valid,
        raw=utila.extract_match(parsed),
    )
    return result


def reduce_word(word, count):
    reduced = word[0:len(word) - count]  # TODO: improve this
    if len(reduced) <= 3:
        return word[0:3]
    return reduced


def simple_alpha_date(  # pylint:disable=R0914
        raw,
        reduce: int = 0,
        month=None,
        pattern=SIMPLE_ALPHA_DATE,
):
    """\
    >>> simple_alpha_date('Abgabedatum: 15. Jan 2010 ')
    TitleDate(year=2010, month=1, day=15, location=None, valid=True, raw='15. Jan 2010')
    """
    if not month:
        month = german.MONTH
    month_match = {reduce_word(item, reduce): item for item in month}
    changed_pattern = str(pattern)
    for key, value in month_match.items():
        changed_pattern = changed_pattern.replace(value, key)
    parsed = re_search(changed_pattern, raw)
    if not parsed:
        return None

    day = int(parsed['day'])
    monthcount = german.month(parsed['month'])
    year = int(parsed['year'])
    valid = len(parsed['day']) == 2
    result = iamraw.TitleDate(
        year=year,
        month=monthcount,
        day=day,
        location=None,
        valid=valid,
        raw=utila.extract_match(parsed),
    )
    return result


def simple_month_year_date(raw):
    """\
    >>> simple_month_year_date('Juli 2003 ')
    TitleDate(year=2003, month=7, day=None, location=None, valid=True, raw='Juli 2003')
    """
    parsed = re_search(SIMPLE_MONTH_YEAR, raw)
    if not parsed:
        return None
    month = german.month(parsed['month'])
    year = int(parsed['year'])
    result = iamraw.TitleDate(
        year=year,
        month=month,
        day=None,
        location=None,
        valid=True,
        raw=utila.extract_match(parsed),
    )
    return result


def location_comma_day_month_year(raw: str) -> iamraw.TitleDate:
    """\
    >>> location_comma_day_month_year('Berlin, 39. April 2016')
    TitleDate(year=2016, month=4, day=39, location='Berlin', valid=False, raw='Berlin, 39. April 2016')
    """
    parsed = re_search(LOCATION_COMMA_DAY_MONTH_YEAR, raw)
    if not parsed:
        return None
    location = parsed['location']
    day = int(parsed['day'])
    month = german.month(parsed['month'])
    year = int(parsed['year'])
    valid = validate_date(year, month, day)

    result = iamraw.TitleDate(
        year=year,
        month=month,
        day=day,
        location=location,
        valid=valid,
        raw=utila.extract_match(parsed),
    )
    return result


SEMESTER = r"""
    (SOMMERSEMESTER|WINTERSEMESTER|SS|WS)
    [ ]{1,4}
    (?P<year>\d{2,4})
"""


def semester_year(raw: str) -> iamraw.TitleDate:
    """Parses year from semester text.

    >>> semester_year('BACHELORARBEIT von Martina Feilke Sommersemester 2009 SOLAR II').year
    2009
    """
    searched = re_search(SEMESTER, raw)
    if not searched:
        return None
    year = int(searched['year'])
    result = iamraw.TitleDate(
        year=year,
        month=None,
        day=None,
        location=None,
        valid=True,
        raw=utila.extract_match(searched),
    )
    return result
