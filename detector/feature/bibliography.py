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
    pageslist = utila.groupby_diff(pages)

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
    best = utila.longest(result)

    dumped = serializeraw.dump_bibliography_reference(best)
    return dumped
