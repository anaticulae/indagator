# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import indagator.path
import tests.detector_


@pytest.mark.xfail(reason='???')
@utilatest.requires(power.MASTER116_PDF)
def test_formula_cli_master116_page22(td, mp):
    source = power.link(power.MASTER116_PDF)
    command = f'-i {source}  --formula --pages=22'
    tests.detector_.run(command, mp=mp)

    formulas = indagator.path.formula_detected(td.tmpdir)
    formulas = serializeraw.load_formulas(formulas)
    formulas = utila.select_content(formulas, page=22)

    assert len(formulas) == 4
    expected = [1, 4, 7, 9]
    current = [formula.line for formula in formulas]
    assert current == expected
