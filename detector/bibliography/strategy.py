# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import texmex
import utila

import detector.bibliography.invalid
import detector.bibliography.layout.alternate
import detector.bibliography.layout.column
import detector.bibliography.layout.vspace


def extracts(
        text: texmex.PageTextNavigators,
        text_oneline: texmex.PageTextNavigators,
) -> iamraw.BibliographyReferences:
    column = detector.bibliography.layout.column.extracts(text)
    alternate = detector.bibliography.layout.alternate.extracts(text_oneline)
    vspace = detector.bibliography.layout.vspace.extracts(text_oneline)

    column = judge(column)
    alternate = judge(alternate)
    vspace = judge(vspace)

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


INVALID_MAX = configo.HolyTable(
    items=[
        (5, 0),
        (15, 0),
        (30, 3 / 30),
        (100, 10 / 100),
    ],
    right_outranges_none=False,
    left_outranges_none=False,
)


def judge(pages: list) -> bool:
    counted = count(pages)
    if not counted:
        return []
    invalid = 0
    for item in utila.flatten(pages):
        if item is None or detector.bibliography.invalid.single(item):
            invalid += 1
    # determine invalid ratio
    ratio = invalid / counted
    # use greather instead of greather equal to pass zero findings with
    # ration 0.0 and allowed ratio of 0.0
    if ratio > INVALID_MAX(counted):
        # invalid result
        return []
    return pages
