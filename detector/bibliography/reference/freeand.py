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

# TODO: ADD OPTIONAL BRACKETS TO REMOVE DIRTY SIMPLE YEAR HACK
# TODO: REMOVE 4,5 HACK: WHEN SUPPORTING HIGHNOTE
AND = r"""
    (?P<authors>[A-Z,;\(\)\.\-\&ÖÄÜ\d ]{5,})
    (
        \((?P<oj>o\.j\.)\)|
        %s # brackets open
        ((?P<year>\d{4,5})([ ]{0,3}\-(?P<yearend>\d{4})[ ]{0,3}){0,1})
        (?P<number>a|b|c|d){0,1}  # optional char
        %s # brackets close
        |
        (?P<simpleyear>\d{4})[ ]{0,2}[a-z]{0,1}[ ]{0,2}:          # see wessels 2007, TODO: DIRTY
    )
    [ ]{0,5}                      # remove trailing whitespaces
    [:\.]{0,1}                    # remove dot or colon
    [ ]{0,5}                      # remove trailing whitespaces
    (?P<content>.+)
"""

NORMAL = AND % (r'\(', r'\)')

BROKEN_BRACKETS = AND % (r'[\(\[]', r'[\]\)]')
"""\
>>> parse_longtext('Deutsche Norm DIN 1421 (1983]: Abschnitte. Berlin: Beuth', pattern=BROKEN_BRACKETS).authors
[NoPerson(confidence=None, raw='Deutsche Norm DIN 1421')]
"""


def parse_longtext(  # pylint:disable=R1260,R0912
        content: str,
        pattern=NORMAL,
) -> iamraw.BibliographyReference:
    # convert multiple lines into a single text block. Convert inner
    # newlines into space and trim spaces at front and end
    content = content.replace('\n', ' ').strip()  # TODO: USE EXTERNAL METHOD
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
    try:
        title, rest = content.split('. ', maxsplit=1)
    except ValueError:
        title_link = title_with_link(content)
        if title_link:
            title, rest = title_link
        else:
            title, rest = None, content
    if invalid_title(title):
        return None
    return title, rest


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
