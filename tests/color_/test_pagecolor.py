# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower

import color.pagecolor
import tests


@tests.ughost
def test_colors():
    """Extract list of rgb colors with color count."""
    source = hoverpower.MASTER031_PDF
    colors = list(color.pagecolor.colors(
        source,
        pages=0,
    ))
    assert len(colors) == 1
    firstpage = colors[0]
    expected = 569  # different colors
    assert len(firstpage) == expected


@tests.ughost
def test_histogram():
    source = hoverpower.MASTER031_PDF
    detected = list(color.pagecolor.colors(
        source,
        pages=0,
    ))
    histogram = color.pagecolor.histogram(
        detected[0],
        count_min=50,
    )
    assert len(histogram) == 18
