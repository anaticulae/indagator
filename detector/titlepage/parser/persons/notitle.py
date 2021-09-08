# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import iamraw
import utila

import detector.titlepage.parser.persons.utils


def parse(raw: str) -> iamraw.Person:
    """Parse `Person`s without any academic title.

    In general, this is the author of the document.

    Hint:
        Examiner must have an academic title, but in some thesis this is not
        so. Therefore we have to mark it later as an error.
    """
    raw = raw.strip()
    matches = re.finditer(PERSON_WITHOUT_TITLE_PATTERN, raw)
    if not matches:
        return None
    for matched in matches:
        # TODO: SUPPORT SINGLE NAME?
        # TODO: LINT TO VERIFY PRE AND SUR NAME
        # TODO: REMOVE , after improving regex
        # TODO: PARSE AND SELECT BEST?
        names = matched['names'].replace(',', '')
        try:
            firstname, name = names.rsplit(' ', maxsplit=1)
        except ValueError:
            utila.debug(f'could not split: {matched["names"]}; {matched}')
            continue
        firstname, name = firstname.strip(), name.strip()
        title = detector.titlepage.parser.persons.utils.author_or_examiner(raw)
        result = iamraw.Person(
            title=title,
            name=name,
            firstname=firstname,
            raw=utila.extract_match(matched),
        )
        return result
    return None


def create_with_title_pattern():
    # TODO: Keep attention to the list below. Refactor later
    preamble = [
        r'Erstprüfer(in)?',  # TODO: Remove this later
        r'Autor(in)?',
        r'Verfasser(in)?',
        r'Zweitprüfer(in)?',
        r'Primary Supervisor',
        r'Secondary Supervisor',
        r'vorgelegt von Diplom-Ingenieur',
        r'vorgelegt von',
        r'angefertigt von',
        r'by',
        r'Name, Vorname',
        r'Referent(in)?',
        r'von',  # TODO: exclude von in `title`
    ]
    preamble = [fr'(?P<t{index}>{item})' for index, item in enumerate(preamble)]
    preamble = '(' + '|'.join(preamble) + ')'  # pylint:disable=R0204
    between = r'[:]?[\s ]{0,8}'
    name = r'(?P<names>(\w{3,}(\,|\.)?[ ]{0,5}){1,5})\b'
    pattern = '^' + preamble + between + name + '$'
    pattern = re.compile(pattern, re.I | re.M)
    return pattern


PERSON_WITHOUT_TITLE_PATTERN = create_with_title_pattern()
