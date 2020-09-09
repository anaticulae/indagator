# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import geostrat
import iamraw
import texmex

import detector.bibliography.reference.freeand
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
        raw = geostrat.connect_text(group)
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
    return None
    # default = iamraw.BibliographyReference(raw=raw)
    # return default
