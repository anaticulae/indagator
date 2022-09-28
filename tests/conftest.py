# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import detector

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(detector.ROOT)

PACKAGE = detector.PACKAGE

RESOURCES = [
    (power.BACHELOR037_PDF, '0:10'),
    (power.BACHELOR051_PDF, '0:10'),
    (power.BACHELOR076_PDF, '0:5'),
    (power.BACHELOR090_PDF, '0:5'),
    (power.BACHELOR109_PDF, '0:5'),
    (power.BACHELOR241_PDF, '0:10'),
    (power.BOOK173_PDF, '164:173'),
    (power.DISS143_PDF, '0:10'),
    (power.DISS170_PDF, '0:10'),
    (power.DISS205_PDF, '0:5'),
    (power.DOCU027_PDF, '0:10'),
    (power.HOME050_PDF, '0:10'),
    (power.MASTER063_PDF, '0:5'),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER075_PDF, '0:10'),
    (power.MASTER078_PDF, '0:5'),
    (power.MASTER091A_PDF, '0:10'),
    (power.MASTER098_PDF, '0:10'),
    (power.MASTER099B_PDF, '0:5'),
    (power.MASTER116_PDF, '0:25'),
    (power.MASTER193_PDF, '0'),
    power.DOCU007_PDF,
    power.DOCU009_PDF,
]

WORKER = utilatest.worker_count(6, onci=len(RESOURCES))

RESOURCES_NOTITLE = [
    power.DOCU007_PDF,
    power.DOCU009_PDF,
    power.DOCU027_PDF,
    power.MASTER072_PDF,
    power.MASTER078_PDF,
]


def extract(resources):
    genex.extract(
        resources,
        pagenumber=True,
        footnote=True,
        sections=True,
        pages=':',
        worker=WORKER,
    )


def extract_notitle(resources):
    worker = len(RESOURCES_NOTITLE)
    genex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        worker=worker,
        pages='0:10',
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
