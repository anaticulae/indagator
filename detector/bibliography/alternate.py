# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hey.geometry.alternate
import hey.text.utils
import iamraw
import texmex

import detector.bibliography.reference.freeand
import detector.bibliography.reference.tech

MIN_CONTENT_LENGTH = 15  # TODO: HOLY VALUE

MIN_WORD_COUNT = 2  # TODO: HOLY VALUE


def extracts(items: texmex.PageTextNavigators) -> iamraw.BibliographyReferences:
    result = []
    config = hey.geometry.alternate.ParserConfig(
        min_content_length=MIN_CONTENT_LENGTH,
        min_word_count=MIN_WORD_COUNT,
    )
    try:
        parsed = hey.geometry.alternate.parse_pages(items, config=config)
    except hey.geometry.alternate.NoMultipleLiningPoints:
        return []
    for page in parsed:
        extracted = extract(page)
        result.append(extracted)
    return result


def extract(content) -> iamraw.BibliographyReferences:
    if content is None:
        # white page
        return []
    result = []
    for group in content:
        raw = hey.text.utils.connect_text(group)
        parsed = split_bibliography(raw)
        result.append(parsed)
    return result


def split_bibliography(raw: str) -> iamraw.BibliographyReference:
    raw = raw.strip()
    matched = detector.bibliography.reference.freeand.parse_longtext(raw)
    if matched:
        return matched
    matched = detector.bibliography.reference.tech.parses(raw)  # pylint:disable=R0204
    if matched:
        return matched[0]
    default = iamraw.BibliographyReference(raw=raw)
    return default
