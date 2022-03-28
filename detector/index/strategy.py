# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import geostrat
import iamraw
import serializeraw
import utila


def run(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    pages: tuple = None,
) -> str:
    ptcns = serializeraw.ptcn_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    extracted = extract_pages(ptcns)
    return extracted


def extract_pages(ptcns) -> iamraw.DocumentIndex:
    result = iamraw.DocumentIndex()
    for page in ptcns:
        cat = list(result.data.keys())[-1] if result.data else None
        for key, value in extract_page(page, cat=cat):
            for item in value:
                result.add(
                    cat=key,
                    title=item.title,
                    page=item.page,
                    raw=item.raw,
                    pdfpage=item.pdfpage,
                )
    return result


# Use high diff to ensure that:
# Title
#       for appendices, 34
#       working, 70
# Is handeld as a single column.
COLUMN_DIFF_MAX = configo.HV_INT_PLUS(default=50)


def extract_page(page, cat=None) -> iamraw.DocumentIndex:
    result = iamraw.DocumentIndex()
    parsed = geostrat.parse(
        page,
        column_diff=COLUMN_DIFF_MAX,
    )
    if not parsed:
        return result
    parsed = utila.flatten(parsed)
    for line in parsed:
        text = line.text.strip()
        if len(text) == 1:
            cat = text
            continue
        parsed = parse_pages(text)
        result.add(
            cat=cat,
            title=parsed[0],
            page=parsed[1],
            raw=parsed[2],
            pdfpage=page.page,
        )
    return result


PAGES = utila.compiles(r"""
    ^
    (?P<TEXT>.{4,}?)
    (\,[ ]{0,2})
    (?P<PAGES>
        (
            \d{1,4}
            (\-\d{1,4})?
            ([ ]|\,[ ]{1,2}|$)
        ){1,8}
    )
""")


def parse_pages(line: str) -> tuple:
    """\
    >>> parse_pages('Wisdom, 104, 105, 116')
    ('Wisdom', '104, 105, 116', 'Wisdom, 104, 105, 116')
    >>> parse_pages('Word processing')
    ('Word processing', None, 'Word processing')
    """
    parsed = PAGES.match(line)
    if not parsed:
        return line, None, line
    text = parsed['TEXT']
    pages = parsed['PAGES']
    return text, pages, parsed[0]
