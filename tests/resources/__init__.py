# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import detector

power.setup(detector.ROOT)

RESOURCES = os.path.join(detector.ROOT, 'tests/resources')

GENERATED = os.path.join(RESOURCES, 'generated')

NO_TITLE = os.path.join(GENERATED, 'notitle')

NO_TITLE_EXAMPLE = [
    power.DOCU07_PDF,
    power.MASTER078_PDF,
    power.MASTER072_PDF,
    power.DOCU09_PDF,
    power.DOCU27_PDF,
]
NO_TITLE_GENERATED = [
    os.path.join(NO_TITLE, item)
    for item in utilatest.simplify_testfile_names(NO_TITLE_EXAMPLE)
]

REQUIRED_RESOURCES = [
    power.link(power.DOCU09_PDF),
    power.link(power.DOCU27_PDF),
    RESOURCES,
]

REQUIRED_RESOURCES = [utila.forward_slash(item) for item in REQUIRED_RESOURCES]
