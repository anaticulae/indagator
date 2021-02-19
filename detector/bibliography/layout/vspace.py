# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import texmex
import utila

import detector.bibliography.layout.alternate


def extracts(navigators: texmex.PageTextContentNavigator
            ) -> iamraw.BibliographyReferences:
    result = []
    for navigator in navigators:
        extracted = extract_optimize(navigator)
        if not extracted:
            continue
        result.append(extracted)
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


def extract(
        navigator: texmex.NavigatorMixin,
        vspace_max: callable = maxdistance,
) -> iamraw.BibliographyReferences:
    grouped = texmex.group_linedistances_complex(
        navigator,
        max_distance=vspace_max,
    )
    grouped = [[navigator[item] for item in group] for group in grouped]
    result = detector.bibliography.layout.alternate.extract(grouped)
    result = utila.not_none(result)
    return result


# TODO: HOLY VALUE
MAXDISTANCE_FACTOR = [
    0.8,
    0.85,
    0.90,
    0.95,
    1.0,
    1.05,
    1.1,
    1.5,
    1.7,
    2.0,
    2.3,
    2.6,
]


def extract_optimize(navigator: texmex.NavigatorMixin,
                    ) -> iamraw.BibliographyReferences:
    results = []
    for factor in MAXDISTANCE_FACTOR:
        adjusted = lambda x: factor * maxdistance(x)  # pylint:disable=cell-var-from-loop
        extracted = extract(navigator, vspace_max=adjusted)
        results.append(extracted)
    # select best
    best = select_best(results)
    return best


def select_best(items: list, selector=len) -> typing.Any:
    # TODO: REPLACE WITH UTILA CODE
    if not items:
        return None
    best = items[0]
    for item in items[1:]:
        if selector(item) < selector(best):
            continue
        best = item
    return best
