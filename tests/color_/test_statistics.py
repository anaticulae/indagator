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


@utilatest.longrun
def test_statistics_master031(testdir, monkeypatch):
    source = power.MASTER031_PDF
    cmd = f'-i {source} -o {testdir.tmpdir} --pages=0:10'
    tests.color_.run(cmd, monkeypatch=monkeypatch)
    loaded = serializeraw.load_color_statistics(content=testdir.tmpdir)
    assert len(loaded) == 10
