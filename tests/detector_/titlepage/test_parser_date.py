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

from indagator.titlepage.parser.date import parse


@pytest.mark.parametrize(
    'raw, expected',
    [
        (
            'Berlin, den 4. Juni 2010',  # yapf:disable
            iamraw.TitleDate(2010, 6, 4, 'Berlin', True,
                             'Berlin, den 4. Juni 2010'),
        ),
        (
            'Berlino, 19. April 2016',  # yapf:disable
            iamraw.TitleDate(2016, 4, 19, 'Berlino', True,
                             'Berlino, 19. April 2016'),
        ),
        (
            '19. April 2016',
            iamraw.TitleDate(2016, 4, 19, None, True, '19. April 2016'),
        ),
        (
            'INFOTEH-JAHORINA Vol. 14, März 2015.',
            iamraw.TitleDate(2015, 3, 14, None, True, '14, März 2015'),
        ),
        (
            'date: 21.5.1999',
            iamraw.TitleDate(1999, 5, 21, None, False, '21.5.1999'),
        ),
        (
            'Stand: 07.04.2013 ',
            iamraw.TitleDate(2013, 4, 7, None, True, '07.04.2013'),
        ),
        (
            'First printing, Oktober 2004 ',
            iamraw.TitleDate(2004, 10, None, None, True, 'Oktober 2004'),
        ),
        (
            'February 28, 2019',
            iamraw.TitleDate(2019, 2, 28, None, True, 'February 28, 2019'),
        ),
    ])
def test_parse_date(raw, expected):
    parsed = parse(raw)
    assert parsed == expected, str(parsed)
