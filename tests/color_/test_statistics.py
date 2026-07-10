# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilotest

import tests
import tests.color_


@tests.ughost
@utilotest.longrun
def test_statistics_master031(td, mp):
    source = hoverpower.MASTER031_PDF
    cmd = f'-i {source} -o {td.tmpdir} --pages=0:10'
    tests.color_.run(cmd, mp=mp)
    loaded = serializeraw.load_color_statistics(content=td.tmpdir)
    assert len(loaded) == 10
