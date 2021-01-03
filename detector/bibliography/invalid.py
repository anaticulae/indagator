# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

TITLE_MIN_LENGTH = 10


def single(item: iamraw.BibliographyReference) -> bool:
    if item.title:
        if len(item.title) < TITLE_MIN_LENGTH:
            return True
    return False
