# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import indagator.titlepage.parser.thesis


@pytest.mark.parametrize('raw, expected', [
    (
        'Masterarbeit',
        iamraw.TitleThesisType(
            iamraw.DocumentType.MASTER,
            'Masterarbeit',
            'Masterarbeit',
        ),
    ),
    (
        'Promotion',
        iamraw.TitleThesisType(
            iamraw.DocumentType.DISS,
            'Promotion',
            'Promotion',
        ),
    ),
])
def test_parse_thesis(raw, expected):
    parsed = indagator.titlepage.parser.thesis.parse(raw)
    assert parsed == expected, str(parsed)
