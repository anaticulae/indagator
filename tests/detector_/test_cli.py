# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import tests.detector_


@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('cmd', [
    '--help',
    '--version',
])
def test_misc(cmd, mp, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.detector_.run(cmd, mp=mp)
    utilotest.write_capsys(capsys)


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.DOCU007_PDF, id='docu007'),
    pytest.param(hoverpower.DOCU009_PDF, id='docu009'),
    pytest.param(hoverpower.DOCU027_PDF, id='docu027'),
])
@utilotest.longrun
def test_run_work(source, td, mp, capsys):
    source = hoverpower.link(source)
    utilotest.fixture_requires(source)
    cmd = f'-i {source} -o {td.tmpdir}'
    with utilotest.increased_filecount(td.tmpdir, mindiff=3, maxdiff=3):
        tests.detector_.run(cmd, mp=mp)
    utilotest.write_capsys(capsys)
