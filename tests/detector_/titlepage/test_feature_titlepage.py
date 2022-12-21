# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import detector.cli
import detector.feature.titlepage
import detector.path
import detector.titlepage
import detector.titlepage.parser.complete
import detector.titlepage.persons
import detector.titlepage.strategy


@utilatest.longrun
@utilatest.requires(power.DOCU007_PDF)
def test_titlepage_parser():
    extracted = detector.feature.titlepage.work(
        iamraw.path.text(
            power.link(power.DOCU007_PDF),
            prefix='oneline',
        ),
        iamraw.path.textposition(
            power.link(power.DOCU007_PDF),
            prefix='oneline',
        ),
    )
    assert extracted
    # ensure that result is converted to yaml
    assert isinstance(extracted, str), type(extracted)


def check_72_pages(titlepage: iamraw.TitlePage):
    deparment = titlepage.institution.department
    # TODO: Decide what is the better approach
    # assert deparment == 'Fakultät I – Geisteswissenschaften', str(deparment)
    assert deparment == 'Geisteswissenschaften', str(deparment)


def check_master78(titlepage: iamraw.TitlePage):
    assert titlepage.thesis.typ == iamraw.DocumentType.MASTER
    university = titlepage.institution.university
    assert university == 'Technische Universität Darmstadt', str(university)
    # ensure that author is parsed
    assert titlepage.author
    assert titlepage.thesis, 'check Dokotorarbeit skipped by figure'


def check_116_pages(titlepage: iamraw.TitlePage):
    # TODO: Activate later if we can explain every element on title page
    # assert titlepage.thesis.typ == iamraw.DocumentType.NONE
    assert titlepage.date == iamraw.TitleDate(
        year=2016,
        month=4,
        day=19,
        location='Berlin',
        valid=True,
        raw='Berlin, 19. April 2016',
    )
    expected_title = ('Modellierung und Simulation eines hybriden '
                      'Lokomotivantriebs mit elektrischem Stufenlosgetriebe')
    assert utila.normalize_whitespaces(titlepage.title) == expected_title
    # TODO: Activate later
    author = iamraw.Person(
        'Fahrendholz',
        'Helmut Konrad',
        iamraw.AcademicTitle.STUDENT,
        raw='vorgelegt von:\nHelmut Konrad Fahrendholz',
    )
    assert titlepage.author == author


def check_bachelor90(titlepage: iamraw.TitlePage):
    title = ('Umsetzungen von Algorithmen zur Zustandsdiagnose für '
             'die Anwendung auf einem Embedded System')
    assert titlepage.title == title


def check_diss205(titlepage: iamraw.titlepage):
    assert titlepage.author.name == 'Kirchner'


@pytest.mark.parametrize('source, checker', [
    pytest.param(
        power.DISS205_PDF,
        check_diss205,
        id='diss205',
    ),
    pytest.param(
        power.MASTER072_PDF,
        check_72_pages,
        id='master72',
    ),
    pytest.param(
        power.MASTER078_PDF,
        check_master78,
        id='master78',
    ),
    pytest.param(
        power.MASTER116_PDF,
        check_116_pages,
        id='master116',
    ),
    pytest.param(
        power.BACHELOR090_PDF,
        check_bachelor90,
        id='bachelor90',
        marks=pytest.mark.xfail(reason='improve title page parser'),
    ),
])
@utilatest.longrun
def test_feature_titlepage_complete(
    source,
    checker,
    td,
    mp,
):
    """Integration test to ensure that rawmaker -> detector works correctly."""
    # run rawmaker
    cmd = (f'rawmaker -i {source} --pages=0:5 '
           f'{detector.feature.titlepage.RAWMAKER_CONFIGURATION}')
    utila.run(cmd)
    # run detector
    cmd = f'-i {td.tmpdir} --titlepage'
    utilatest.run_command(
        cmd,
        process=detector.PROCESS,
        main=detector.cli.main,
        expect=True,
        mp=mp,
    )
    resultpath = detector.path.titlepage_detected(td.tmpdir)
    titlepage: iamraw.TitlePage = serializeraw.load_titlepage(resultpath)
    assert titlepage
    # validate result
    checker(titlepage)


def parse_titlepages(path: str, pages: tuple = None):
    navigators = serializeraw.ptn_frompath(path, pages=pages) # yapf:disable
    parsed = detector.feature.titlepage.parse_titlepages(navigators, pages)
    return parsed


@utilatest.longrun
@utilatest.requires(power.MASTER072_PDF)
def test_feature_titlepage_select_best():
    parsed = parse_titlepages(power.link(power.MASTER072_PDF), pages=None)
    best = detector.titlepage.strategy.select_best(parsed)
    assert best == parsed[0], str(best)
