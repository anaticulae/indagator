# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
[1] W. Abmayr. Einführung in die digitale Bildverarbeitung. B.G. Teubner
Stuttgart, 1994.

[2] M. Baccar, L.A. Gee, R.C. Gonzalez, and
M.A. Abidi. Segmentation of Range Images via Data Fusion and
Morphological Watersheds. Pattern Recognition, 29(10):1673 – 1687, 1996.

[3] W. Bailer, F. Höller, A. Messina, D. Airola, P. Schallauer, and M.
Hausenblas. State of the Art of Content Analysis Tools for Video, Audio
and Speech. Technical report, Presto Space, 3 2005.
"""

import re

import german
import iamraw
import utila


def parse(raw: str) -> iamraw.BibliographyReference:
    splitted = split(raw)
    if not splitted:
        return None
    number, text = splitted
    parsed = content(text)
    if not parsed:
        utila.debug(f'could not parse reference:number `{text}`')
        return None
    parsed.reference = f'[{number}]'
    return parsed


SPLITTER = re.compile(
    r"""
    ^
    \[
        (\d{1,4})
    \]
    [ ]{0,4}
    """,
    re.X | re.DOTALL,
)


def split(raw: str) -> tuple:
    """\
    >>> split('[1] W. Abmayr. Einführung in die digitale')
    (1, 'W. Abmayr. Einführung in die digitale')
    """
    splitted = SPLITTER.split(raw)
    if not splitted or len(splitted) <= 1:
        # TODO: IS `not splitted` not REQUIRED?
        return None
    number = int(splitted[1])
    data = splitted[2]
    return number, data


PATTERN = re.compile(
    r"""^
    (?P<authors>
        (
            (\w\.[ ]{0,3}){1,2}        # short first name
            \w{2,}                     # last name
            (\,|\.){0,1}               # optional separator between authors
            ([ ]{0,3}and[ ]{0,3}){0,1} # optional and before last author
            [ ]{0,3}
        ){1,}                          # more than one author
    )
    [ ]{0,3}
    (?P<middle>.+?)
    \,{0,1}
    [ ]{0,3}
    (?P<year>\d{4})
    [ ]{0,3}
    \.{0,1}
    """,
    re.X | re.DOTALL,
)


def content(
    raw: str,
    title_length_min: int = 10,
) -> iamraw.BibliographyReference:
    """\
    >>> content('W. Abmayr. Einführung in die digitale Bildverarbeitung. B.G. Teubner Stuttgart, 1994.')
    BibliographyReference(title='Einf...year=1994...name='Abmayr.'...)
    >>> content('M. Baccar, L.A. Gee, R.C. Gonzalez, and M.A. Abidi. Segmentation of Range Images via, 1996.')
    BibliographyReference(title='Segmentat...year=1996...)
    >>> content('D. Forsyth and J. Ponce. Computer Vision. A Modern Approch. Prentice Hall PTR, 2002.')
    BibliographyReference(title='Computer Vision'...year=2002,...)
    """
    parsed = PATTERN.search(raw)
    if not parsed:
        return None
    authors = parsed['authors']
    authors = authors.replace('and', ' ')
    authors = german.authors(authors)
    authors = german.authors_decide(authors)
    year = int(parsed['year'])
    result = iamraw.BibliographyReference(
        authors=authors,
        year=year,
        raw=utila.extract_match(parsed),
    )
    middle = parsed['middle']
    if middle:
        try:
            title, middle = middle.split('.', maxsplit=1)
        except ValueError:
            # no dot in middle
            title, middle = middle, ''
        if len(title) > title_length_min:
            result.title = title
        result.data = middle.strip()
    return result
