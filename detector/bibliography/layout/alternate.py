# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Alternate
=========

[Bra11] Braess, H.H.: Vieweg Handbuch Kraftfahrzeugtechnik. Vieweg+Teubner Verlag,
        2011 (ATZ/MTZ-Fachbuch)
[Dit13] Dittmann, D.: Alstom Hybridlokomotiven im Verschubeinsatz - Konzept und
        Erfahrungen im Einsatz H3 Fahrzeugplattform. 2013

[1] W. Abmayr. Einführung in die digitale Bildverarbeitung. B.G.
    Teubner Stuttgart, 1994.
[2] M. Baccar, L.A. Gee, R.C. Gonzalez, and M.A. Abidi. Segmentation of
    Range Images via Data Fusion and Morphological Watersheds. Pattern
    Recognition, 29(10):1673 – 1687, 1996.
"""

import geostrat
import iamraw
import texmex

import detector.bibliography.reference.freeand
import detector.bibliography.reference.magic
import detector.bibliography.reference.number
import detector.bibliography.reference.tech

MIN_CONTENT_LENGTH = 15  # TODO: HOLY VALUE
MIN_WORD_COUNT = 2  # TODO: HOLY VALUE
ERROR_MAX_LEVEL = 0.25


def extracts(items: texmex.PageTextNavigators) -> iamraw.BibliographyReferences:
    result = []
    config = geostrat.ParserConfig(
        min_content_length=MIN_CONTENT_LENGTH,
        min_word_count=MIN_WORD_COUNT,
    )
    try:
        parsed = geostrat.al_parse_pages(items, config=config)
    except geostrat.NoMultipleLiningPoints:
        return []
    for page in parsed:
        extracted = extract(page)
        if not extracted:
            continue
        error = len([item for item in extracted if not item])
        error_quote = error / len(extracted)
        if error_quote >= ERROR_MAX_LEVEL:
            continue
        result.append(extracted)
    return result


def extract(content) -> iamraw.BibliographyReferences:
    if content is None:
        # white page
        return []
    result = []
    for group in content:
        raw = texmex.connect_text(group)
        parsed = split_bibliography(raw)
        if not parsed:
            continue
        result.append(parsed)
    return result


def split_bibliography(raw: str) -> iamraw.BibliographyReference:  # pylint:disable=R0911
    raw = raw.strip()
    matched = detector.bibliography.reference.number.parse(raw)
    if matched:
        return matched
    matched = detector.bibliography.reference.freeand.parse_longtext_less_strict(raw)  # yapf:disable
    if matched:
        return matched
    matched = detector.bibliography.reference.tech.parse_single_row(raw)  # pylint:disable=R0204
    if matched:
        return matched
    matched = detector.bibliography.reference.tech.parse_longtext(raw)
    if matched:
        return matched
    matched = detector.bibliography.reference.magic.parse(raw)
    if matched:
        return matched
    matched = parse_last(raw)
    if matched:
        return matched
    return None


MAGIC_LENGTH = 120


def parse_last(raw: str) -> iamraw.BibliographyReference:
    # TODO: NOT VERY SMART
    if len(raw) < MAGIC_LENGTH:
        return None
    content = raw
    year = detector.bibliography.reference.years(raw)
    if year:
        raw = raw.replace(year[0], '')
        year = year[1]
    try:
        title, rest = raw.split('-')  # pylint:disable=W0612
    except ValueError:
        title, rest = 'NO TITLE', raw
    authors = iamraw.NoPerson(raw='o.A.')
    result = iamraw.BibliographyReference(
        authors=[authors],
        title=title,
        year=year,
        raw=content,
    )
    return result
