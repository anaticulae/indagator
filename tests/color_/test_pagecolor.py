# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import color.pagecolor


def test_colors():
    source = power.MASTER031_PDF
    colors = color.pagecolor.colors(
        source,
        pages=0,
    )
    assert len(colors) == 1
    firstpage = colors[0]
    expected = 1191 * 1684  # DPI dependent
    assert len(firstpage) == expected
