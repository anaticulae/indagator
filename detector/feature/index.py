# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import serializeraw

import detector.index.strategy


def work(
    text: str,
    textpositions: str,
    sizeandborder: str,
    headerfooter: str,
    pages: tuple = None,
) -> str:
    extracted = detector.index.strategy.run(
        text,
        textpositions,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
    # dump result
    dumped = serializeraw.dump_index(extracted)
    return dumped
