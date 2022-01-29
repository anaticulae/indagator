# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

FIRST = """
Fakultät IV
Institut für gute Getränke

Modellierung und Simulation eines hybriden Lokomotivantriebs

Masterarbeit

vorgelegt von:

B.Sc. Helmut Konrad Fahrendholz 321240

Hochschullehrer: Prof. Dr.-Ing. Cuba Libre
Zweitgutachter: Prof. Dr.-Ing. Coffee Lover
Betreuer: Dipl. Ing. Thomas MÜller

Technische Universität Berlin, Fakultät IV, Institut für gute Getränke,
Fachgebiet Trinken und Essen,

Berlin, 19. April 2016
"""

FIRST_INSTITUTION = iamraw.Institution(
    courseofstudies=None,
    department=None,
    field='Trinken und Essen',
    institute='gute Getränke',
    university='Technische Universität Berlin',
)
FIRST_EXPECTED = iamraw.TitlePage(
    # title='Modellierung und Simulation eines hybriden Lokomotivantriebs',
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        'Masterarbeit',
        'Masterarbeit',
    ),
    date=iamraw.TitleDate(
        2016,
        4,
        19,
        'Berlin',
        True,
        'Berlin, 19. April 2016',
    ),
    author=iamraw.Person(
        'Fahrendholz',
        'Helmut Konrad',
        iamraw.AcademicTitle.BSC,
        raw='B.Sc. Helmut Konrad Fahrendholz',
    ),
    matrikel=iamraw.Matrikel(321240, '', '321240'),
    examiner=[
        iamraw.Person(
            'MÜller',
            'Thomas',
            iamraw.AcademicTitle.MASTER,
            raw='Betreuer: Dipl. Ing. Thomas MÜller',
        ),
        iamraw.Person(
            'Libre',
            'Cuba',
            iamraw.PROF_DR,
            raw='Hochschullehrer: Prof. Dr.-Ing. Cuba Libre',
        ),
        iamraw.Person(
            'Lover',
            'Coffee',
            iamraw.PROF_DR,
            raw='Zweitgutachter: Prof. Dr.-Ing. Coffee Lover',
        ),
    ],
    institution=FIRST_INSTITUTION,
    pageraw=-1,
)

SECOND = """
Steuerung und Überwachung intelligenter Gebäudetechnik

Masterarbeit

zur Erlangung des akademischen Grades Master of Science
an der Hochschule für Technik und Wirtschaft Berlin,
Fachbereich Wirtschaftswissenschaften II,
Studiengang Angewandte Kunst

vorgelegt von B.Sc. Thomas Helmer
Matrikelnummer: 161647

1. Betreuer: Prof. Dr. Carsten Semilov
2. Betreuer: Dr.-Ing. Dirk Contemporary

Berlin, den 8. August 2015
"""

SECOND_FONTSTORE = None

SECOND_INSTITUTION = iamraw.Institution(
    university='Hochschule für Technik und Wirtschaft Berlin',
    field='Wirtschaftswissenschaften II',
    courseofstudies='Angewandte Kunst',
)
SECOND_EXPECTED = iamraw.TitlePage(
    # title='Steuerung und Überwachung intelligenter Gebäudetechnik',
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        'Masterarbeit',
        'Masterarbeit',
    ),
    date=iamraw.TitleDate(
        2015,
        8,
        8,
        'Berlin',
        True,
        'Berlin, den 8. August 2015',
    ),
    author=iamraw.Person(
        'Helmer',
        'Thomas',
        iamraw.AcademicTitle.BSC,
        raw='vorgelegt von B.Sc. Thomas Helmer',
    ),
    matrikel=iamraw.Matrikel(
        161647,
        'Matrikelnummer:',
        'Matrikelnummer: 161647',
    ),
    examiner=[
        iamraw.Person(
            'Contemporary',
            'Dirk',
            iamraw.AcademicTitle.DR,
            raw='2. Betreuer: Dr.-Ing. Dirk Contemporary',
        ),
        iamraw.Person(
            'Semilov',
            'Carsten',
            iamraw.PROF_DR,
            raw='1. Betreuer: Prof. Dr. Carsten Semilov',
        ),
    ],
    institution=SECOND_INSTITUTION,
    pageraw=-1,
)

