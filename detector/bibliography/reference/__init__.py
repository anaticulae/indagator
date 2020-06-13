# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Reference
=========

accessed
--------

>>> accessed('[Online; Zugriff Oktober 20, 2015]')
('[Online; Zugriff Oktober 20, 2015]', (2015, 10, 20))
>>> accessed('Version:August 2012')
('Version:August 2012', (2012, 8, 0))
>>> accessed('Zugriff am 19.06.2014')
('Zugriff am 19.06.2014', (2014, 6, 19))
"""

import contextlib
import re

import utila


def pages(raw: str):
    """\
    >>> pages('IEEE Joint, 2004, S. 113-117')
    ('S. 113-117', (113, 117))
    >>> pages('p.103')
    ('p.103', (103,))
    >>> pages('text before, S. 263–268')
    ('S. 263–268', (263, 268))
    """
    pattern = r"""(
         (Seite|S\.|p\.|P\.|page)[ ]{0,3}
         (
          (?P<pagestart>\d{1,4})[ ]{0,3}(\-|–)[ ]{0,3}(?P<pageend>\d{1,4})|
          (?P<page>\d{1,4})
         )
    )
    """
    matched = re.search(pattern, raw, re.VERBOSE)
    if not matched:
        return None
    raw = utila.extract_match(matched)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['page']),)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['pagestart']), int(matched['pageend']))
    return None


def pages_complex(raw: str):
    """\
    >>> pages_complex('Germaniques 53, H. 2, 93-122.')
    (', 93-122.', (93, 122))
    >>> pages_complex('Blutalkohol, 41, 1-10.')
    (', 1-10.', (1, 10))
    >>> pages_complex(',41, 1-10')
    (', 1-10', (1, 10))
    """
    pattern = r"""(
         (\,){0,1}[ ]{0,3}
         (
          (?P<pagestart>\d{1,4})[ ]{0,3}(\-|–)[ ]{0,3}(?P<pageend>\d{1,4})(\.|$)
         )
    )
    """
    matched = re.search(pattern, raw, re.VERBOSE)
    if not matched:
        return None
    raw = utila.extract_match(matched)
    with contextlib.suppress(TypeError):
        return raw, (int(matched['pagestart']), int(matched['pageend']))
    return None


def years(raw: str):
    """\
    >>> years('IEEE Joint, 2004, S. 113–117')
    ('2004', 2004)
    """
    pattern = r'(?P<year>\d{4})'
    matched = re.search(pattern, raw, re.VERBOSE)
    if not matched:
        return None
    raw = utila.extract_match(matched)
    return (raw, int(raw))


def link(raw: str):
    r"""\
    >>> link('Before: http://student.unifr.ch/\nReferenzrahmen2001.pdf after.')[0]
    'http://student.unifr.ch/Referenzrahmen2001.pdf'
    >>> link('This is a link:https://www.youtube.com/watch?v=RXbcAYxuZxw')[0]
    'https://www.youtube.com/watch?v=RXbcAYxuZxw'
    >>> link('Text.http://google.de')[0]
    'http://google.de'
    """
    raw = raw.replace('\n', '')
    pattern = r"""
    (http|https|www)[:]//[\w\d\./\-\?\=]+
    """
    result = []
    for item in re.finditer(pattern, raw, flags=re.VERBOSE):
        matched = utila.extract_match(item)
        result.append(matched)
    return result


def accessed(raw: str):
    """\
    >>> accessed('europaeischegemeinschaften?p=all (27.05.2018).')
    ('(27.05.2018)', (2018, 5, 27))
    >>> accessed('[Letzter Zugriff: 16.02.15]')
    ('[Letzter Zugriff: 16.02.15]', (15, 2, 16))
    """
    pattern = [
        r'\[Letzter[ ]{0,3}Zugriff\:[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})\]',
        r'Letzter[ ]{0,3}Zugriff\:[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})',
        r'\((?P<year>\d{2,4})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})\)',
        r'\((?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})\)',
        r'\[Online[ ]{0,3}Zugriff\:[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})\]',
        r'\[Online\;[ ]{0,3}Zugriff[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<day>\d{1,2})\,[ ]{0,3}(?P<year>\d{2,4})\]',
        r'Version\:[ ]{0,3}(?P<month>\w+)[ ]{0,3}(?P<year>\d{2,4})',
        r'Zugriff[ ]{0,3}am[ ]{0,3}(?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{2,4})',
    ]
    for item in pattern:
        matched = re.search(item, raw, re.IGNORECASE | re.VERBOSE)
        if not matched:
            continue
        raw = utila.extract_match(matched)
        date = (
            int(matched['year']),
            month(matched['month']),
            day(matched),
        )
        return (raw, date)
    return None


MONTH = [
    'januar', 'februar', 'märz', 'april', 'mai', 'juni', 'juli', 'august',
    'september', 'oktober', 'november', 'dezember'
]


def day(matched):
    with contextlib.suppress(IndexError):
        return int(matched['day'])
    return 0


def month(item: str):
    item = item.lower()
    for index, month_ in enumerate(MONTH, start=1):
        if item == month_:
            return index
    return int(item)
