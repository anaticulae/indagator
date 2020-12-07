# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

import detector.bibliography.reference as dbr
import detector.bibliography.reference.authors as dbra


def parse_longtext(content: str) -> iamraw.BibliographyReference:
    content = content.replace('\n', ' ')
    raw = content
    try:
        authors, rest = content.split(':', maxsplit=1)
    except ValueError:
        return None
    try:
        title, rest = rest.split('.', maxsplit=1)
    except ValueError:
        return None
    # press = rest.split('.)

    title = title.strip()
    authors = authors.strip()
    authors = dbra.simple(authors)

    page = dbr.pages(rest)
    if page:
        rest = rest.replace(page[0], '')
    year = dbr.years(rest)
    if year:
        # remove year from right to left
        rest = ' '.join(rest.rsplit(year[0], maxsplit=1))

    # TODO: ADD PUBLISHER EXTRACTOR

    result = iamraw.BibliographyReference(
        authors=authors,
        title=title,
        raw=raw,
        publisher=rest,
    )
    if page:
        result.page = page[1][0]
        if len(page[1]) == 2:
            result.pageend = page[1][1]
    if year:
        result.year = year[1]
    return result
