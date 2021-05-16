# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests


@pytest.mark.usefixtures('testdir')
@pytest.mark.parametrize('cmd', [
    ['--help'],
    ['--version'],
])
def test_detector_misc(cmd, monkeypatch, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.run(cmd, monkeypatch=monkeypatch)
    utilatest.write_capsys(capsys)


@pytest.mark.parametrize('example', [
    pytest.param(power.DOCU07_PDF, id='howto_pyporting'),
    pytest.param(power.DOCU09_PDF, id='pyporting'),
    pytest.param(power.DOCU27_PDF, id='restructured'),
])
@utilatest.longrun
def test_detector_run_work(example, testdir, monkeypatch, capsys):
    example = power.link(example)
    cmd = f'-i {example} -o {testdir.tmpdir}'

    with utilatest.increased_filecount(testdir.tmpdir, mindiff=3, maxdiff=3):
        tests.run(cmd, monkeypatch=monkeypatch)

    utilatest.write_capsys(capsys)
