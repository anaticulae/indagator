# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import pytest
import serializeraw
import utila
import utilatest

import detector.path
import tests


def file_load(name):
    path = os.path.join(detector.ROOT, f'tests/bibliography/expected/{name}')
    loaded = utila.file_read(path)
    return loaded


def bachelor51(flat):
    assert len(flat) == 37  # VALIDATED


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


def master75(flat):  # pylint:disable=W0613
    pass


def master110(flat):
    titles = [item.title for item in flat if item.title]
    assert len(titles) >= 66  # NOT VALIDATED


def master116(flat):
    expected = [
        'App14', 'Bah12', 'Bas14', 'Bor13', 'Bra11', 'Dit13', 'Don04', 'EB03',
        'EPA98', 'Fil15', 'Fis12', 'Fri15', 'Gas13', 'Gev13', 'Hei13', 'Hof11',
        'IAV15', 'Jaa13', 'Kac14', 'Kon13', 'Kur16', 'Les15', 'LG03', 'Mü13',
        'Mag14', 'MAT16', 'Min13', 'Mor09', 'Nit11', 'Pac12', 'Pap15', 'Pfe14',
        'Rö15', 'Rei10', 'Rie11', 'RNB12', 'Sch09', 'Sko11', 'Spi05', 'Stö10',
        'Tom12', 'Tsc12', 'Vö15', 'Wik07', 'Wik13', 'Wit13'
    ]
    references = [item.reference for item in flat]
    assert references == expected
    authors = [item.authors for item in flat]
    assert authors


def diss170(flat):
    # 11+11+11+12+11+11+11+11+11+13+11+13+5
    assert len(flat) == 146  # change to 142!


def diss272(flat):
    # 11 11 11 9 10 11 11 11 12 11 12 3 = 124
    assert len(flat) == 120  # TODO: CHANGES LATER


def bachelor128(flat):
    assert flat
    # 51: Validated by hand
    assert len(flat) == 47


def master91b(flat):
    assert flat
    assert len(flat) == 85  # VALIDATED


def master148(flat):
    raw = authors_raw(flat)
    utila.log(raw)
    assert flat
    assert len(flat) == 85  # VALIDATED


def authors_raw(flat) -> str:
    items = [' ; '.join([item.raw for item in line.authors]) for line in flat]
    items = [item.strip() for item in items]
    raw = utila.NEWLINE.join(items)
    return raw


# yapf:disable
@pytest.mark.parametrize('source, pages, expected, validate', [
    pytest.param(power.ORDER107_PDF, '104:108', 31, 'order107', id='order107'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR051_PDF, '42:46', 37, bachelor51, id='bachelor51'),
    pytest.param(power.BACHELOR056_PDF, '49:53', 32, 'bachelor056', id='bachelor56'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR063_PDF, '59', 12, 'bachelor063', id='bachelor63', marks=pytest.mark.xfail(reason='improve name detector')),
    pytest.param(power.BACHELOR090_PDF, '84:89', 52, bachelor90, id='bachelor90'),
    pytest.param(power.BACHELOR109_PDF, '72:79', 98, 'bachelor109', id='bachelor109'),
    pytest.param(power.BACHELOR111_PDF, '85:87', 18, 'bachelor111', id='bachelor111'), # VALIDATED BY HAND
    pytest.param(power.BACHELOR128_PDF, '96:103', None, bachelor128, id='bachelor128'),
    pytest.param(power.MASTER075_PDF, '70', 18, master75, id='master75'), # VALIDATED BY HAND
    pytest.param(power.MASTER089_PDF, '70:81', 149, 'master089', id='master89'), # VALIDATED BY HAND
    pytest.param(power.MASTER091B_PDF, '82:89', 85, master91b, id='master91b'), # VALIDATED BY HAND
    pytest.param(power.MASTER110_PDF, '104:109', 71, master110, id='master110'),
    pytest.param(power.MASTER116_PDF, '97,98,99,100', 46, master116, id='master116'), # VALIDATED BY HAND
    pytest.param(power.MASTER148_PDF, '109:114', 38, master148, id='master148', marks=pytest.mark.xfail(reason='handle very bad bibs')), # VALIDATED BY HAND
    pytest.param(power.MASTER155_PDF, '75:85', 111, 'master155', id='master155'), # VALIDATED BY HAND 109
    pytest.param(power.DISS170_PDF, '150:163', None, diss170, id='diss170'),
    pytest.param(power.DISS266_PDF, '215:247', 427, None, id='diss266', marks=pytest.mark.xfail(reason='improve parser')), # VALIDATED BY HAND
    pytest.param(power.DISS272_PDF, '259:271', None, diss272, id='diss272'),
    pytest.param(power.MASTER083_PDF, '75:82', None, 'master083', id='master083'),
    pytest.param(power.MASTER083_PDF, '81', None, 2, id='master083last'),
])
# yapf:enable
@utilatest.longrun
def test_detector_bibliography_run(
    source,
    pages,
    expected,
    validate,
    testdir,
    monkeypatch,
):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} -o {testdir.tmpdir} --bibliography --pages={pages}'
    tests.run(cmd, monkeypatch=monkeypatch)
    # validate
    outpath = detector.path.bibliography_detected(testdir.tmpdir)
    loaded = serializeraw.load_bibliography_reference(outpath)
    flat = utila.flatten(loaded)
    assert len(flat) == expected or expected is None, str(loaded)
    if isinstance(validate, str):
        path = os.path.join(detector.ROOT, f'tests/bibliography/expected/{validate}')  # yapf:disable
        expected = utila.file_read(path).strip()
        raw = authors_raw(flat)
        assert raw == expected
    elif isinstance(validate, int):
        assert len(flat) == validate
    elif validate:
        validate(flat)
