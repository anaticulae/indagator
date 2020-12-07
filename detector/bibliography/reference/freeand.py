# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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

import iamraw
import utila

import detector.bibliography.reference as dbr
import detector.bibliography.reference.authors as dbra

# TODO: REMOVE 4,5 HACK: WHEN SUPPORTING HIGHNOTE
AND = r"""
    (?P<authors>[A-Za-z,;\(\)\.\-\&ÖöÄäÜü ]{5,})
    \(
        (
            (?P<oj>o\.j\.)|
            ((?P<year>\d{4,5})([ ]{0,3}\-(?P<yearend>\d{4})[ ]{0,3}){0,1})
            (?P<number>a|b|c|d){0,1}  # optional char
        )
    \)
    [ ]{0,5}                      # remove trailing whitespaces
    [:\.]{0,1}                    # remove dot or colon
    [ ]{0,5}                      # remove trailing whitespaces
    (?P<content>.+)
"""


def parse_longtext(content: str) -> iamraw.BibliographyReference:  # pylint:disable=R1260,R0912
    content = content.replace('\n', ' ').strip()
    raw = content
    matched = re.search(AND, content, re.VERBOSE | re.IGNORECASE)
    if not matched:
        return None

    authors = dbra.parses(matched['authors'])
    if matched['year']:
        year = int(matched['year'])
    else:
        # without year
        year = 'no year'
    number = matched['number'] if matched['number'] else None

    hyperlink = dbr.link(content)
    if hyperlink:
        content = content.replace(hyperlink[0], '')
    if len(hyperlink) > 1:
        utila.error(f'more than one link parsed: {content}')

    accessed = dbr.accessed(content)
    if accessed:
        content = content.replace(accessed[0], '')

    try:
        title, rest = matched['content'].split('. ', maxsplit=1)  # pylint:disable=W0612
    except ValueError:
        title_link = title_with_link(matched['content'])
        if title_link:
            title, rest = title_link
        else:
            title, rest = None, matched['content']
    if invalid_title(title):
        return None

    page = dbr.pages(rest)
    if not page:
        page = dbr.pages_complex(rest)
    if page:
        rest = rest.replace(page[0], '')

    result = iamraw.BibliographyReference(
        authors=authors,
        number=number,
        title=title,
        year=year,
        raw=raw,
    )
    result.hyperlink = hyperlink[0] if hyperlink else None
    result.accessed = accessed[1] if accessed else None

    # TODO: ADD YEAREND after upgrading
    if page:
        result.page = page[1][0]
        if len(page[1]) == 2:
            result.pageend = page[1][1]

    return result


TITLE_MIN_LENGTH = 10


def title_with_link(text: str) -> str:
    """\
    >>> title_with_link('Zentrale Orte Raumordnungsprogramm (NÖ) https://www.ris.bka.gv.at/LRNI_1992062.pdf (25.01.2018)')
    ('Zentrale Orte Raumordnungsprogramm (NÖ)', 'https://www.ris.bka.gv.at/LRNI_1992062.pdf (25.01.2018)')
    """
    hypers = dbr.link(text)
    if not hypers:
        return None
    started = text.find(hypers[0])
    title = text[0:started].strip()
    rest = text[started:].strip()
    return title, rest


def invalid_title(title: str) -> bool:
    if not title:
        return False
    if len(title) < TITLE_MIN_LENGTH:
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
