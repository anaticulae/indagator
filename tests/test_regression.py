# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests


@utilatest.longrun
@utilatest.requires(power.BACHELOR090_PDF)
def test_regression_detector(testdir, monkeypatch):
    """Start with white page that leads to some trouble with empty
    navigators and problems to detect title page"""
    pattern = '[rawmaker|groupme]*.yaml'
    utila.copy_content(
        power.link(power.BACHELOR090_PDF),
        testdir.tmpdir,
        pattern=pattern,
    )
    jobs = 5
    cmd = f'-j{jobs} --all'
    tests.run(cmd, monkeypatch=monkeypatch)
