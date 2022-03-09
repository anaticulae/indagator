# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest
import serializeraw
import texmex

import detector.feature.titlepage
import detector.titlepage.parser.complete
import tests.detector_
import tests.detector_.fixtures.titlepage


@pytest.mark.parametrize('page, expected', [
    pytest.param(
        tests.detector_.fixtures.titlepage.FIRST,
        tests.detector_.fixtures.titlepage.FIRST_EXPECTED,
        id='first',
    ),
    pytest.param(
        tests.detector_.fixtures.titlepage.SECOND,
        tests.detector_.fixtures.titlepage.SECOND_EXPECTED,
        id='second',
    ),
    pytest.param(
        tests.detector_.fixtures.titlepage.THIRD,
        tests.detector_.fixtures.titlepage.THIRD_EXPECTED,
        id='third',
    ),
    pytest.param(
        tests.detector_.fixtures.titlepage.FOURTH,
        tests.detector_.fixtures.titlepage.FOURTH_EXPECTED,
        id='fourth',
    ),
])
def test_parse_complete_title_page(page, expected):
    pcn = texmex.create_pagetextnavigator_fromstr(page)
    parsed = detector.titlepage.parser.complete.parse(pcn)
    assert parsed == expected, str(parsed)


def test_parser_complete_dump_and_load_titlepage():
    current = iamraw.TitlePage()

    dumped = serializeraw.dump_titlepage(current)
    assert len(dumped) > 100, str(dumped)

    loaded = serializeraw.load_titlepage(dumped)
    assert loaded == current
