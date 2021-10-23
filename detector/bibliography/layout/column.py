# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import geostrat
import iamraw
import texmex
import utila

import detector.bibliography.layout.utils
import detector.bibliography.layout.vspace
import detector.bibliography.machine.runtime


def extracts(navigators: texmex.PageTextNavigators):
    for strategy in [extract, double_column]:
        result = []
        for navigator in navigators:
            extracted = strategy(navigator)
            if not extracted:
                continue
            if detector.bibliography.layout.utils.invalid_title(extracted):
                continue
            # update pdf page number
            for item in extracted:
                item.raw_pdfpage = navigator.page
            result.append(extracted)
        if result:
            return result
    return []


def extract(content: texmex.PageTextNavigator) -> iamraw.BibliographyReferences:
    layouted = geostrat.parse(content, data_adjust=True)
    if layouted is None:
        return None
    result = []
    for left, right in layouted:
        reference = left[0].text.strip()
        # remove latex reference pattern [FCB87]
        reference = remove_bracket_angle(reference)
        raw = ' '.join(item.text.strip() for item in right)
        parsed = detector.bibliography.machine.runtime.reference(raw)
        parsed.reference = reference
        result.append(parsed)
    return result



def double_column(content: texmex.PageTextNavigator) -> iamraw.BibliographyReferences: # yapf:disable
    parsed = geostrat.parse(content, column_count=2)
    if parsed is None:
        return None
    result = []
    for column in parsed:
        navigator = texmex.PageTextNavigator()
        navigator.data = column
        parsed = detector.bibliography.layout.vspace.extracts([navigator])
        result.extend(utila.flatten(parsed))
    return result


def remove_bracket_angle(reference: str) -> str:
    """Remove bracket angle at start and end of `reference`.

    >>> remove_bracket_angle('[TM12]')
    'TM12'
    >>> remove_bracket_angle('DSB')
    'DSB'
    """
    reference = reference.strip()
    if reference[0] == '[':
        reference = reference[1:]
    if reference[-1] == ']':
        reference = reference[0:-1]
    return reference
