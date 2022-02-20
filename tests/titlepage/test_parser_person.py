# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import detector.titlepage.persons.notitle
import detector.titlepage.persons.person
import detector.titlepage.persons.strategy
import detector.titlepage.persons.utils

HELMUT = iamraw.Person(
    'Fahrendholz',
    'Helmut Konrad',
    iamraw.AcademicTitle.BSC,
    raw='B.Sc. Helmut Konrad Fahrendholz',
)

GOMEZ = iamraw.Person(
    'Gomez',
    'Fabian',
    iamraw.PROF_DR,
    raw='Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
)

KAHN = iamraw.Person(
    'Kahn',
    'Oliver',
    iamraw.PROF_DR,
    raw='Zweitgutachter: Prof. Dr. Oliver Kahn',
)

BIRTH = """\
vorgelegt von
Dipl.-Ing.
Manfred Helmer
geb. in Berlin
"""


@pytest.mark.parametrize('raw, expected', [
    (
        '  B.Sc. Helmut Konrad Fahrendholz',
        HELMUT,
    ),
    (
        'Hochschullehrer: Prof. Dr.-Ing. Fabian Gomez',
        GOMEZ,
    ),
    (
        '  Zweitgutachter: Prof. Dr. Oliver Kahn  ',
        KAHN,
    ),
    (
        'Betreuer VAI:Dipl. Ing. Andreas Zickler   Hier folgt weiterer Text',
        iamraw.Person(
            'Zickler',
            'Andreas',
            iamraw.AcademicTitle.MASTER,
            raw='Betreuer VAI:Dipl. Ing. Andreas Zickler',
        ),
    ),
    (
        'Betreuer: Prof. Dr. Groeg Trichter  ',
        iamraw.Person(
            'Trichter',
            'Groeg',
            iamraw.PROF_DR,
            raw='Betreuer: Prof. Dr. Groeg Trichter',
        ),
    ),
    (
        'Hochschullehrer: Prof.-Dr.-Ing. Clemens Gühmann',
        iamraw.Person(
            'Gühmann',
            'Clemens',
            iamraw.PROF_DR,
            raw='Hochschullehrer: Prof.-Dr.-Ing. Clemens Gühmann',
        ),
    ),
    (
        '2. Betreuer: Dr.-Ing. Dirk Contemporary',
        iamraw.Person(
            'Contemporary',
            'Dirk',
            iamraw.AcademicTitle.DR,
            raw='2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
    ),
    (
        'Erstgutachter: Prof. Dr. rer. biol. hum. Erwin Paulat',
        iamraw.Person(
            'Paulat',
            'Erwin',
            iamraw.PROF_DR,
            raw='Erstgutachter: Prof. Dr. rer. biol. hum. Erwin Paulat',
        ),
    ),
    (
        'Zweitgutachter: Prof. Dr. med. Dr.-Ing. Ronald Verbus-Trapp',
        iamraw.Person(
            'Verbus-Trapp',
            'Ronald',
            iamraw.PROF_DR,
            raw='Zweitgutachter: Prof. Dr. med. Dr.-Ing. Ronald Verbus-Trapp',
        ),
    ),
    (
        '   vorgelegt von   Thomas Helmer  ',
        iamraw.Person(
            'Helmer',
            'Thomas',
            iamraw.AcademicTitle.STUDENT,
            raw='vorgelegt von   Thomas Helmer',
        ),
    ),
    (
        '   Verfasserin: Tina Tomate  ',
        iamraw.Person(
            'Tomate',
            'Tina',
            iamraw.AcademicTitle.STUDENT,
            raw='Verfasserin: Tina Tomate',
        ),
    ),
    (
        'Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt',
        iamraw.Person(
            'Frühwirt',
            'Stephan',
            iamraw.AcademicTitle.MASTER,
            raw='Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt',
        ),
    ),
    (
        'Prof. Dr. Nobert Bolz',
        iamraw.Person(
            'Bolz',
            'Nobert',
            iamraw.PROF_DR,
            raw='Prof. Dr. Nobert Bolz',
        ),
    ),
    (
        'Zweitgutachter: M.A. Erwin Nolte',
        iamraw.Person(
            'Nolte',
            'Erwin',
            iamraw.AcademicTitle.MASTER,
            raw='Zweitgutachter: M.A. Erwin Nolte',
        ),
    ),
    (
        'Zweitprüfer: Peter Thomson',
        iamraw.Person(
            'Thomson',
            'Peter',
            iamraw.AcademicTitle.EXAMINIER,
            raw='Zweitprüfer: Peter Thomson',
        ),
    ),
    (
        'Zweitgutachterin: Aleksandra Filonova, M.A.',
        iamraw.Person(
            'Filonova',
            'Aleksandra',
            iamraw.AcademicTitle.MASTER,
            raw='Zweitgutachterin: Aleksandra Filonova, M.A.',
        ),
    ),
    (
        'Erstgutachter: Herr Prof. Dr. O. T. Wolf',
        iamraw.Person('Wolf', 'O. T.', iamraw.PROF_DR),
    ),
    pytest.param(
        BIRTH,
        iamraw.Person('Helmer', 'Manfred', iamraw.AcademicTitle.MASTER),
        id='multiline',
    ),
])
def test_parser_parse_person(raw, expected):
    parsed = detector.titlepage.persons.strategy.parse_strategies(raw)
    assert parsed == expected, str(parsed)


def test_parser_person_order_person():
    persons = [KAHN, GOMEZ, HELMUT]
    expected = (HELMUT, [GOMEZ, KAHN])
    current = detector.titlepage.persons.utils.order_persons(persons)
    assert current == expected, str(current)


def test_parser_person_parse_person_without_title():
    raw = '  Vorgelegt von    Helmut Konrad Fahrendholz   '
    expected = iamraw.Person(
        title=iamraw.AcademicTitle.STUDENT,
        name='Fahrendholz',
        firstname='Helmut Konrad',
        raw=raw.strip(),
    )
    parsed = detector.titlepage.persons.notitle.parse(raw)
    assert parsed == expected


BROKEN_INPUT = """\
Hier steht ein wenig Text

Matrikel-Nummer:
Erstprüfer:

Zweitprüfer: *
"""


def test_parser_person_regression():
    r"""The regex matches `Erstprüfer:\n\nZweitprüfer` and fails to
    extract name.
    """
    parsed = detector.titlepage.persons.notitle.parse(BROKEN_INPUT)
    assert not parsed, str(parsed)


LONGRUN = """\
Nils Backhaus     Emotionales n-back-Paradigma
Abkürzungsverzeichnis
Abb.        Abbildung
"""


@pytest.mark.timeout(2, method="thread")
def test_person_parser_timeout():
    """Regression test for a long running example."""
    assert not detector.titlepage.persons.person.parse(LONGRUN)
