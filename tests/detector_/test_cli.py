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

import tests.detector_


@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('cmd', [
    '--help',
    '--version',
])
def test_misc(cmd, mp, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.detector_.run(cmd, mp=mp)
    utilatest.write_capsys(capsys)


@pytest.mark.parametrize('source', [
    pytest.param(power.DOCU007_PDF, id='docu007'),
    pytest.param(power.DOCU009_PDF, id='docu009'),
    pytest.param(power.DOCU027_PDF, id='docu027'),
])
@utilatest.longrun
def test_run_work(source, td, mp, capsys):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} -o {td.tmpdir}'
    with utilatest.increased_filecount(td.tmpdir, mindiff=3, maxdiff=3):
        tests.detector_.run(cmd, mp=mp)
    utilatest.write_capsys(capsys)
