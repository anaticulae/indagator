# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses
import functools

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import detector.path
import tests.conftest
import tests.detector_

ARCHIVE = utila.join(
    detector.ROOT,
    'tests/detector_/titlepage/expected',
    exist=True,
)


def bachelor37(titlepage: iamraw.TitlePage):
    assert titlepage
    assert len(titlepage.examiner) == 2, titlepage.examiner


def bachelor76(titlepage: iamraw.TitlePage):
    assert titlepage

    assert titlepage.matrikel.number == 70409886, titlepage.matrikel
    assert titlepage.date.raw == '25.05.2018', titlepage.date
    assert titlepage.thesis.raw == 'Bachelorarbeit', titlepage.thesis.raw

    assert titlepage.author.name == 'Haubrock', titlepage.author
    assert len(titlepage.examiner) == 2, titlepage.examiner


def master98(titlepage: iamraw.TitlePage):
    assert titlepage
    assert len(titlepage.examiner) == 2, titlepage.examiner
    assert titlepage.institution, titlepage.institution
    assert titlepage.thesis.typ == iamraw.DocumentType.MASTER, titlepage.thesis
    assert titlepage.date, titlepage.date


def bachelor241(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.thesis.typ == iamraw.DocumentType.BACHELOR
    assert titlepage.title == (
        'SOLAR II - Komplexe Modellierung von beruﬂichen '
        'Allergierisiken und Simulation zur Anwendung von Imputationsmethoden')
    assert len(titlepage.examiner) == 3, titlepage.examiner


def master78(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.matrikel.number == 1024577
    assert len(titlepage.examiner) == 2
    assert titlepage.title == (
        'Entwicklung eines Softwaresystems zur Planung'
        ' und Inbetriebnahme von Gebäudeautomationssystemen')


def homework50(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.thesis.typ == iamraw.DocumentType.HOMEWORK
    assert titlepage.title == 'Implementierung eines Leistungsmesssystem auf dem MSP430'
    assert len(titlepage.examiner) == 3, titlepage.examiner


def bachelor51(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.author.name == 'Ilja'
    assert titlepage.author.firstname == 'Laas'
    assert titlepage.thesis.typ == iamraw.DocumentType.BACHELOR
    # assert len(titlepage.examiner) == 2, titlepage.examiner


def diss170(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.author.name == 'Dunger'
    assert len(titlepage.examiner) == 3


def master91a(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.author.name == 'Sprengel'
    assert len(titlepage.examiner) == 2


def bachelor109(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.examiner


def diss143(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.author
    assert titlepage.examiner
    assert len(titlepage.examiner) == 4


def master075(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.author


def master099b(titlepage: iamraw.TitlePage):
    assert titlepage
    assert titlepage.author
    assert titlepage.examiner


def master063(titlepage: iamraw.TitlePage):
    # assert titlepage.author
    assert titlepage.examiner
    assert titlepage.institution


@pytest.mark.parametrize('source, check', [
    pytest.param(
        power.HOME050_PDF,
        homework50,
        id='homework50',
        marks=pytest.mark.xfail(reason='improve headline parser'),
    ),
    pytest.param(power.BACHELOR037_PDF, bachelor37, id='bachelor37'),
    pytest.param(power.BACHELOR051_PDF, bachelor51, id='bachelo51'),
    pytest.param(power.BACHELOR076_PDF, bachelor76, id='bachelor76'),
    pytest.param(power.BACHELOR109_PDF, bachelor109, id='bachelor109'),
    pytest.param(
        power.BACHELOR241_PDF,
        bachelor241,
        id='bachelor241',
        marks=pytest.mark.xfail(reason='improve headline parser'),
    ),
    pytest.param(
        power.MASTER078_PDF,
        master78,
        id='master78',
        marks=pytest.mark.xfail(reason='improve headline parser'),
    ),
    pytest.param(power.MASTER091A_PDF, master91a, id='master91a'),
    pytest.param(power.MASTER098_PDF, master98, id='master98'),
    pytest.param(power.DISS170_PDF, diss170, id='diss170'),
    pytest.param(power.DISS143_PDF, diss143, id='diss143'),
    pytest.param(power.MASTER075_PDF, master075, id='master075'),
    pytest.param(power.MASTER063_PDF, master063, id='master063'),
    pytest.param(
        power.MASTER099B_PDF,
        master099b,
        id='master099b',
        marks=pytest.mark.xfail(reason='require image detector'),
    ),
])
@utilatest.longrun
def test_validate_titlepage_extractor(source, check, testdir, monkeypatch):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} -o {testdir.tmpdir} --title --page=0'

    tests.detector_.run(cmd, monkeypatch=monkeypatch)

    source = detector.path.titlepage_detected(testdir.tmpdir)
    titlepage = serializeraw.load_titlepage(source)
    check(titlepage)


RESOURCES = [
    item[0] if isinstance(item, tuple) else item
    for item in tests.conftest.RESOURCES
]
RESOURCES = [pytest.param(item, id=utila.file_name(item)) for item in RESOURCES]


@utilatest.longrun
@pytest.mark.parametrize('source', RESOURCES)
def test_validate(
    source,
    testdir,
    monkeypatch,
):
    TitleCompare(
        source,
        testdir,
        monkeypatch,
    ).evaluate()


class TitleCompare(utilatest.BaseLiner):

    def __init__(self, source, testdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.detector_.run,
                monkeypatch=monkeypatch,
            ),
            step='titlepage',
            pages=':',
            source=source,
            workdir=testdir.tmpdir,
            archive=ARCHIVE,
            loader=serializeraw.load_titlepage,
        )

    def load(self) -> str:
        path = detector.path.titlepage_detected(self.workdir)
        loaded = self.loader(path)
        return loaded

    def raw(self, value) -> str:
        if not value:
            return 'NO TITLE PAGE'
        author = ''
        if value.author:
            author = f'{value.author.title.name}    '
            author += f'{value.author.firstname}    {value.author.name}    '
            author += value.author.raw.replace('\n', ' ')
        thesis = ''
        if value.thesis:
            thesis = f'{value.thesis.typ.name}    {value.thesis.title}'
        examiner = [
            f'{item.title.name}    {item.raw}'.replace('\n', ' ')
            for item in value.examiner
        ]
        examiner: str = '\n                    '.join(examiner)
        data = dict(
            author=author,
            title=value.title,
            thesis=thesis,
            date=value.date.raw if value.date else None,
            matrikel=value.matrikel.number if value.matrikel else None,
            examiner=examiner,
        )
        result = utila.dict_dump(data)
        # remove trailing white spaces
        result: str = '\n'.join(item.rstrip() for item in result.splitlines())
        return result
