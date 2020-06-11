# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila

import tests


@pytest.mark.parametrize('command', [
    ['--help'],
    ['--version'],
])
def test_detector_misc(command, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    """Run help and version command to reach basic test coverage"""
    tests.run(command, monkeypatch=monkeypatch)

    tests.write_capsys(capsys)


@pytest.mark.parametrize('example', [
    pytest.param(power.link(power.DOCU07_PDF), id='howto_pyporting'),
    pytest.param(power.link(power.DOCU09_PDF), id='pyporting'),
    pytest.param(power.link(power.DOCU27_PDF), id='restructured'),
])
@utila.skip_longrun
def test_detector_run_work(example, testdir, monkeypatch, capsys):  #pylint: disable=W0613
    output = str(testdir)
    command = f'-i {example} -o {output}'

    with utila.increased_filecount(output, mindiff=2, maxdiff=2):
        tests.run(command, monkeypatch=monkeypatch)

    tests.write_capsys(capsys)
