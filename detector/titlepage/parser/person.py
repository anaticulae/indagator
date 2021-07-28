# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Titlepage: Person Parser
========================

There are two types of person which must appear on the titlepage. The
author and examiner. An author can have an academic title. An Examiner
must have an academic title.

Examples:

    Author:
        Vorgelegt von Helmut Konrad Fahrendholz

    Examiner:
        Prof. Dr. Nobert Bolz
        Zweitgutachter: Dipl.-Medienberater Stephan Frühwirt
"""

import operator
import re
import typing

import iamraw
import iamraw.title
import utila


def parse(raw: str) -> iamraw.Person:
    """Parse `Person` out of name line

    Args:
        raw(str): raw parsing text
    Returns:
        Person if parsing was successful, else None
    """
    strategies = [
        parse_pattern,
        parse_person_after,
        parse_person_without_title,
    ]
    for strategy in strategies:
        parsed = strategy(raw)
        if not parsed:
            continue
        return parsed
    return None


def parse_pattern(raw: str) -> iamraw.Person:
    """\
    >>> parse_pattern('Gutachter: Prof. em. Dr.-Ing. Dr.-Ing. E.h. Herbert Reichl, TU Berlin').raw
    'Gutachter: Prof. em. Dr.-Ing. Dr.-Ing. E.h. Herbert Reichl'
    >>> parse_pattern('Gutachter: Prof. Dr.-Ing. Dr. sc. techn. Klaus-Dieter Lang, TU Berlin').raw
    'Gutachter: Prof. Dr.-Ing. Dr. sc. techn. Klaus-Dieter Lang'
    """
    parsed = re.search(PATTERN, raw, re.X)
    if not parsed:
        return None
    title = extract_title(parsed)
    if not title:
        return None
    title = merge_title(title)
    name, firstname = parsed['name'], parsed['fname']
    raw = utila.extract_match(parsed)
    person = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return person


def parse_person_after(raw: str) -> iamraw.Person:
    """\
    >>> parse_person_after('Betreuer extern :  Eduard  Wagner (M. Sc.)').title
    <AcademicTitle.MASTER: 8>
    """
    raw = utila.normalize_whitespaces(raw)  # TODO: REMOVE LATER?
    parsed = re.search(PATTERN_PERSON_AFTER, raw, re.VERBOSE | re.IGNORECASE)
    if not parsed:
        return None
    title = extract_title(parsed)
    if not title:
        return None
    title = merge_title(title)
    name, firstname = parsed['name'], parsed['fname']
    if name.lower() in ('master', 'of', 'science'):
        # skip false positive detection
        # Master of Science (M. Sc.)
        return None
    raw = utila.extract_match(parsed)
    person = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return person


def parse_person_without_title(raw: str) -> iamraw.Person:
    """Parse `Person`s without any academic title. In general, this is
    the author of the document.

    Hint:
        Examiner must have an academic title, but in some thesis this is not
        so. Therefore we have to mark it later as an error.
    """
    raw = raw.strip()
    matched = re.search(PERSON_WITHOUT_TITLE_PATTERN, raw)
    if not matched:
        return None
    try:
        # TODO: SUPPORT SINGLE NAME?
        # TODO: LINT TO VERIFY PRE AND SUR NAME
        # TODO: REMOVE , after improving regex
        names = matched['names'].replace(',', '')
        firstname, name = names.rsplit(' ', maxsplit=1)
    except ValueError:
        utila.error(f'could not split: {matched["names"]}; {matched}')
        return None
    firstname, name = firstname.strip(), name.strip()

    title = author_or_examiner(raw)
    result = iamraw.Person(
        title=title,
        name=name,
        firstname=firstname,
        raw=utila.extract_match(matched),
    )
    return result


@utila.profile('persons')
def parse_all(
        items: list,
        person_length_max: int = 70,  # TODO: HOLY VALUE
) -> list:
    """Parse title content to extract a list of Persons.

    Args:
        items(list): content of title page
        person_length_max(int): max length of potential title
    Returns:
        detected list of Persons and the rest of the page content as a list
    """
    persons = []
    rest = []
    for item in items:
        lines = item.splitlines()
        for line in lines:
            if len(line) > person_length_max:
                rest.append(line)
                continue
            parsed = parse(line)
            if not parsed:
                rest.append(line)
                # check area to parse more than one line
                # limit length of look behind to reduce computation power
                area = lookbehind(rest[-3:])
                if area is not None:
                    persons.append(area[0])
                    rest = area[1]
                    continue
                continue
            rest.append(line.replace(parsed.raw, ''))
            persons.append(parsed)
    # remove double parsed authors
    persons = utila.make_unique(persons)  # TODO: REMOVE LATER
    return persons, rest


def create_with_title_pattern():
    # TODO: Keep attention to the list below. Refactor later
    preamble = [
        r'Erstprüfer(in)?',  # TODO: Remove this later
        r'Autor(in)?',
        r'Verfasser(in)?',
        r'Zweitprüfer(in)?',
        r'Primary Supervisor',
        r'Secondary Supervisor',
        r'vorgelegt von',
        r'angefertigt von',
        r'by',
        r'Name, Vorname',
        r'Referent(in)?',
        # r'von', # TODO: exclude von in `title`
    ]
    preamble = [fr'(?P<t{index}>{item})' for index, item in enumerate(preamble)]
    preamble = '(' + '|'.join(preamble) + ')'  # pylint:disable=R0204
    between = r'[:]?[\s ]{0,8}'
    name = r'(?P<names>(\w+(\,|\.)?[ ]{0,5}){1,5})\b'
    pattern = re.compile(preamble + between + name, re.IGNORECASE)
    return pattern


PERSON_WITHOUT_TITLE_PATTERN = create_with_title_pattern()


def create_person_title_pattern() -> str:
    keys = [
        item.replace('.', r'\.').replace(' ', '[ ]')
        for item in iamraw.AcademicTitle.keys()
        if item
    ]
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

# TODO: IMPROVE THIS
# TODO: SUPPORT PARSING DOUBLE PRE NAME
# TODO: VERIFY HERR/FRAU PATTERN
# Parses: Examiner: Hemut Konrad, M.A.
ACADEMIC_TITLE = r'(M\.[ ]?A\.?\B|DIPL\.[ ]PSYCH\.([ ]FH)?|\(?M\.[ ]?Sc\.\)?)'
PATTERN_PERSON_AFTER = rf"""
    (?P<examiner>({EXAMINER})[:]?\s?)
    ([ ]{0,4}(Herr|Frau)?[ ]{0,4})?
    (?P<fname>(\w+[ ]?){1,5}?)[ ](?P<name>[\w|-]+)
    [,]?[ ]{0,3}?(?P<t3>{ACADEMIC_TITLE})
