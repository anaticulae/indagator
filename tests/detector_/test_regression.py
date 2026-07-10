# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilo
import utilotest

import tests.detector_


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_regression_detector(td, mp):
    """Start with white page that leads to some trouble with empty
    navigators and problems to detect title page.
    """
    pattern = '[rawmaker|groupme]*.yaml'
    utilo.copy_content(
        hoverpower.link(hoverpower.BACHELOR090_PDF),
        td.tmpdir,
        pattern=pattern,
    )
    jobs = 5
    cmd = f'-j{jobs} --all'
    tests.detector_.run(cmd, mp=mp)
