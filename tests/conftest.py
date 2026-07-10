# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import indagator

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(indagator.ROOT)

PACKAGE = indagator.PACKAGE

RESOURCES = [
    (hoverpower.BACHELOR037_PDF, '0:10'),
    (hoverpower.BACHELOR051_PDF, '0:10'),
    (hoverpower.BACHELOR076_PDF, '0:5'),
    (hoverpower.BACHELOR090_PDF, '0:5'),
    (hoverpower.BACHELOR109_PDF, '0:5'),
    (hoverpower.BACHELOR241_PDF, '0:10'),
    (hoverpower.BOOK173_PDF, '164:173'),
    (hoverpower.DISS143_PDF, '0:10'),
    (hoverpower.DISS170_PDF, '0:10'),
    (hoverpower.DISS205_PDF, '0:5'),
    (hoverpower.DOCU027_PDF, '0:10'),
    (hoverpower.HOME050_PDF, '0:10'),
    (hoverpower.MASTER063_PDF, '0:5'),
    (hoverpower.MASTER072_PDF, '0:10'),
    (hoverpower.MASTER075_PDF, '0:10'),
    (hoverpower.MASTER078_PDF, '0:5'),
    (hoverpower.MASTER091A_PDF, '0:10'),
    (hoverpower.MASTER098_PDF, '0:10'),
    (hoverpower.MASTER099B_PDF, '0:5'),
    (hoverpower.MASTER116_PDF, '0:25'),
    (hoverpower.MASTER193_PDF, '0'),
    hoverpower.DOCU007_PDF,
    hoverpower.DOCU009_PDF,
]

WORKER = utilotest.worker_count(6, onci=len(RESOURCES))

RESOURCES_NOTITLE = [
    hoverpower.DOCU007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER078_PDF,
]


def extract(resources):
    gennex.extract(
        resources,
        footnote=True,
        groupme='--hefopa',
        headnote=True,
        lock=False,
        pagenumber=True,
        sections=True,
        worker=WORKER,
    )


def extract_notitle(resources):
    worker = len(resources)
    gennex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        worker=worker,
        pages='0:10',
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()
