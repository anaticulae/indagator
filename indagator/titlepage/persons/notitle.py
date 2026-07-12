# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""\
>>> parse('   vorgelegt von   Thomas Helmer  ')
Person(name='Helmer', firstname='Thomas'...STUDENT...raw='vorgelegt von   Thomas Helmer')
"""

import re

import iamraw
import utilo

import indagator.titlepage.persons.person
import indagator.titlepage.persons.utils


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
            utilo.debug(f'could not split: {matched["names"]}; {matched}')
            continue
        firstname, name = firstname.strip(), name.strip()
        title = indagator.titlepage.persons.utils.author_or_examiner(raw)
        result = iamraw.Person(
            title=title,
            name=name,
            firstname=firstname,
            raw=utilo.extract_match(matched),
        )
        return result
    return None


def create_with_title_pattern():
    positions = set(indagator.titlepage.persons.person.EXAMINERS +
                    indagator.titlepage.persons.person.AUTHORS)
    preamble = [
        fr'(?P<t{index}>{item})' for index, item in enumerate(positions)
    ]
    preamble: str = '(' + '|'.join(preamble) + ')'
    between = r'[:]?[\s ]{0,8}'
    name = r'(?P<names>(\w{3,}(\,|\.)?[ ]{0,5}){1,5})\b'
    pattern = '^' + preamble + between + name + '$'
    pattern = re.compile(pattern, re.I | re.M)
    return pattern


PERSON_WITHOUT_TITLE_PATTERN = create_with_title_pattern()
