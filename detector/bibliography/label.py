# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibRefTechParser
================

Parses technical bibliographic reference like:

.. code-block:: none

    [WL11]
    [Rum05, Seite 10]

"""

import contextlib
import re

import iamraw
import utila

# [ ]{0,3} Optional whitespaces

TECHNICAL = r"""\[[ ]{0,3}
                (?P<author>[\w\.]{2,3}[+]{0,1})[ ]{0,3}
                (?P<year>\d{2})[ ]{0,3}
                (?P<number>a|b|c|d){0,1}[ ]{0,3}
                (\,[ ]{0,3}(Seite|S\.)[ ]{0,3}
                (
                 (?P<pagestart>\d{1,3})[ ]{0,3}\-[ ]{0,3}(?P<pageend>\d{1,3})|
                 (?P<page>\d{1,3}[ ]{0,3}[f]{0,2}\.?)
                )
                ){0,1}
                [ ]{0,3}\]
             """


def parses(content: str) -> iamraw.BibliographyReferences:
    result = []
    for item in re.finditer(TECHNICAL, content, re.VERBOSE):
        raw = utila.extract_match(item)
        page, pageend = None, None
        if item['page']:
            page, pageraw = parse_single(item['page'])  # pylint:disable=W0612
        with contextlib.suppress(KeyError, TypeError):
            page, pageend = int(item['pagestart']), int(item['pageend'])
        number = item['number'] if item['number'] else None

        techref = item['author'] + item['year'] + (number if number else '')
        year = int(item['year'])
        year = millennium(year)

        reference = iamraw.BibliographyReference(
            page=page,
            pageend=pageend,
            reference=techref,
            year=year,
            number=number,
            raw=raw,
        )
        result.append(reference)
    return result


def parse_single(page: str):
    number = parse_ints(page)[0]
    follow = page.replace(str(number), '').strip()
    return number, follow


def parse_ints(item: str) -> int:
    # TODO: REPLACE WITH UTILA CODE
    return [int(item) for item in re.findall(r'\d+', item)]


def millennium(year: int) -> int:
    """\
    >>> millennium(99)
    1999
    >>> millennium(0)
    2000
    >>> millennium(29)
    2029
    """
    # HINT: Works till 2030 :)
    if year < 30:
        # 2000 - 2029
        year += 2000
    else:
        # 1900 - 1999
        year += 1900
    return year
