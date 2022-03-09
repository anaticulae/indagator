# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power

import color.feature.statistics
import tests.color_


def test_statistics_master031(testdir, monkeypatch):
    source = power.MASTER031_PDF
    cmd = f'-i {source} -o {testdir.tmpdir} --pages=0:10'
    tests.color_.run(cmd, monkeypatch=monkeypatch)
    loaded = color.feature.statistics.load_statistics(content=testdir.tmpdir)
    assert len(loaded) == 10
