# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import utila

import detector.bibliography.label
import detector.bibliography.reference


def parse_single_row(content: str) -> iamraw.BibliographyReference:
    matched = detector.bibliography.label.parses(content)
    if not matched:
        matched = detector.bibliography.label.numbers(content)
    if not matched:
        return None
    if len(matched) > 1:
        # Mostly a result of failure in layout grouping. This can
        # happen if a wrong layout grouping mechanism is used. This
        # issn't a problem cause we have more than one strategy.
        utila.error(f'parses more than one reference: {content}')
        return None
    matched: iamraw.BibliographyReference = matched[0]
    content = content.replace(matched.raw, '')
    detected = detector.bibliography.reference.tech.parse_longtext(content)
    if not detected:
        # no further information detected
        return matched
    # append information of second parsing step
    matched.title = detected.title
    matched.authors = detected.authors
    matched.publisher = detected.publisher
    matched.raw += detected.raw
    return matched


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
    authors = german.authors(authors)
    # disable non person authors
    authors = german.authors_decide(authors)

    page = detector.bibliography.reference.pages(rest)
    if page:
        rest = rest.replace(page[0], '')
    year = detector.bibliography.reference.years(rest)
    if year:
        # remove year from right to left
        rest = ' '.join(rest.rsplit(year[0], maxsplit=1))

    # TODO: ADD PUBLISHER EXTRACTOR

    rest = rest.strip()
    result = iamraw.BibliographyReference(
        authors=authors,
        title=title,
        raw=raw,
        publisher=rest or None,
    )
    if page:
        result.page = page[1][0]
        if len(page[1]) == 2:
            result.pageend = page[1][1]
    if year:
        result.year = year[1]
    return result
