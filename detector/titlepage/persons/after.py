# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
r"""After
=====

>>> parse('Examiner: Hemut Konrad, M.A.')
Person(name='Konrad', firstname='Hemut',...MASTER...raw='Examiner: Hemut Konrad, M.A.')
>>> parse('verfasst von / submitted by Martin SCHRAMMEL, BSc')
Person(name='SCHRAMMEL', firstname='Martin', title=...BSC...raw='verfasst von / submitted by Martin SCHRAMMEL, BSc')

DONT:
>>> parse('vorgelegt von\nM. Sc.\nJakob Vinzenz Kirchner')
"""

import iamraw
import iamraw.title
import utila

import detector.titlepage.persons.person
import detector.titlepage.persons.utils


def parse(raw: str) -> iamraw.Person:
    """\
    >>> parse('Betreuer extern :  Eduard  Wagner (M. Sc.)').title
    <AcademicTitle.MASTER: 8>
    >>> parse('Betreuer extern :  Eduard  Wagner (B. Sc.)').title
    <AcademicTitle.BSC: 4>
    >>> parse('verfasst von Claudia Ziegler, BA')
    Person(name='Ziegler', firstname='Claudia'...BSC..., raw='verfasst von Claudia Ziegler, BA')
    """
    raw = utila.normalize_whitespaces(raw)  # TODO: REMOVE LATER?
    parsed = PATTERN_PERSON_AFTER.search(raw)
    if not parsed:
        return None
    title = parsed['title']
    title = detector.titlepage.persons.utils.extract_titles(title)
    if not title:
        return None
    title = iamraw.AcademicTitle.merges(title)
    name, firstname = parsed['name'], parsed['fname']
    if noname(name) or noname(firstname):
        return None
        # skip false positive detection
        # Master of Science (M. Sc.)
    raw = utila.extract_match(parsed)
    result = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return result


def noname(name: str):
    name = name.lower()
    if ' ' in name:
        name = name.split()
    if ' ' not in name:
        name = [name]
    if any(item in NONAME for item in name):
        return True
    return False


NONAME = utila.splitlines("""\
MASTER
OF
SCIENCE
VON
VORGELEGT
ON
FACH
""")

# TODO: IMPROVE THIS
# TODO: SUPPORT PARSING DOUBLE PRE NAME
# TODO: VERIFY HERR/FRAU PATTERN
# Parses: Examiner: Hemut Konrad, M.A.
EXAMINER = detector.titlepage.persons.person.INTRO
TITLES = r'|'.join([
    r'BA\b',
    r'MA\b',
    r'BSC\b',
    r'MSC\b',
    r'\(?M\.[ ]?A\.?\B\)?',
    r'\(?B\.[ ]?SC\.?\B\)?',
    r'\(?DIPL\.[ ]PSYCH\.([ ]FH)?\)?',
    r'\(?M\.[ ]?Sc\.\)?',
])
ACADEMIC_TITLE = rf'({TITLES})'
PATTERN_PERSON_AFTER = utila.compiles(rf"""
    (?P<examiner>({EXAMINER})[:]?\s?)
    ([ ]{0,4}(Herr|Frau)?[ ]{0,4})?
    (?P<fname>(\w+[ ]?){1,5}?)[ ](?P<name>[\w|-]+)
    [,]?[ ]{0,3}?(?P<title>{ACADEMIC_TITLE})
""")
