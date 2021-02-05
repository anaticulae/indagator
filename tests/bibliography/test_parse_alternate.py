# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import detector.bibliography.layout.alternate


@pytest.mark.parametrize('pages, expected', [
    (97, 14),
    (98, 14),
    (99, 15),
    (100, 3),
])
@utilatest.skip_longrun
def test_parse_bibliography_master116_page_x(pages, expected):
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.MASTER116_PDF),
        prefix='oneline',
        pages=pages,
    )
    parsed = detector.bibliography.layout.alternate.extracts(navigators)
    parsed = utila.flatten(parsed)
    assert len(parsed) == expected, str(parsed)


def test_parse_bibliography_hurenkind():
    expected = 7  # VALIDATED; 8 with item from before, but item in not completed
    pages = (51,)
    navigators = serializeraw.create_pagetextnavigators_frompath(
        power.link(power.BACHELOR056_PDF),
        prefix='oneline',
        pages=pages,
    )
    parsed = detector.bibliography.layout.alternate.extracts(navigators)
    parsed = utila.flatten(parsed)
    assert len(parsed) == expected, str(parsed)
