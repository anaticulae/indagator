# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tests.detector_


@utilatest.requires(power.BOOK173_PDF)
def test_index_book173(testdir, monkeypatch):
    source = power.link(power.BOOK173_PDF)
    command = f'-i {source}  --index --pages=164:173'
    tests.detector_.run(command, monkeypatch=monkeypatch)
    index = serializeraw.load_index(testdir.tmpdir)
    assert len(index) == 810
