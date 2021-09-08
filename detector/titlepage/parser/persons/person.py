# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
r"""\
>>> parse('vorgelegt von\nM.Sc.\nJakob Vinzenz Kirchner')
Person(name='Kirchner'...MASTER:...raw='vorgelegt von\nM.Sc.\nJakob Vinzenz Kirchner')
"""

import re

import iamraw
import utila

import detector.titlepage.parser.persons.utils


def parse(raw: str) -> iamraw.Person:
    """\
    >>> parse('Gutachter: Prof. em. Dr.-Ing. Dr.-Ing. E.h. Herbert Reichl, TU Berlin').raw
    'Gutachter: Prof. em. Dr.-Ing. Dr.-Ing. E.h. Herbert Reichl'
    >>> parse('Gutachter: Prof. Dr.-Ing. Dr. sc. techn. Klaus-Dieter Lang, TU Berlin').raw
    'Gutachter: Prof. Dr.-Ing. Dr. sc. techn. Klaus-Dieter Lang'
    """
    parsed = re.search(PATTERN, raw, re.X)
    if not parsed:
        return None
    title = detector.titlepage.parser.persons.utils.extract_title(parsed)
    if not title:
        return None
    title = iamraw.AcademicTitle.merges(title)
    name, firstname = parsed['name'], parsed['fname']
    raw = utila.extract_match(parsed)
    person = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return person


def create_person_title_pattern() -> str:
    keys = list(iamraw.AcademicTitle.keys())
    # make regex able and insert optional white space to dots 'M.Sc.' and 'M. Sc.'
    keys = [item.replace('.', r'\. {0,3}') for item in keys]
    # convert whte spaces
    keys = [item.replace(' ', '[ ]') for item in keys]
    result = (fr'(?P<t{index}>{item})[ ]?' for index, item in enumerate(keys))
    joined = '|'.join(result)
    return joined


EXAMINERS = r"""
(\d\.\s?)?Betreuer(in)?[ ]{0,3}(extern)?
Betreuung
Erstgutachter(in)?
Erstprüfer(in)?
Gutachter(in)?
Hochschullehrer(in)?
Primary Supervisor
Referent(in)?
Secondary Supervisor
Vorsitzende(r)?
Zweitgutachter(in)?
Zweitprüfer(in)?
"""

MAGICS = r"""
(\w+\s?){1,4}?[\s|:]
^
"""

AUTHORS = r"""
Autor(in)?
Name, Vorname
Referent(in)?
Verfasser(in)?
angefertigt von
by
vorgelegt von Diplom-Ingenieur
vorgelegt von
von
"""

PERSONS = EXAMINERS + AUTHORS
POSITIONS = utila.splitlines(PERSONS + MAGICS, lowers=False)
INTRO = '|'.join(POSITIONS)
PERSON_TITLE = create_person_title_pattern()
PERSON_NAME = r'(?P<fname>([A-Z]\.[ ]?|\w+(-|\ )?){1,5})[ ](?P<name>[\w|-]+)'
# pattern can be spread over more than one line
PATTERN = rf"""
    (?P<examiner>({INTRO})[:]?\s?)?
    ([ ]{0,4}(Herr|Frau)[ ]{0,4})?
    ({PERSON_TITLE}[ ]*)+\s?
    {PERSON_NAME}
"""
