# C O P Y R I G H T
# =============================================================================
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw

import detector.titlepage.parser.complete

TITLEPAGE_RATING_MIN = configo.HV_INT_PLUS(default=20)


def select_best(pages: 'list[iamraw.TitlePage]') -> iamraw.TitlePage:
    pages = [
        item for item in pages
        if detector.titlepage.parser.complete.valid_titlepage(item)
    ]
    if not pages:
        # no valid page
        return None
    result = pages[0]
    current = rate(result)
    for item in pages[1:]:
        rating = rate(item)
        if rating > current:
            current = rating
            result = item
    if current <= 0:
        # No valid title page detected
        return None
    if current <= TITLEPAGE_RATING_MIN:
        # rating is to low
        # TODO: Handle different than no detection
        return None
    return result


def rate(title: iamraw.TitlePage) -> int:
    # TODO: NOT VERY SMART
    result = 0
    if title.title:
        result += 5
    if title.thesis:
        result += 10
    if title.date:
        result += 10
    if title.matrikel:
        result += 5
    if title.examiner:
        result += 5 * len(title.examiner)
    if title.institution:
        result += 20
    if title.author:
        result += 5
    return result
