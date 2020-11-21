# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex

import detector.bibliography.alternate
import detector.bibliography.column
import detector.bibliography.data
import detector.bibliography.vspace


def extracts(
        text: texmex.PageTextNavigators,
        text_oneline: texmex.PageTextNavigators,
) -> iamraw.BibliographyReferences:
    column = detector.bibliography.column.extracts(text)
    alternate = detector.bibliography.alternate.extracts(text_oneline)
    vspace = detector.bibliography.vspace.extracts(text_oneline)

    count_column = count(column)
    # alternate extracts a lot of more possible bibs, therefore we
    # have to punish the number of results. HolyValue: 0.5
    count_alternate = count(alternate) * 0.7
    count_vspace = count(vspace) * 0.5

    count_best, best = count_column, column
    for value, selected in [
        (count_alternate, alternate),
        (count_vspace, vspace),
    ]:
        if value < count_best:
            continue
        count_best = value
        best = selected
    return best


def count(pages) -> int:
    result = 0
    for page in pages:
        result += len(page)
    return result
