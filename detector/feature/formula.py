# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import detector.formula.parser


def work(
        text: str,
        text_positions: str,
        sizeandborder: str,
        headerfooter: str,
        pages: tuple = None,
) -> str:
    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        text_positions,
        sizeandborder,
        headerfooter,
        pages=pages,
    )
    result = []
    for page in ptcns:
        parsed = detector.formula.parser.parse(page)
        result.append(parsed)

    dumped = serializeraw.dump_formulas(result)
    return dumped
