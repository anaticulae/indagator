# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw
import pattern

import detector.bibliography.machine.author
import detector.bibliography.machine.title

IN = pattern.Regex(regex=r'IN:[^\*]+', name='in-pattern')

PATTERN = (
    german.issn,
    german.isbn,
    german.doi,
    german.accessed,
    german.pagenumbers,
    german.hyperlink,
    german.dates_master,
    'URL:',
    pattern.SimpleCleanup,
    IN,
    german.years,
    pattern.SimpleCleanup,
    detector.bibliography.machine.title.Titles,
    detector.bibliography.machine.author.SmartAuthor,
    detector.bibliography.machine.title.TitlesBetween,
)

IMPROVES = (german.href_magic,)


def reference(raw: str) -> iamraw.BibliographyReference:
    matched = pattern.match(
        raw,
        patterns=PATTERN,
        improves=IMPROVES,
    )
    if not matched:
        return None
    data = matched['data']
    result = iamraw.BibliographyReference(raw=raw)
    result.authors = data.get('authors', None)
    result.title = data.get('title', None)
    result.hyperlink = data.get('hyperlink', None)
    return result
