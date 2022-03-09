# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import detector.titlepage.parser.institution
from tests.detector_.fixtures.titlepage import FIRST
from tests.detector_.fixtures.titlepage import FIRST_INSTITUTION
from tests.detector_.fixtures.titlepage import SECOND
from tests.detector_.fixtures.titlepage import SECOND_INSTITUTION


@pytest.mark.parametrize('example, expected', [
    pytest.param(FIRST, FIRST_INSTITUTION, id='first'),
    pytest.param(SECOND, SECOND_INSTITUTION, id='second'),
])
def test_parser_institution_parse(example, expected):
    parsed, _ = detector.titlepage.parser.institution.parse(example)
    assert parsed == expected, str(parsed)
