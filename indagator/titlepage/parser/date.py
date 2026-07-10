# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
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

import germania
import iamraw
import utilo


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
        month=germania.MONTH,
        pattern=ALPHA_DATE_MONTH_FIRST,
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


def validate_date(year: int, month: int, day: int) -> bool:
    """\
    >>> validate_date(2010, 8, 25)
    True
    """
    try:
        calendar.weekday(year, month, day)
    except ValueError:
        return False
    return True


MONTH_GROUP = r'(?P<month>%s)' % germania.MONTH_REGEX[1:-1]  # pylint:disable=C0209

SIMPLE_DATE = utilo.compiles(r"""
    (?P<day>\d{1,2})\.
    (?P<month>\d{1,2})\.
    (?P<year>(20[012]\d|1[789]\d\d))
""")

ALPHA_DATE = r'(?P<day>\d{1,2})([\.|,])[ ]' + MONTH_GROUP + r'[ ](?P<year>(20[012]\d|1[789]\d\d))'
ALPHA_DATE_MONTH_FIRST = MONTH_GROUP + r'[ ](?P<day>\d{1,2})([\.|,])[ ](?P<year>(20[012]\d|1[789]\d\d))'

MONTH_YEAR = utilo.compiles(MONTH_GROUP + r'[ ](?P<year>(20[012]\d|1[789]\d\d))') # yapf:disable

LOCATION_COMMA_ALPHADATE = utilo.compiles(
    r'(?P<location>\w{3,75}),[ ](den[ ]){0,1}(%s)' % ALPHA_DATE)  # pylint:disable=C0209


def simple_date(raw):
    """\
    >>> simple_date(' 21.05.1999  random')
    TitleDate(year=1999, month=5, day=21, location=None, valid=True, raw='21.05.1999')
    """
    parsed = SIMPLE_DATE.search(raw)
    if not parsed:
        return None
    result = iamraw.TitleDate(
        valid=len(parsed['day']) == len(parsed['month']) == 2,
        **extract_data(
            parsed,
            values=dict(
                day=int,
                month=int,
                year=int,
            ),
        ),
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
    pattern=ALPHA_DATE,
):
    """\
    >>> simple_alpha_date('Abgabedatum: 15. Jan 2010 ')
    TitleDate(year=2010, month=1, day=15, location=None, valid=True, raw='15. Jan 2010')
    """
    if not month:
        month = germania.MONTH
    month_match = {reduce_word(item, reduce): item for item in month}
    changed_pattern = str(pattern)
    for key, value in month_match.items():
        changed_pattern = changed_pattern.replace(value, key)
    parsed = utilo.search(changed_pattern, raw)
    if not parsed:
        return None
    result = iamraw.TitleDate(
        valid=len(parsed['day']) == 2,
        **extract_data(
            parsed,
            values=dict(
                day=int,
                month=germania.month,
                year=int,
            ),
        ),
    )
    return result


def simple_month_year_date(raw):
    """\
    >>> simple_month_year_date('Juli 2003 ')
    TitleDate(year=2003, month=7, day=None, location=None, valid=True, raw='Juli 2003')
    """
    parsed = MONTH_YEAR.search(raw)
    if not parsed:
        return None
    result = iamraw.TitleDate(
        valid=True,
        **extract_data(
            parsed,
            values=dict(
                month=germania.month,
                year=int,
            ),
        ),
    )
    return result


def location_comma_day_month_year(raw: str) -> iamraw.TitleDate:
    """\
    >>> location_comma_day_month_year('Berlin, 39. April 2016')
    TitleDate(year=2016, month=4, day=39, location='Berlin', valid=False, raw='Berlin, 39. April 2016')
    """
    parsed = LOCATION_COMMA_ALPHADATE.search(raw)
    if not parsed:
        return None
    result = iamraw.TitleDate(**extract_data(
        parsed,
        values=dict(
            location=str,
            day=int,
            month=germania.month,
            year=int,
        ),
    ))
    result.valid = validate_date(result.year, result.month, result.day)
    return result


SEMESTER = utilo.compiles(r"""
    (SOMMERSEMESTER|WINTERSEMESTER|SS|WS)
    [ ]{1,4}
    (?P<year>\d{2,4})
""")


def semester_year(raw: str) -> iamraw.TitleDate:
    """Parses year from semester text.

    >>> semester_year('BACHELORARBEIT von Martina Feilke Sommersemester 2009 SOLAR II').year
    2009
    """
    parsed = SEMESTER.search(raw)
    if not parsed:
        return None
    result = iamraw.TitleDate(
        valid=True,
        **extract_data(
            parsed,
            values=dict(year=int,),
        ),
    )
    return result


def extract_data(data, values: list) -> dict:
    # TODO: MOVE TO utilo
    result = {
        'raw': utilo.extract_match(data),
    }
    for key, converter in values.items():
        result[key] = converter(data[key])
    return result
