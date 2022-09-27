# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests
import tests.color_


@tests.ghost
@utilatest.nightly
def test_large_pdf(td, mp):
    source = power.MASTER193_PDF
    cmd = f'-i {source} -o {td.tmpdir}'
    tests.color_.run(cmd, mp=mp)
    loaded = serializeraw.load_color_statistics(content=td.tmpdir)
    assert len(loaded) == 193


@tests.ghost
def test_book173_nocolor(td, mp):
    """Number of possible color in histogram was to low.

    After increasing number of colors, everything works fine.
    """
    source = power.BOOK173_PDF
    cmd = f'-i {source} -o {td.tmpdir} --page=0'
    tests.color_.run(cmd, mp=mp)
    loaded = serializeraw.load_color_statistics(content=td.tmpdir)
    assert len(loaded) == 1


@tests.ghost
def test_non_zero_pagestart(td, mp):
    """Ensure that first page does not always start with zero.

    If only parts of document is rendered, align these page numbers.
    """
    source = power.BOOK173_PDF
    cmd = f'-i {source} -o {td.tmpdir} --page=10:15,20:25'
    tests.color_.run(cmd, mp=mp)
    loaded = serializeraw.load_color_statistics(content=td.tmpdir)
    assert len(loaded) == 10
    expected = [10, 11, 12, 13, 14, 20, 21, 22, 23, 24]
    pages = [item.page for item in loaded]
    assert pages == expected
