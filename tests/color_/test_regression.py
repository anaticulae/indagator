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

import tests.color_


@utilatest.nightly
def test_large_pdf(testdir, monkeypatch):
    source = power.MASTER193_PDF
    cmd = f'-i {source} -o {testdir.tmpdir}'
    tests.color_.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_color_statistics(content=testdir.tmpdir)
    assert len(loaded) == 193


def test_book173_nocolor(testdir, monkeypatch):
    """Number of possible color in histogram was to low.

    After increasing number of colors, everything works fine.
    """
    source = power.BOOK173_PDF
    cmd = f'-i {source} -o {testdir.tmpdir} --page=0'
    tests.color_.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_color_statistics(content=testdir.tmpdir)
    assert len(loaded) == 1