THIRD = """
Technische Universität Berlin

Fakultät I – Geisteswissenschaften
Institut für Sprache und Kommunikation
Studiengang: Kommunikation und Sprache
Studienschwerpunkt: Medienwissenschaft

Identittsbildung 2.0
Selbstdarstellung und Privatheit im Social Web
___________________________________________________________________


Masterarbeit
Vorgelegt von   Tabea Canham



Gutachter:    Prof. Dr. Nobert Bolz
Zweitgutachter:  Dipl.-Medienberater Stephan Frühwirt


Abgabedatum:   31.7.2014
"""

THIRD_INSTITUTION = iamraw.Institution(
    courseofstudies='Kommunikation und Sprache',
    department='Geisteswissenschaften',
    institute='Sprache und Kommunikation',
    university='Technische Universität Berlin',
)

THIRD_EXPECTED = iamraw.TitlePage(
    institution=THIRD_INSTITUTION,
    author=iamraw.Person(
        title=iamraw.AcademicTitle.STUDENT,
        name='Canham',
        firstname='Tabea',
        raw='Vorgelegt von   Tabea Canham',
    ),
    date=iamraw.TitleDate(
        year=2014,
        month=7,
        day=31,
        location=None,
        valid=False,  # TODO: Check why invalid
        raw='31.7.2014',
    ),
    examiner=[
        iamraw.Person(
            title=iamraw.AcademicTitle.MASTER,
            name='Frühwirt',
            firstname='Stephan',
            raw='Dipl.-Medienberater Stephan Frühwirt',
        ),
        iamraw.Person(
            title=iamraw.PROF_DR,
            name='Bolz',
            firstname='Nobert',
            raw='Prof. Dr. Nobert Bolz',
        ),
    ],
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        title='Masterarbeit',
        raw='Masterarbeit',
    ),
    pageraw=-1,
)

FOURTH = """\
THE IMPACT OF EMOTIONAL RATINGS
ON RISK BEHAVIOR

by
Venja Och
B. Sc., Humboldt-Universität zu Berlin, 2012
(Student No. 532196)

Thesis Submitted in Partial Fulfillment
of the Requirements for the Degree of
Master of Science (M. Sc.)

in the
Department of Psychology
Faculty of Mathematics and Natural Sciences II

Primary Supervisor: Prof. Dr. T. Schubert
Secondary Supervisor: Dr. A. Weinreich

January 22, 2014
"""

FOURTH_EXPECTED = iamraw.TitlePage(
    title='',
    thesis=iamraw.TitleThesisType(
        iamraw.DocumentType.MASTER,
        title='Master',
        raw='Master',
    ),
    date=iamraw.TitleDate(
        year=2014,
        month=1,
        day=22,
        location=None,
        valid=True,
        raw='January 22, 2014',
    ),
    author=iamraw.Person(
        title=iamraw.AcademicTitle.NO_TITLE,
        name='Och',
        firstname='Venja',
        raw='by\nVenja Och',
    ),
    matrikel=iamraw.Matrikel(number=2012, intro=',', raw=', 2012'),
    examiner=[
        iamraw.Person(
            title=iamraw.AcademicTitle.DR,
            name='Weinreich',
            firstname='A.',
            raw='Secondary Supervisor: Dr. A. Weinreich',
        ),
        iamraw.Person(
            title=iamraw.PROF_DR,
            name='Schubert',
            firstname='T.',
            raw='Primary Supervisor: Prof. Dr. T. Schubert',
        ),
    ],
    institution=iamraw.Institution(
        courseofstudies=None,
        department='Mathematics and Natural Sciences II',
        field='Psychology',
        institute=None,
        university='Humboldt-Universität zu Berlin',
    ),
    pageraw=-1,
)
