# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import texmex
import utila

import detector.bibliography.data
import detector.bibliography.strategy


def work(  # pylint:disable=R0914
        text: str,
        textpositions: str,
        oneline_text: str,
        oneline_textpositions: str,
        pages: tuple = None,
) -> str:
    # ensure to have connected pages
    pageslist = groupby_diff(pages)

    if len(pageslist) > 1:
        utila.log(f'more than one potential bib section: {len(pageslist)}')

    result = []
    for selected in pageslist:
        text_ = serializeraw.load_document(text, pages=selected)
        textpositions_ = serializeraw.load_textpositions(
            textpositions,
            pages=selected,
        )

        oneline_text_ = serializeraw.load_document(oneline_text, pages=selected)
        oneline_textpositions_ = serializeraw.load_textpositions(
            oneline_textpositions,
            pages=selected,
        )

        textnavigators = texmex.create_pagetextnavigators(
            text_,
            textpositions_,
        )
        onelines = texmex.create_pagetextnavigators(
            oneline_text_,
            oneline_textpositions_,
        )

        extracted = detector.bibliography.strategy.extracts(
            textnavigators,
            onelines,
        )
        result.append(extracted)

    # select best bib ref
    best = longest(result)

    dumped = serializeraw.dump_bibliography_reference(best)
    return dumped


# TODO: MOVE TO UTILA
def groupby_diff(pages: tuple, *, diff=1) -> list:
    """\
    >>> groupby_diff((1, 5, 2, 6, 9))
    [(1, 2), (5, 6), (9,)]
    >>> groupby_diff(None)
    [None]
    >>> groupby_diff((5,))
    [(5,)]
    """
    assert diff >= 0, 'negative diff'
    if not pages:
        return [None]
    pages = sorted(pages)
    result = [[pages[0]]]
    for item in pages[1:]:
        if item - result[-1][-1] <= diff:
            result[-1].append(item)
        else:
            result.append([item])
    result = [tuple(item) for item in result]
    return result


def longest(items):
    """\
    >>> longest([(1, 2, 4), (2, 2, 2, 2), (5, 5, 5)])
    (2, 2, 2, 2)
    """
    # TODO: MOVE TO UTILA
    # TODO: SUPPORT MORE THAN ONE RESULT
    if not items:
        return []
    items = sorted(items, key=len)
    return items[-1]
