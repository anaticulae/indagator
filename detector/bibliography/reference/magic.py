# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
Agricola, Erhard (Hrg.), Wörter und Wendungen. Wörterbuch zum deutschen.
        Sprachgebrauch, München: Max Hueber Verlag 1970.

Bergsträsser, Gotthelf, Einführung in die semitischen Sprachen, München:
        Max Hueber Verlag 1963.
"""

import functools
import re

import german
import iamraw


@functools.lru_cache(maxsize=4096)
def parse(raw: str) -> iamraw.BibliographyReference:
    raw = raw.strip()
    rest = raw
    splitted = raw.split(',')
    splitted = [item.strip() for item in splitted]
    collected = []
    for token in splitted:
        if token.count(' ') <= 1:
            collected.append(token)
            continue
        if '/' in token:
            collected.append(token)
            continue
        break
    collected: str = ', '.join(collected)

    authors = german.authors(collected)
    if authors == [['']]:
        # HACK: remove empty authors
        return None
    authors = german.authors_decide(authors)

    year_raw = re.search(r'(\d{4})\.$', raw)
    year = int(year_raw[1]) if year_raw else None

    rest = rest.replace(collected, '')
    if year_raw:
        rest = rest.replace(year_raw[0], '').strip()
    title = rest.strip() if rest.strip() else None
    if not title or not year:
        return None
    result = iamraw.BibliographyReference(
        title=title,
        authors=authors,
        year=year,
        raw=raw,
    )
    return result
