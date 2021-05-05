# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import texmex
import utila

import detector.bibliography.judge
import detector.bibliography.layout.alternate
import detector.bibliography.layout.column
import detector.bibliography.layout.vspace
import detector.bibliography.utils


def extracts(
        text: texmex.PageTextNavigators,
        text_oneline: texmex.PageTextNavigators,
) -> iamraw.BibliographyReferences:
    column = detector.bibliography.layout.column.extracts(text)
    alternate = detector.bibliography.layout.alternate.extracts(text_oneline)
    vspace = detector.bibliography.layout.vspace.extracts(text_oneline)

    column = detector.bibliography.judge.judge(column)
    alternate = detector.bibliography.judge.judge(alternate)
    vspace = detector.bibliography.judge.judge(vspace)

    utila.debug(f'column:    {detector.bibliography.utils.count(column)}')
    utila.debug(f'alternate: {detector.bibliography.utils.count(alternate)}')
    utila.debug(f'vspace:    {detector.bibliography.utils.count(vspace)}')

    count_column = detector.bibliography.utils.count(column)
    # alternate extracts a lot of more possible bibs, therefore we
    # have to punish the number of results. HolyValue: 0.5
    count_alternate = detector.bibliography.utils.count(alternate) * 0.7
    count_vspace = detector.bibliography.utils.count(vspace) * 0.5

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
