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
import utila

import detector

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

RESTRUCT = os.path.join(GENERATED, 'restruct')
RESTRUCT_PDF = os.path.join(DOCU, 'restructuredtext.pdf')
RESTRUCT_CHAPTER_COUNT = 8
RESTRUCT_TOC_LINES = 13

HOWTO_PYPORTING = os.path.join(GENERATED, 'howto_pyporting')
HOWTO_PYPORTING_PDF = os.path.join(DOCU, 'howto_pyporting.pdf')
# the simple example has two 2 chapters, but there are on the same page,
# therfore 1 page_count.
# TODO: Change after removed xfail, see: test_sections_extract_sections_simple
HOWTO_PYPORTING_CHAPTER_PAGE_COUNT = 1  # change to 2
HOWTO_PYPORTING_HEADLINES_PAGE_3 = 4
HOWTO_PYPORTING_TOC_LINES = 12

# porting module
PYPORTING = os.path.join(GENERATED, 'porting_module')
PYPORTING_PDF = os.path.join(DOCU, 'porting_extension_modules.pdf')
PYPORTING_CHAPTER_COUNT = 6

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
    HOWTO_PYPORTING_PDF,
    MASTER72_PDF,
    MASTER78_PDF,
    PYPORTING_PDF,
    RESTRUCT_PDF,
]
NO_TITLE_GENERATED = [
    os.path.join(NO_TITLE, item)
    for item in utila.simplify_testfile_names(NO_TITLE_EXAMPLE)
]

NO_TITLE_RESTRUCTURED = os.path.join(NO_TITLE, 'docu_restructuredtext')

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
    HOWTO_PYPORTING,
    HOWTO_PYPORTING_PDF,
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
    PYPORTING,
    PYPORTING_PDF,
    RESOURCES,
    RESTRUCT,
    RESTRUCT_PDF,
]

REQUIRED_RESOURCES = [utila.forward_slash(item) for item in REQUIRED_RESOURCES]
