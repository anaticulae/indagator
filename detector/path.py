# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila


def bibliography_detected(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'detector',
        'bibliography_detected',
        prefix,
    )


def titlepage_detected(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'detector',
        'titlepage_detected',
        prefix,
    )


def formula_detected(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        'detector',
        'formula_formula',
        prefix,
    )
