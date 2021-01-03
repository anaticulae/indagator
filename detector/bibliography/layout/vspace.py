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

import detector.bibliography.layout.alternate


def extracts(navigators: texmex.PageTextContentNavigator
            ) -> iamraw.BibliographyReferences:
    result = []
    for navigator in navigators:
        extracted = extract(navigator)
        if not extracted:
            continue
        result.append(extracted)
    return result


def extract(navigator) -> iamraw.BibliographyReferences:
    grouped = texmex.group_linedistances_complex(
        navigator,
        max_distance=maxdistance,
    )
    grouped = [[navigator[item] for item in group] for group in grouped]
    result = detector.bibliography.layout.alternate.extract(grouped)
    result = utila.not_none(result)
    return result


def maxdistance(size: float):
    # TODO: HOLY VALUE. Support table as holy value
    if size <= 12.0:
        return 15.0
    if size <= 14.5:
        return 30
    if size <= 15.96:
        return 35
    return 50.0
