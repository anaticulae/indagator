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


EXAMINER = '|'.join([
    # it's important to limit parsing length to avoid very long running parsing
    r'(\d\.\s?)?Betreuer(in)?[ ]{0,3}(extern)?',
    r'Erstgutachter(in)?',
    r'Betreuung',
    r'Gutachter(in)?',
    r'Vorsitzende(r)?',
    r'Hochschullehrer(in)?',
    r'Zweitgutachter(in)?',
    # [\s|:] to avoid confusing 'Prof. Dr. Theo Wil'
    r'(\w+\s?){1,4}?[\s|:]',
    r'Primary Supervisor',
    r'Secondary Supervisor',
    r'Referent(in)?',
    r'^',
])
PERSON_TITLE = create_person_title_pattern()
PERSON_NAME = r'(?P<fname>([A-Z]\.[ ]?|\w+(-|\ )?){1,5})[ ](?P<name>[\w|-]+)'
# pattern can be spread over more than one line
PATTERN = rf"""
    (?P<examiner>({EXAMINER})[:]?\s?)?
    ([ ]{0,4}(Herr|Frau)[ ]{0,4})?
    ({PERSON_TITLE}[ ]*)+\s?
    {PERSON_NAME}
"""
