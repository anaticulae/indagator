# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator
import typing

import iamraw
import utila


def order_persons(persons: list) -> typing.Tuple[iamraw.Person, iamraw.Persons]:
    """Sort persons by academical rang and return the lowest rang as
    author and the rest as examiner.

    Args:
        persons(Persons): list to order
    Returns:
        author(Person), examines as a list of persons
    """
    if not persons:
        return None
    # sort persons by title and name as a tiebraker
    persons = sorted(persons, key=operator.attrgetter('title', 'name'))
    if persons[0].title in EXAMINERS_TITLES:
        # author was not detected
        return None, persons
    if author_or_examiner(persons[0].raw) == iamraw.AcademicTitle.EXAMINIER:
        # author was not detected
        return None, persons
    author, examiner = persons[0], persons[1:]
    return author, examiner


def author_or_examiner(raw: str) -> iamraw.AcademicTitle:
    """\
    >>> author_or_examiner('Betreuer:')
    <AcademicTitle.EXAMINIER: 16>
    """
    raw = raw.lower()
    if any(item in raw for item in AUTHOR_INTRO):
        return iamraw.AcademicTitle.STUDENT
    if any(item in raw for item in EXAMINER_INTRO):
        return iamraw.AcademicTitle.EXAMINIER
    return iamraw.AcademicTitle.NO_TITLE


def valid_title(title: str) -> bool:
    """\
    >>> valid_title('geb.')
    False
    """
    # TODO: INVESTIGATE VALID LIST OF ACADEMIC TITLES
    title = title.strip().lower()
    if title in TITLE_INVALID:
        return False
    return True


ACADEMIC_TITLES = utila.compiles(r"""
\b
(
    # # PROF_DR
    # (
    #     Prof\.[-]?[ ]?Dr\.(-|[ ])?Ing\.
    # )
    # |
    (?P<PROF>
        Prof\.[-]?[ ]?(em\.)?
    )
    |
    (?P<MASTER>
        M\.A\.|
        M\.[ ]?Sc\.|
        Dipl\.(-|[ ])Ing\.|
        Dipl\.\-\w+
    )
    |
    (?P<BSC>
        B\.?[ ]?Sc\.?|
        B\.A\.
    )
    |
    (?P<DR>
        Dr\.(-|[ ])?(Ing\.)?([ ]?(sc\.|tech\.|h\.c\.|E\.h\.)){0,5}|
        [A-Z\-]{2,4}\.   # ???
    )
)
""")


def extract_titles(title: str) -> list:
    """\
    >>> extract_titles('BSC')
    [<AcademicTitle.BSC:...>]
    >>> extract_titles('(M. Sc.)')
    [<AcademicTitle.MASTER:...>]
    """
    result = ACADEMIC_TITLES.finditer(title)
    if not result:
        return None
    title = []
    for item in result:
        for key, value in item.groupdict().items():
            if not value:
                continue
            if not valid_title(value):
                continue
            title.append(iamraw.AcademicTitle[key])
    return title


EXAMINERS_TITLES = (
    iamraw.AcademicTitle.DR,
    iamraw.AcademicTitle.EXAMINIER,
    iamraw.AcademicTitle.PROF,
    iamraw.PROF_DR,
)

AUTHOR_INTRO = utila.splitlines("""
VON
ANGEFERTIGT
AUTOR
VERFASSER
VORGELEGT
""")

EXAMINER_INTRO = utila.splitlines("""
BETREUER
GUTACHTER
PRÜFER
REFERENT
SUPERVISOR
""")

TITLE_INVALID = utila.splitlines("""
GEB.
""")
