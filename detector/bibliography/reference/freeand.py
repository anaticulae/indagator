# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""BibRef AND(&) Parser
====================

.. code-block:: none

    Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B. (2000b). A
    review of the literature on the Effects of Low Doses of Alcohol on
    driving-Related Skills. National Highway Traffic Safety
    Administration (NHTS), Southern California Research Institute,
    Washington.

Authors
-------

Correct
~~~~~~~

* Schmidt, R., Dettmeyer, R., Padosch, S. & Madea, B.

Failures
~~~~~~~~

* Schnabel, Eva
* Sdao-Jarvie, K. and Vogel-Sprott, M.

"""

import re

import german
import iamraw
import utila

MONTHRAW = '|'.join("""
JANUAR FEBRUAR MÄRZ APRIL MAI JUNI JULI AUGUST \
SEPTEMBER OKTOBER NOVEMBER DEZEMBER \
JANUARY FEBRUARY MARCH APRIL MAY JUNE JULY AUGUST \
SEPTEMBER OCTOBER NOVEMBER DECEMBER
""".strip().split())

MONTH = r"""
    (
        [ ]{0,3}
        (%s)
        [ ]{0,3}
        \d{0,2}
        [ ]{0,3}
        \,{0,1}
        [ ]{0,3}
    ){0,1}
""" % MONTHRAW

# TODO: ADD OPTIONAL BRACKETS TO REMOVE DIRTY SIMPLE YEAR HACK
# TODO: REMOVE 4,5 HACK: WHEN SUPPORTING HIGHNOTE
AND = r"""
    (?P<authors>
        [A-Z,;\(\)\.\-\&ÖÄÜ\d ]{5,}
        [^\(\)\[\]]                           # author does not ends with bracket
    )
    (
        \(?(?P<oj>o\.j\.)\)?
        |
        %s # brackets open
        %s # optional month
        ((?P<year>\d{4,5})([ ]{0,3}\-(?P<yearend>\d{4})[ ]{0,3}){0,1})
        (?P<number>a|b|c|d){0,1}  # optional char
        %s # brackets close
        |
        \({0,1}
        (?P<simpleyear>\d{4})[ ]{0,2}[a-z]{0,1}[ ]{0,2}:    # see wessels 2007, TODO: DIRTY
        \){0,1}
    )
    [ ]{0,5}                      # remove trailing whitespaces
    [:\.]{0,1}                    # remove dot or colon
    [ ]{0,5}                      # remove trailing whitespaces
    (?P<content>.+)
"""

NORMAL = AND % (r'\(', MONTH, r'\)')

BROKEN_BRACKETS = AND % (r'[\(\[]', MONTH, r'[\]\)]')
"""\
>>> parse_longtext('Deutsche Norm DIN 1421 (1983]: Abschnitte. Berlin: Beuth', pattern=BROKEN_BRACKETS).authors
[NoPerson(confidence=None, raw='Deutsche Norm DIN 1421')]
"""


def parse_longtext(  # pylint:disable=R1260,R0912
        content: str,
        pattern=NORMAL,
) -> iamraw.BibliographyReference:
    content = utila.normalize_text(content)
    raw = content
    matched = re.search(pattern, content, re.VERBOSE | re.IGNORECASE)
    if not matched:
        return None
    authors = german.authors(matched['authors'])
    # disable non person authors
    authors = german.authors_decide(authors)
    if matched['year']:
        year = int(matched['year'])
    elif matched['simpleyear']:
        year = int(matched['simpleyear'])
    else:
        # without year
        year = 'no year'
    number = matched['number'] if matched['number'] else None

    hyperlinks = german.hyperlink(content)
    if hyperlinks:
        for hyperlink in hyperlinks:
            content = content.replace(hyperlink, '')
    if len(hyperlinks) > 1:
        utila.debug(f'more than one link parsed: {raw}')

    accessed = german.accessed(content)
    if accessed:
        content = content.replace(accessed[0], '')

    parsed_title = parse_title(content=matched['content'])
    if not parsed_title:
        return None
    title, rest = parsed_title

    page = german.pages(rest)
    if not page:
        page = german.pages_complex(rest)
    if page:
        rest = rest.replace(page[0], '')

    result = iamraw.BibliographyReference(
        authors=authors,
        number=number,
        title=title,
        year=year,
        raw=raw,
    )
    result.hyperlink = hyperlinks[0] if hyperlinks else None
    result.accessed = accessed[1] if accessed else None

    # TODO: ADD YEAREND after upgrading
    if page:
        result.page = page[1][0]
        if len(page[1]) == 2:
            result.pageend = page[1][1]
    return result


def parse_title(content: str) -> tuple:
    """Increase number of valid dots to parse long title with a lot of dots.

    >>> parse_title('Hrsg. von der Dudenredaktion. 23. neu bearb. Aufl..') # TODO: CHANGE LATER
    ('Hrsg. von der Dudenredaktion', '23. neu bearb. Aufl..')
    >>> parse_title('Das System der zentralen Orte Österreichs: Eine empirische Untersuchung - Graz')
    ['Das System der zentralen Orte Österreichs: Eine empirische Untersuchung', 'Graz']
    """
    # 1.  Try normal title splitter
    # 1b. Try splitting till link starts
    # 2.  Extend number of valid dots
    try:
        title, rest = content.split('. ', maxsplit=1)
        if invalid_title(title) is False:  # None means no title given
            return title, rest
    except ValueError:
        title_link = title_with_link(content)
        if title_link:
            title, rest = title_link
            return title, rest
    if not '.' in content:
        # TODO: ADD OTHER ALGO
        if ' - ' in content:
            return content.split(' - ', maxsplit=1)
        return content, ''

    for maxdots in range(1, 5):
        splitted = content.split('. ', maxsplit=maxdots)
        title, rest = '. '.join(splitted[:-1]), splitted[-1]
        if invalid_title(title) is False:  # None means no title given
            return title, rest
    return None


def parse_longtext_less_strict(content: str) -> iamraw.BibliographyReference:
    for pattern in [NORMAL, BROKEN_BRACKETS]:
        parsed = parse_longtext(content, pattern=pattern)
        if not parsed:
            continue
        return parsed
    return None


TITLE_MIN_LENGTH = 10


def title_with_link(text: str) -> str:
    """\
    >>> title_with_link('Zentrale Orte Raumordnungsprogramm (NÖ) https://www.ris.bka.gv.at/LRNI_1992062.pdf (25.01.2018)')
    ('Zentrale Orte Raumordnungsprogramm (NÖ)', 'https://www.ris.bka.gv.at/LRNI_1992062.pdf (25.01.2018)')
    """
    hypers = german.hyperlink(text)
    if not hypers:
        return None
    started = text.find(hypers[0])
    title = text[0:started].strip()
    rest = text[started:].strip()
    return title, rest


def invalid_title(title: str, title_min_length: int = TITLE_MIN_LENGTH) -> bool:
    if not title:
        return None
    if len(title) < title_min_length:
        return True
    rate = char_rate(title)
    if rate < 0.8:
        return True
    return False


ALPHA = 'abcdefghijklmnopqrstuvwxyz '


def char_rate(text: str):
    # TODO: MOVE
    if not text:
        return 0
    text = text.lower()
    selected = len([item for item in text if item in ALPHA])
    return selected / len(text)
