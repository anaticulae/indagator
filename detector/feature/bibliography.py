# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw
import utila

import detector.bibliography.strategy


def work(  # pylint:disable=R0914
        text: str,
        textpositions: str,
        sizeandborderpath: str,
        headerfooterpath: str,
        oneline_text: str,
        oneline_textpositions: str,
        pages: tuple = None,
) -> str:
    # ensure to have connected pages
    if pages:
        pageslist = utila.groupby_diff(pages)
    else:
        # analyze all pages
        pageslist = [None]

    if len(pageslist) > 1:
        utila.log(f'more than one potential bib section: {len(pageslist)}')

    result = []
    for selected in pageslist:
        textnavigators = serializeraw.create_pagetextcontentnavigators_fromfile(
            text,
            textpositions,
            sizeandborderpath,
            headerfooterpath,
            pages=selected,
        )
        onelines = serializeraw.create_pagetextcontentnavigators_fromfile(
            oneline_text,
            oneline_textpositions,
            sizeandborderpath,
            headerfooterpath,
            pages=selected,
        )

        extracted = detector.bibliography.strategy.extracts(
            textnavigators,
            onelines,
        )
        result.append(extracted)

    # select best bib ref
    best = utila.longest(result)
    # remove None items
    best = [[item for item in page if item] for page in best]

    dumped = serializeraw.dump_bibliography_reference(best)
    return dumped
