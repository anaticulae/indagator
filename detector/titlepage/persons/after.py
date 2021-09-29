# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
r"""After
=====

>>> parse('Examiner: Hemut Konrad, M.A.')
Person(name='Konrad', firstname='Hemut',...MASTER...raw='Examiner: Hemut Konrad, M.A.')

DONT:
>>> parse('vorgelegt von\nM. Sc.\nJakob Vinzenz Kirchner')
"""

import re

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
    """
    raw = utila.normalize_whitespaces(raw)  # TODO: REMOVE LATER?
    parsed = re.search(PATTERN_PERSON_AFTER, raw, re.VERBOSE | re.IGNORECASE)
    if not parsed:
        return None
    title = detector.titlepage.persons.utils.extract_titles(parsed['title'])
    if not title:
        return None
    title = iamraw.AcademicTitle.merges(title)
    name, firstname = parsed['name'], parsed['fname']

    if name.lower() in NONAME or firstname.lower() in NONAME:
        # skip false positive detection
        # Master of Science (M. Sc.)
        return None
    raw = utila.extract_match(parsed)
    result = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return result


NONAME = utila.splitlines("""\
MASTER
OF
SCIENCE
VON
VORGELEGT
""")

# TODO: IMPROVE THIS
# TODO: SUPPORT PARSING DOUBLE PRE NAME
# TODO: VERIFY HERR/FRAU PATTERN
# Parses: Examiner: Hemut Konrad, M.A.
EXAMINER = detector.titlepage.persons.person.INTRO
TITLES = r'|'.join([
    r'\(?M\.[ ]?A\.?\B\)?',
    r'\(?B\.[ ]?SC\.?\B\)?',
    r'\(?DIPL\.[ ]PSYCH\.([ ]FH)?\)?',
    r'\(?M\.[ ]?Sc\.\)?',
])
ACADEMIC_TITLE = rf'({TITLES})'
PATTERN_PERSON_AFTER = rf"""
    (?P<examiner>({EXAMINER})[:]?\s?)
    ([ ]{0,4}(Herr|Frau)?[ ]{0,4})?
    (?P<fname>(\w+[ ]?){1,5}?)[ ](?P<name>[\w|-]+)
    [,]?[ ]{0,3}?(?P<title>{ACADEMIC_TITLE})
"""
