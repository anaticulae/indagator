# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw

import detector.formula.parser


def formulas(source: str, page: int):
    ptcn = serializeraw.create_pagetextcontentnavigators_frompath(
        power.link(source),
        pages=(page,),
    )[0]
    parsed = detector.formula.parser.parse(ptcn)
    content = parsed.content
    return content


def test_parse_master116_page24():
    content = formulas(source=power.MASTER116_PDF, page=24)
    assert len(content) == 12


def test_parse_master116_page23():
    content = formulas(source=power.MASTER116_PDF, page=23)
    # TODO: merge multiline equations together
    assert len(content) == 17  # not correct, if changed, algo changed


def test_parse_docu09():
    content = formulas(source=power.DOCU09_PDF, page=0)
    assert not content


def test_parse_docu07():
    content = formulas(source=power.DOCU07_PDF, page=0)
    assert not content
