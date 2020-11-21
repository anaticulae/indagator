# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import detector.bibliography.data
import detector.path
import tests
import tests.resources


def bachelor90(flat):
    references = [item.reference for item in flat]
    expected = [
        'Ju04', 'AT09', 'Bae08', 'BAU11', 'BKL+09', 'Bus98', 'But11', 'CJM12',
        'Dav72', 'DDG09', 'DIN08', 'Dor10', 'DRP01', 'emf12', 'FLS07', 'Fos10',
        'Güe06', 'Hal93', 'Hof08', 'Hue10', 'Ibr04', 'ISO03', 'ISO05', 'JL07',
        'K.11', 'Lig09', 'Mar07', 'Mat09', 'mat12a', 'mat12b', 'mat12c',
        'mis98', 'NN09', 'OK09', 'Ole10', 'Plu06', 'PP04', 'PR06', 'Rei12',
        'Rum05', 'SBD+10', 'Sch05', 'Sta73', 'Sta09', 'Ste12', 'TS07', 'TZ10',
        'VAC+08', 'VG06', 'WL11', 'WR10', 'ZSM11'
    ]
    assert references == expected


def master89(flat):
    first = flat[0]
    assert first.year == 2010
    assert first.authors == [('ABELS', 'Heinz'), ('KÖNIG', 'Alexandra')]

    second = flat[1]
    assert second.year == 2009
    assert second.authors == [('ANDRONIKASHVILI', 'Zaal')]

    last = flat[-1]
    assert last.year == 2009


def master75(flat):
    pass


# yapf:disable
@pytest.mark.parametrize('source, pages, expected, validate', [
    pytest.param(power.link(power.BACHELOR056_PDF), '49:53', 32, None, id='bachelor56'),
    pytest.param(power.link(power.BACHELOR063_PDF), '59', 12, None, id='bachelor63'),
    pytest.param(power.link(power.MASTER116_PDF), '97,98,99,100', 46, None, id='master116'), # VALIDATED BY HAND
    pytest.param(power.link(power.MASTER089_PDF), None, 149, master89, id='master89'),
    pytest.param(power.link(power.BACHELOR090_PDF), '84:89', 52, bachelor90, id='bachelor90'),
    pytest.param(power.link(power.MASTER075_PDF), '70', 18, master75, id='master75'),
])
# yapf:enable
@utilatest.skip_longrun
def test_detector_bibliography_run(
        source,
        pages,
        expected,
        validate,
        testdir,
        monkeypatch,
):  #pylint: disable=W0613
    root = testdir.tmpdir
    command = f'-i {source} -o {root} --bibliography --pages={pages}'
    tests.run(command, monkeypatch=monkeypatch)

    outpath = detector.path.bibliography_detected(root)
    loaded = serializeraw.load_bibliography_reference(outpath)
    flat = utila.flatten(loaded)
    assert len(flat) == expected, str(loaded)

    if validate:
        validate(flat)


def test_unconnected_pages(testdir, monkeypatch, capsys):
    root = testdir.tmpdir
    source = power.link(power.BACHELOR056_PDF)
    pages = '1,2,3,6,7,8'  # invalid pages input

    command = f'-i {source} -o {root} --bibliography --pages={pages}'
    tests.run(command, monkeypatch=monkeypatch)

    stdout, _ = capsys.readouterr()
    assert 'more than one potential bib section' in stdout
