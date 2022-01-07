# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import german
import iamraw


def parse(raw: str) -> iamraw.Person:
    """\
    >>> parse('Marta Anadon Rosinach')
    Person(name=None..., raw='Marta Anadon Rosinach')
    >>> parse('Higinio Raventos')
    Person(name=None..., raw='Higinio Raventos')
    """
    # TODO:  ENABLE THIS STRATEGY
    # HINT: IN CURRENT STATE, THIS STRATEGY PRODUCES TO MANY FALSE
    # POSITIVE RESULTS
    if not german.isperson(raw):
        return None
    title = iamraw.AcademicTitle.NO_TITLE
    result = iamraw.Person(
        title=title,
        raw=raw,
    )
    return result
