# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila


@utila.profile('institution')
def parse(raw: str) -> iamraw.Institution:
    university = find_institution(raw)
    if university:
        university, raw = university
    results = []
    for item in [DEPARTMENT, INSTITUTE, FIELD, COURSES]:
        parsed, raw = detection(raw, item)
        if parsed:
            # TODO: Investigate here
            # assert len(parsed) == 1, str(parsed)
            # select first one, more then one institut is possible
            parsed = parsed[0]
        else:
            parsed = None
        results.append(parsed)

    department, institute, field, courses = results  # pylint:disable=W0632
    result = iamraw.Institution(
        courseofstudies=courses,
        department=department,
        field=field,
        institute=institute,
        university=university,
    )
    if not any(results) and not university:
        # No iamraw.Institution was parsed
        return None, raw
    return result, raw


def detection(raw, items, remove: bool = True):
    if isinstance(items, str):
        items = [items]
    # FIRST DRAFT

    splitted = raw.split(',')
    splitted = utila.flatten([item.split(utila.NEWLINE) for item in splitted])
    splitted = [item for item in splitted if item]  # remove empty items

    result = []
    for item in items:
        for chunk in splitted:
            if not item in chunk:
                continue
            if remove:
                # use words after `collector` as the result
                prepared = chunk.split(item)[1].strip()
                result.append(prepared)
            else:
                result.append(chunk.strip())
            raw.replace(chunk, '')
    # make results unique
    result = utila.make_unique(result)
    return result, raw


SELECTOR = {
    'Akademisch',
    'College',
    'Erlangung',
    'Fachbereich',
    'Fachgebiet',
    'Faktultät',
    'Grad',
    'Grades',
    'Hochschule',
    'Institut für',
    'Institut',
    'Studiengang',
    'Universität',
}

# Replace this approach due regex

INSTITUTE = [
    'Institut für ',
    'Institut',
]

DEPARTMENT = [
    # TODO: Think about chaining in parser, special character?
    # 2 different minus signs
    'Fakultat I –',
    'Fakultat I -',
    'Fakultat I ',
    'Fakultat',
    'Fakultät I –',
    'Fakultät I -',
    'Fakultät I ',
    'Fakultät',
    'Faculty of',
    'Faculty',
]

FIELD = [
    'Fachgebiet',
    'Fachbereich',
    'Department of',
    'Department',
    'Fach',
]

UNIVERSITY = [
    'Hochschule',
    'Universität',
]

COURSES = [
    'Studiengang:',
    'Studiengang',
]

# TODO: Load from dictionary
UNIVERSITIES = [
    'Duale Hochschule Baden-Würtemberg',
    'Freie Universität Berlin',
    'Hochschule für Technik und Wirtschaft Berlin',
    'Humboldt-Universität zu Berlin',
    'Katholische Hochschule Nordrhein-Westfalen',
    'Ludwig-Maximilians-Universität München'
    'Suchtakademie Berlin-Brandenburg',
    'Technische Universita\xA8t Berlin',  # TODO: INVESTIGATE HERE
    'Technische Universität Berlin',
    'Technische Universität Darmstadt',
    'Universität Bielefeld',
    'Universität Hamburg',
    'Universität Münster',
]


def find_institution(raw) -> str:
    """Check that `institution` is in UNIVERSITIES dictionary.

    Args:
        raw(str): page text content
    Returns:
        None if `institution` is in dictionary else collected

    TODO: Use difflib to improve collecting approach
    """
    raw = replace_special_chars(raw)
    splitted = raw.split(',')
    splitted = utila.flatten([item.split(utila.NEWLINE) for item in splitted])
    # TODO require better lookup technology with hashing
    collected = [
        item for item in UNIVERSITIES
        if any(test for test in splitted if item in test)
    ]
    if not collected:
        return None, raw
    assert len(collected) == 1, 'More than one institution is collected'
    collected = collected[0]

    rest = raw.replace(collected, '')
    return collected, rest


def replace_special_chars(raw: str) -> str:
    raw = raw.replace('¨a', 'ä')
    raw = raw.replace('¨u', 'ü')
    return raw
