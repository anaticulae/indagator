# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import detector.bibliography.reference.authors as dbra

AUTHORS = """\
Batra, Anil; Bilke-Hentsch, Oliver (Hg.)

""".split('\n\n')


@pytest.mark.parametrize('raw, expected', [
    pytest.param(
        AUTHORS[0],
        [['Batra', 'Anil'], ['Bilke-Hentsch', 'Oliver (Hg.)']],
        id='batra',
    ),
])
def test_author_parser(raw, expected):
    parsed = dbra.parses(raw)
    assert parsed == expected
