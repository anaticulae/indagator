# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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
def test_misc(cmd, monkeypatch, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.run(cmd, monkeypatch=monkeypatch)
    utilatest.write_capsys(capsys)


@pytest.mark.parametrize('source', [
    pytest.param(power.DOCU007_PDF, id='docu007'),
    pytest.param(power.DOCU009_PDF, id='docu009'),
    pytest.param(power.DOCU027_PDF, id='docu027'),
])
@utilatest.longrun
def test_run_work(source, testdir, monkeypatch, capsys):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} -o {testdir.tmpdir}'
    with utilatest.increased_filecount(testdir.tmpdir, mindiff=3, maxdiff=3):
        tests.run(cmd, monkeypatch=monkeypatch)
    utilatest.write_capsys(capsys)
