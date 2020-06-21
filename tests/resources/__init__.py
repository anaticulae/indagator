# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import hey
import hey.example
import power
import utila
import utilatest

import detector

power.setup(detector.ROOT)

RESOURCES = os.path.join(detector.ROOT, 'tests/resources')

BACHELOR = os.path.join(RESOURCES, 'bachelor')
BOOK = os.path.join(RESOURCES, 'book')
DOCU = os.path.join(RESOURCES, 'docu')
HOMEWORK = os.path.join(RESOURCES, 'homework')
MASTER = os.path.join(RESOURCES, 'master')
ORDER = os.path.join(RESOURCES, 'order')
TECHNICAL = os.path.join(RESOURCES, 'technical')

GENERATED = os.path.join(RESOURCES, 'generated')
# TODO: remove _ after fixing path bug
NO_TITLE = os.path.join(GENERATED, '_notitle')

BACHELOR56 = os.path.join(GENERATED, 'page_56_hard_to_read')
BACHELOR56_PDF = os.path.join(BACHELOR, 'page_56_hard_to_read.pdf')

BACHELOR63 = os.path.join(GENERATED, 'page_63_images_toc')
BACHELOR63_PDF = os.path.join(BACHELOR, 'page_63_images_toc.pdf')

BACHELOR90 = os.path.join(GENERATED, 'bachelor90')
BACHELOR90_PDF = os.path.join(BACHELOR, 'bachelor90.pdf')

BACHELOR76 = os.path.join(GENERATED, 'page76')
BACHELOR76_PDF = os.path.join(BACHELOR, 'page76.pdf')

MASTER72 = os.path.join(GENERATED, 'page_72_noimages_toc')
MASTER72_PDF = os.path.join(MASTER, 'page_72_noimages_toc.pdf')

MASTER89 = os.path.join(GENERATED, 'page_89_noimages_toc')
MASTER89_PDF = os.path.join(MASTER, 'page_89_noimages_toc.pdf')

MASTER98 = os.path.join(GENERATED, 'master98')
MASTER98_PDF = os.path.join(MASTER, 'page98.pdf')

MASTER116 = os.path.join(GENERATED, 'page_116_images_toc_formular')
MASTER116_PDF = os.path.join(MASTER, 'page_116_images_toc_formular.pdf')

BACHELOR241 = os.path.join(GENERATED, 'page241')
BACHELOR241_PDF = os.path.join(BACHELOR, 'page241.pdf')

MASTER78 = os.path.join(GENERATED, 'page_78_images_toc')
MASTER78_PDF = os.path.join(MASTER, 'page_78_images_toc.pdf')

HOMEWORK50 = os.path.join(GENERATED, 'homework_page_50_math')
HOMEWORK50_PDF = os.path.join(HOMEWORK, 'page_50_math.pdf')

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
    BACHELOR56,
    BACHELOR56_PDF,
    BACHELOR63,
    BACHELOR63_PDF,
    BACHELOR63_PDF,
    BACHELOR76,
    BACHELOR76_PDF,
    BACHELOR90,
    BACHELOR90_PDF,
    HOMEWORK50,
    HOMEWORK50_PDF,
    MASTER116,
    MASTER116_PDF,
    MASTER72,
    MASTER72_PDF,
    MASTER78,
    MASTER78_PDF,
    MASTER89,
    MASTER89_PDF,
    MASTER98,
    MASTER98_PDF,
    power.link(power.DOCU09_PDF),
    power.link(power.DOCU27_PDF),
    RESOURCES,
]

REQUIRED_RESOURCES = [utila.forward_slash(item) for item in REQUIRED_RESOURCES]
