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

import detector.cli
import detector.feature.titlepage
import detector.path
import detector.titlepage
import detector.titlepage.parser.complete
import detector.titlepage.parser.person
import detector.titlepage.strategy


@utilatest.longrun
def test_titlepage_parser():
    extracted = detector.feature.titlepage.work(
        iamraw.path.text(
            power.link(power.DOCU07_PDF),
            prefix='oneline',
        ),
        iamraw.path.textposition(
            power.link(power.DOCU07_PDF),
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


def check_78_pages(titlepage: iamraw.TitlePage):
    assert titlepage.thesis.typ == iamraw.DocumentType.MASTER

    university = titlepage.institution.university
    assert university == 'Technische Universität Darmstadt', str(university)


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


@pytest.mark.parametrize('source, checker', [
    pytest.param(
        power.MASTER072_PDF,
        check_72_pages,
        id='master72',
    ),
    pytest.param(
        power.MASTER078_PDF,
        check_78_pages,
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
        marks=pytest.mark.xfail(reason='improve title page parser')),
])
@utilatest.longrun
def test_detector_feature_titlepage_complete(
        source,
        checker,
        testdir,
        monkeypatch,
):
    """Intergration test to ensure that rawmaker -> detector works correctly."""
    root = str(testdir)
    cmd = (f'rawmaker -i {source} --pages=0:5 '
           f'{detector.feature.titlepage.RAWMAKER_CONFIGURATION}')
    utila.run(cmd)

    cmd = f'-i {root} --titlepage'
    utilatest.run_command(
        cmd,
        process=detector.cli.PROCESS,
        main=detector.cli.main,
        success=True,
        monkeypatch=monkeypatch,
    )
    resultpath = detector.path.titlepage_detected(root)
    titlepage: iamraw.TitlePage = serializeraw.load_titlepage(resultpath)
    assert titlepage

    checker(titlepage)


def parse_titlepages(path: str, pages: tuple = None):
    navigators = serializeraw.create_pagetextnavigators_frompath(path, pages=pages) # yapf:disable
    parsed = detector.feature.titlepage.parse_titlepages(navigators, pages)
    return parsed


@utilatest.longrun
def test_detector_feature_titlepage_select_best():
    parsed = parse_titlepages(power.link(power.MASTER072_PDF), pages=None)
    best = detector.titlepage.strategy.select_best(parsed)
    assert best == parsed[0], str(best)


# @utilatest.longrun
# @pytest.mark.parametrize('source', [
#     pytest.param(item, id=os.path.split(item)[1])
#     for item in tr.NO_TITLE_GENERATED
# ])
# def test_detector_feature_titlepage_select_best_no_titlepage(source):
#     pages = tuple(range(20))
#     parsed = parse_titlepages(source, pages=pages)
#     best = detector.titlepage.select_best(parsed)
#     assert best is None, str(best)

# @pytest.mark.parametrize('pages', [
#     range(1, 5),
#     range(5, 10),
#     range(10, 15),
#     range(20, 25),
#     range(25, 30),
#     range(30, 35),
#     range(35, 40),
#     range(40, 45),
#     range(45, 50),
# ])
# @utilatest.longrun
# def test_detector_feature_titlepage_parse_titlepage_negative(pages):
#     """Split pages to increase mutli-process-testing."""
#     pages = tuple(pages)
#     navigators = serializeraw.create_pagetextnavigators_frompath(
#         tr.MASTER72,
#         pages=pages,
#     )
#     for page in pages:
#         selected = utila.select_page(navigators, page=page)
#         parsed = detector.feature.titlepage.parse_titlepages(
#             navigators=[selected],
#             pages=[page],
#         )
#         selected = detector.titlepage.select_best(parsed)
#         assert not selected, str(f'page: {page}\n{selected}')
