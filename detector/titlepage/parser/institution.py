# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import sdata
import utila


@utila.profile('institution')
def parse(raw: str) -> iamraw.Institution:
    """\
    >>> parse('Fakultät I – Geisteswissenschaften')
    (Institution(...department='Geisteswissenschaften'...,...************')
    """
    university = find_institution(raw)
    if university:
        university, raw = university
    results = []
    for item in [DEPARTMENT, INSTITUTE, FIELD, COURSES]:
        parsed, raw = detection(raw, item)
        if parsed:  # pylint:disable=W0160
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


def detection(raw, pattern, remove: bool = True):
    lines = prepare(raw)
    result = []
    for line in lines:
        searched = pattern.search(line)
        if not searched:
            continue
        matched = searched[0]
        if remove:
            # use words after `collector` as the result
            prepared = line.split(matched)[1].strip()
            if not prepared:
                # do not store empty value in result; see Fakultät IV
                # which matches completely and give no data
                continue
            result.append(prepared)
        else:
            result.append(line.strip())
        raw = utila.ghost_replace(raw, line)
    # make results unique
    result = utila.unique(result)
    return result, raw


INSTITUTE = utila.compiles(r"""
(
    INSTITUT(E)?[ ]{0,3}
    (FÜR|FOR){0,1}
)
""")

DEPARTMENT = utila.compiles(r"""
(
    (
        FACULTY|
        FAKULT(A|Ä)T
    )
    [ ]{0,4}
    (
        OF|
        (IV|I|II|III|IIII|V|VI|VII|VIII|VIIII|IX|X)|
        \d{1,2}
    )
    [ ]{0,4}
    [-–]?           # 2 different minus signs
    [ ]{0,4}
)
""")

FIELD = utila.compiles(r"""
(
    DEPARTMENT[ ]{0,4}(OF)?|
    FACHBEREICH|
    FACHGEBIET|
    FACH
)
""")

COURSES = utila.compiles(r"""
(
    STUDIENGANG\:?|
    COURSE(S)?\:?
)
""")


def find_institution(raw) -> str:
    """Check that `institution` is in UNIVERSITIES dictionary.

    Args:
        raw(str): page text content
    Returns:
        None if `institution` is in dictionary else collected
    """
    splitted = prepare(raw)
    # improve collection
    splitted = [shrink_institution(item) for item in splitted]
    collected = [item for item in splitted if sdata.rate_institution(item)]
    if not collected:
        return None, raw
    if len(collected) > 1:
        utila.error(f'More than one institution: {collected}')
    collected = collected[0]
    rest = raw.replace(collected, '')
    return collected, rest


def shrink_institution(name: str) -> str:
    """\
    >>> shrink_institution('an der Hochschule für Technik und Wirtschaft Berlin ')
    'Hochschule für Technik und Wirtschaft Berlin'
    """
    name = name.strip()
    name = re.sub(r'(^|[ ])an[ ]der[ ]', '', name)
    return name


def prepare(text: str) -> list:
    text = replace_special_chars(text)
    splitted = text.split(',')
    splitted = utila.flat([item.split(utila.NEWLINE) for item in splitted])
    splitted = [item for item in splitted if item]  # remove empty items
    return splitted


def replace_special_chars(raw: str) -> str:
    """\
    >>> replace_special_chars('¨Ullo')
    'Üllo'
    """
    raw = raw.replace('¨A', 'Ä')
    raw = raw.replace('¨O', 'Ö')
    raw = raw.replace('¨U', 'Ü')
    raw = raw.replace('¨a', 'ä')
    raw = raw.replace('¨o', 'ö')
    raw = raw.replace('¨u', 'ü')
    return raw