"""


def extract_title(result: re.Match) -> list:
    title = []
    for item in range(len(iamraw.AcademicTitle.keys())):
        try:
            parsed = result['t%d' % item]
            if not parsed:
                continue
            if not valid_title(parsed):
                continue
        except (KeyError, IndexError):
            # IndexError: no every group is used. For example only t3:master
            continue
        else:
            matches = list(iamraw.title.MATCHES.values())
            title.append(matches[item])
    return title


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


TITLE_INVALID = {
    'geb.',
}

AUTHOR_INTRO = utila.splitlines("""
angefertigt
autor
verfasser
vorgelegt
""")

EXAMINER_INTRO = utila.splitlines("""
betreuer
gutachter
prüfer
referent
supervisor
""")


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


def merge_title(items) -> iamraw.AcademicTitle:
    # TODO: REPLACE WITH IAMRAW CODE
    if not items:
        return None
    result = items[0]
    for item in items:
        if not item:
            continue
        result |= item
    return result


def lookbehind(rest):
    complete = '\n'.join(rest)
    parsed = parse(complete)
    if not parsed:
        return None
    complete = complete.replace(parsed.raw, '')
    rest = [item for item in complete.splitlines() if item.strip()]
    return parsed, rest


EXAMINERS = (
    iamraw.AcademicTitle.DR,
    iamraw.AcademicTitle.EXAMINIER,
    iamraw.AcademicTitle.PROF,
    iamraw.PROF_DR,
)


def order_persons(persons: list) -> typing.Tuple[iamraw.Person, iamraw.Persons]:
    """Sort persons by academical rank and return the lowester rang as author
    and the rest as examier.

    Args:
        persons(Persons): list to order
    Returns:
        author(Person), examines as a list of persons
    """
    if not persons:
        return None
    # sort persons by title and name as a tiebraker
    persons = sorted(persons, key=operator.attrgetter('title', 'name'))
    if persons[0].title in EXAMINERS:
        # author was not detected
        return None, persons
    if author_or_examiner(persons[0].raw) == iamraw.AcademicTitle.EXAMINIER:
        # author was not detected
        return None, persons
    author, examiner = persons[0], persons[1:]
    return author, examiner
