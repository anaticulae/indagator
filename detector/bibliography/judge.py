# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import detector.bibliography.utils

TITLE_MIN_LENGTH = 10

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


def judge(pages: list) -> list:
    counted = detector.bibliography.utils.count(pages)
    if not counted:
        return []
    invalid = 0
    for item in utila.flatten(pages):
        if item is None or invalid_single(item):
            invalid += 1
    # determine invalid ratio
    ratio = invalid / counted
    # use greather instead of greather equal to pass zero findings with
    # ration 0.0 and allowed ratio of 0.0
    if ratio > INVALID_MAX(counted):
        # invalid result
        return []
    return pages


def invalid_single(item: iamraw.BibliographyReference) -> bool:
    if item.title:
        if len(item.title) < TITLE_MIN_LENGTH:
            return True
    return False
