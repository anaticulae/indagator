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

import detector
import tests.resources
import tests.resources.update

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = detector.PACKAGE

power.setup(detector.ROOT)

REQUIRED = tests.resources.REQURIED_RESOURCES + tests.resources.NO_TITLE_GENERATED


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run(REQUIRED)


def extract():
    utila.log('synchronize resources')
    tests.resources.update.sync_resources()

    utila.log('extract resources')
    tests.resources.update.extract_examples()
