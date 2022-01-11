# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import german
import iamraw
import utila

import detector.bibliography.label
import detector.bibliography.reference
import detector.bibliography.reference.freeand
import detector.quotes


@functools.lru_cache(maxsize=4096)
def parse_single_row(content: str) -> iamraw.BibliographyReference:
    matched = detector.bibliography.label.parses(content)
    if not matched:
        matched = detector.bibliography.label.numbers(content)
    if not matched:
        return None
    if len(matched) > 1:
        # Mostly a result of failure in layout grouping. This can
        # happen if a wrong layout grouping mechanism is used. This is not
        # a problem cause we have more than one strategy.
        # utila.debug('parses more than one reference, '
        #             f'skip tech result: {content}')
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


@functools.lru_cache(maxsize=4096)
def parse_longtext(content: str) -> iamraw.BibliographyReference:
    """\
    >>> parse_longtext('Todd D. Jick. “Mixing Qualitative and Quantitative Methods: Triangulation in Action.” In: AdministrativeScienceQuarterly 24 (1979), pp. 602– 611.')
    BibliographyReference(title='“Mixing...authors=[Person(name='Todd', firstname='D. Jick.'...raw_pdfpage=None)
    """
    content = utila.normalize_text(content)
    raw = content
    parsed = parse_first(content)
    if not parsed:
        return None
    authors, rest = parsed
    try:
        title, rest = parse_title(rest)
    except TypeError:
        return None
    title = title.strip()
    authors = authors.strip()
    authors = german.authors(authors)
    # disable non person authors
    authors = german.authors_decide(authors)
    page = german.pages(rest)
    if page:
        rest = rest.replace(page[0], '')
    year = detector.bibliography.reference.years(rest)
    access, rest = detector.bibliography.reference.freeand.parse_accessed(rest)
    if year:
        # remove year from right to left
        rest = ' '.join(rest.rsplit(year[0], maxsplit=1))
        # remove fragment from year splitter, TODO: remove later!
        rest = rest.replace('( )', '').strip()
    # TODO: ADD PUBLISHER EXTRACTOR
    rest = rest.strip()
    hyperlinks, rest = detector.bibliography.reference.freeand.parse_hyperlinks(
        rest)
    publisher = parse_publisher(rest)
    result = iamraw.BibliographyReference(
        authors=authors,
        title=title,
        raw=raw,
        publisher=publisher,
        hyperlink=hyperlinks,
        accessed=access,
    )
    if page:
        result.page = page[1][0]
        if len(page[1]) == 2:
            result.pageend = page[1][1]
    if year:
        result.year = year[1]
    return result


@functools.lru_cache(maxsize=4096)
def parse_first(content: str):
    """\
    >>> parse_first('Put People First. http://www.putpeoplefirst.org.uk/ (19.1.2015).')
    ('Put People First. ', 'http://www.putpeoplefirst.org.uk/ (19.1.2015).')
    """
    authors = detector.quotes.before_first_quote(content, starting=5)
    if authors:
        if len(authors) <= content.find(':'):
            # quote starts before first collon
            rest = content.replace(authors, '')
            return authors, rest
    try:
        authors, rest = content.split(':', maxsplit=1)
    except ValueError:
        return None
    for token in 'https http'.split():
        if authors.endswith(token):
            rest = f'{token}:{rest}'
            authors = authors[:-len(token)]
    return authors, rest


@functools.lru_cache(maxsize=4096)
def parse_title(rest: str) -> tuple:
    rest = rest.strip()
    if '.' in rest:
        return rest.split('.', maxsplit=1)
    if ';' in rest:
        return rest.split(';', maxsplit=1)
    if ',' in rest:
        return rest.split(',', maxsplit=1)
    return None


@functools.lru_cache(maxsize=4096)
def parse_publisher(rest: str):
    if not rest:
        return None
    rest = rest.strip()
    if len(rest) < 10:
        # Not a valid publisher
        return None
    return rest
