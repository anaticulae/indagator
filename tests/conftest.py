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

import detector

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(detector.ROOT)

PACKAGE = detector.PACKAGE

WORKER = 4

# Put long documents first! If we have the long documents at the end, the
# scheduler gets hungry in the end and runs with low cpu load.
# NOTE: This schedule is ordered by the required runtime on my computer.
RESOURCES = [
    (power.MASTER116_PDF, '0:25,97,98,99,100'),
    power.MASTER098_PDF,
    power.MASTER075_PDF,
    (power.DISS266_PDF, '0,212:251'),
    (power.BACHELOR090_PDF, '0:5,84:90'),
    (power.MASTER110_PDF, '90:110'),
    (power.BACHELOR056_PDF, '47:55'),
    (power.MASTER089_PDF, '68:82'),
    (power.ORDER107_PDF, '90:108'),
    (power.DISS272_PDF, '259:271'),
    power.DOCU027_PDF,
    (power.BACHELOR111_PDF, '70:91'),
    (power.BACHELOR076_PDF, '0:5'),
    (power.BACHELOR109_PDF, '0:5,70:80'),
    (power.MASTER072_PDF, '0:10'),
    (power.BACHELOR063_PDF, '0:9,59:62'),
    (power.BACHELOR128_PDF, '96:103'),
    (power.HOME050_PDF, '0:10'),
    (power.BACHELOR241_PDF, '0:10,239,240'),
    (power.BACHELOR051_PDF, '0:10,40:52'),
    (power.DISS205_PDF, '0:5,177,181'),
    (power.MASTER078_PDF, '0:5'),
    (power.BACHELOR037_PDF, '0:10,33:37'),
    (power.BACHELOR075_PDF, '70:74'),
    (power.DISS170_PDF, '0:10,150:163'),
    (power.MASTER091B_PDF, '82:89'),
    (power.MASTER155_PDF, '78:85'),
    (power.MASTER091A_PDF, '0:10'),
    (power.MASTER148_PDF, '109:113'),
    (power.MASTER083_PDF, '74:83'),
    (power.DISS143_PDF, '0:10,131:143'),
    (power.DISS167_PDF, '140:167'),
    (power.DISS172_PDF, '152:172'),
    (power.DISS178_PDF, '166:170'),
    (power.MASTER099B_PDF, '0:5'),
    genex.todo(
        power.BACHELOR067_PDF,
        pages='63:66',
        rawmaker='--char_margin=1.1',
    ),
    power.DOCU007_PDF,
    power.DOCU009_PDF,
]

RESOURCES_NOTITLE = [
    power.MASTER078_PDF,
    power.MASTER072_PDF,
    power.DOCU027_PDF,
    power.DOCU009_PDF,
    power.DOCU007_PDF,
]


def extract(resources):
    genex.extract(
        resources,
        destination=power.generated(),
        groupme=True,
        sections=True,
        pdfinfo=True,
        pages=':',
        worker=WORKER,
        base=power.REPOSITORY,
    )


def extract_notitle(resources):
    genex.extract_removepages(
        resources,
        removepages='0',
        folder='notitle',
        worker=WORKER,
        pages='0:10',
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
