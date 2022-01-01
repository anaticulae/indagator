# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import detector.path
import tests


@pytest.mark.xfail(reason='???')
@utilatest.requires(power.MASTER116_PDF)
def test_formula_cli_master116_page22(testdir, monkeypatch):
    source = power.link(power.MASTER116_PDF)
    command = f'-i {source}  --formula --pages=22'
    tests.run(command, monkeypatch=monkeypatch)

    formulas = detector.path.formula_detected(testdir.tmpdir)
    formulas = serializeraw.load_formulas(formulas)
    formulas = utila.select_content(formulas, page=22)

    assert len(formulas) == 4
    expected = [1, 4, 7, 9]
    current = [formula.line for formula in formulas]
    assert current == expected
