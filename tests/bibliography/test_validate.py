# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import detector.path
import tests


def bachelor63(flat):
    # zero is iamraw.NoPerson
    # numbers iamraw.Person
    expected = [2, 1, 1, 2, 0, 1, 1, 0, 1, 1, 2, 1]
    parsed = []
    for item in flat:
        authors = item.authors
        if not authors:
            parsed.append(None)
            continue
        if all([isinstance(item, iamraw.Person) for item in authors]):
            parsed.append(len(authors))
            continue
        # no person
        parsed.append(0)
    assert parsed == expected


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


# yapf:disable
@pytest.mark.parametrize('source, pages, expected, validate', [
    pytest.param(power.BACHELOR056_PDF, '49:53', 32, None, id='bachelor56', marks=pytest.mark.xfail(reason='improve parser')),
    pytest.param(power.BACHELOR063_PDF, '59', 12, bachelor63, id='bachelor63'),
    pytest.param(power.MASTER116_PDF, '97,98,99,100', 46, master116, id='master116'), # VALIDATED BY HAND
    pytest.param(power.MASTER089_PDF, None, 149, master89, id='master89', marks=pytest.mark.xfail(reason='improve parser')),
    pytest.param(power.BACHELOR090_PDF, '84:89', 52, bachelor90, id='bachelor90'),
    pytest.param(power.MASTER075_PDF, '70', 18, master75, id='master75', marks=pytest.mark.xfail(reason='improve parser')), # VALIDATED BY HAND
    pytest.param(power.MASTER110_PDF, '104:109', 71, master110, id='master110'),
    pytest.param(power.DISS266_PDF, '215:247', 402, None, id='diss266'),
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
    source = power.link(source)
    root = testdir.tmpdir
    command = f'-i {source} -o {root} --bibliography --pages={pages}'
    tests.run(command, monkeypatch=monkeypatch)

    outpath = detector.path.bibliography_detected(root)
    loaded = serializeraw.load_bibliography_reference(outpath)
    flat = utila.flatten(loaded)
    assert len(flat) == expected, str(loaded)

    if validate:
        validate(flat)
