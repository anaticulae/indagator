# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

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
    """
    pattern = [
        r'\((?P<year>\d{4})\.(?P<month>\d{1,2})\.(?P<day>\d{1,2})\)',
        r'\((?P<day>\d{1,2})\.(?P<month>\d{1,2})\.(?P<year>\d{4})\)',
    ]
    for item in pattern:
        matched = re.search(item, raw)
        if not matched:
            continue
        raw = utila.extract_match(matched)
        date = (
            int(matched['year']),
            int(matched['month']),
            int(matched['day']),
        )
        return (raw, date)
    return None
