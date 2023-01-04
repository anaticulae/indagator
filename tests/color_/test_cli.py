# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest
import utilatest

import tests
import tests.color_


@tests.ghost
@pytest.mark.usefixtures('td')
@pytest.mark.parametrize('cmd', [
    '--help',
    '--version',
])
def test_color_cli(cmd, mp, capsys):
    """Run help and version command to reach basic test coverage"""
    tests.color_.run(cmd, mp=mp)
    utilatest.write_capsys(capsys)
