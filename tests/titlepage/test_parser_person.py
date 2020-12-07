# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import pytest

import detector.titlepage.parser.person

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
])
def test_detector_parser_parse_person(raw, expected):
    parsed = detector.titlepage.parser.person.parse(raw)
    assert parsed == expected, str(parsed)


def test_detector_parser_person_order_person():
    persons = [KAHN, GOMEZ, HELMUT]
    expected = (HELMUT, [GOMEZ, KAHN])
    current = detector.titlepage.parser.person.order_persons(persons)

    assert current == expected, str(current)


def test_detector_parser_person_parse_person_without_title():
    raw = '  Vorgelegt von    Helmut Konrad Fahrendholz   '
    expected = iamraw.Person(
        title=iamraw.AcademicTitle.STUDENT,
        name='Fahrendholz',
        firstname='Helmut Konrad',
        raw=raw.strip(),
    )
    parsed = detector.titlepage.parser.person.parse_person_without_title(raw)
    assert parsed == expected


BROKEN_INPUT = """\
Hier steht ein wenig Text

Matrikel-Nummer:
Erstprüfer:

Zweitprüfer: *
"""


def test_detector_parser_person_regression(capsys):
    """The regex matches `Erstprüfer:\n\nZweitprüfer` and fails to
    extract name."""
    # TODO: SOLVE BY BETTER REGEX APPROACH
    parsed = detector.titlepage.parser.person.parse_person_without_title(
        BROKEN_INPUT)
    assert not parsed, str(parsed)
    _, stderr = capsys.readouterr()
    assert '[ERROR]' in stderr  # TODO: REMOVE LATER
