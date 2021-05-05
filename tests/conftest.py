# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import genex
import power
import pytest
import utila
import utilatest

import detector

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(detector.ROOT)

PACKAGE = detector.PACKAGE

WORKER = 4

# Put long documents first! If we have the long documents at the end, the
# scheduler gets hungry in the end and runs with low cpu load.
# NOTE: This schedule is orderd by the required runtime on my computer.
RESOURCES = [
    (power.MASTER116_PDF, '0:25,97,98,99,100'),
    (power.MASTER098_PDF, None),
    (power.DISS266_PDF, '0,212:251'),
    (power.BACHELOR090_PDF, '0:5,84:90'),
    (power.MASTER110_PDF, '90:110'),
    (power.BACHELOR056_PDF, '47:55'),
    (power.MASTER089_PDF, '68:82'),
    (power.ORDER107_PDF, '90:108'),
    (power.BACHELOR076_PDF, '0:5'),
    (power.MASTER072_PDF, '0:10'),
    (power.MASTER075_PDF, None),
    (power.BACHELOR063_PDF, '0:9,59:62'),
    (power.DOCU07_PDF, None),
    (power.DOCU09_PDF, None),
    (power.DOCU27_PDF, None),
    (power.BACHELOR128_PDF, '96:103'),
    (power.HOME050_PDF, '0:10'),
    (power.BACHELOR241_PDF, '0:10'),
    (power.BACHELOR051_PDF, '0:10'),
    (power.MASTER078_PDF, '0:5'),
    (power.BACHELOR037_PDF, '0:10,33:37'),
    (power.DISS170_PDF, '0:10,150:163'),
    (power.DISS272_PDF, '259:271'),
    (power.MASTER091B_PDF, '82:89'),
    (power.MASTER155_PDF, '78:85'),
    (power.MASTER091A_PDF, '0:10'),
    (power.BACHELOR111_PDF, '70:91'),
]

RESOURCES_NOTITLE = [
    power.DOCU07_PDF,
    power.MASTER078_PDF,
    power.MASTER072_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
]


def extract(resources):
    genex.extract(
        resources,
        destination=power.generated(),
        groupme=True,
        sections=True,
        pages=':',
        worker=WORKER,
        base=power.REPOSITORY,
    )


def extract_notitle(resources):
    destination = power.generated(folder='notitle')
    files = [item[0] if isinstance(item, tuple) else item for item in resources]
    # prepare
    without_titlepage = [
        os.path.join(destination, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(
            files + [power.REPOSITORY],  # ensure correct parent
            sort=False,
        )
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        todo.append(f'jam -i {inpath} -o {outpath} --remove=0')
    utila.run_parallel(todo)

    # generate
    genex.extract(
        without_titlepage,
        destination,
        pages='0:10',
        worker=1,
        base=destination,
    )


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()
