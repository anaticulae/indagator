# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
r"""\
>>> parse('vorgelegt von\nM.Sc.\nJakob Vinzenz Kirchner')
Person(name='Kirchner'...MASTER:...raw='vorgelegt von\nM.Sc.\nJakob Vinzenz Kirchner')
"""

import iamraw
import utila

import detector.titlepage.persons.utils


def parse(raw: str) -> iamraw.Person:
    """\
    >>> parse('Gutachter: Prof. em. Dr.-Ing. Dr.-Ing. E.h. Herbert Reichl, TU Berlin')
    Person(name='Reichl',...'Gutachter: Prof. em. Dr.-Ing. Dr.-Ing. E.h. Herbert Reichl')
    >>> parse('Gutachter: Prof. Dr.-Ing. Dr. sc. techn. Klaus-Dieter Lang, TU Berlin')
    Person(name='Lang',...'Gutachter: Prof. Dr.-Ing. Dr. sc. techn. Klaus-Dieter Lang')
    >>> parse('BSC. Helmut Konrad Fahrendholz')
    Person(name='Fahrendholz'...'BSC. Helmut Konrad Fahrendholz')
    """
    parsed = PATTERN.search(raw)
    if not parsed:
        return None
    title = detector.titlepage.persons.utils.extract_titles(
        utila.extract_match(parsed))
    if not title:
        return None
    title = iamraw.AcademicTitle.merges(title)
    name, firstname = parsed['name'], parsed['fname']
    raw = utila.extract_match(parsed)
    person = iamraw.Person(title=title, name=name, firstname=firstname, raw=raw)
    return person


EXAMINERS = utila.splitlines(r"""
(\d\.\s?)?Betreuer(in)?[ ]{0,3}(extern)?
Betreuung
Erstgutachter(in)?
Erstprüfer(in)?
Gutachter(in)?
Hochschullehrer(in)?
Primary[ ]Supervisor
Referent(in)?
Secondary Supervisor
Vorsitzende(r)?
Zweitgutachter(in)?
Zweitprüfer(in)?
""")

MAGICS = utila.splitlines(r"""
(\w{2,150}\s?){1,4}?[\s|:]
^
""")

AUTHORS = utila.splitlines(r"""
Autor(in)?
Name\,[ ]Vorname
Referent(in)?
Verfasser(in)?
angefertigt[ ]von
eingereicht[ ]von
by
verfasst[ ]{1,3}von[ ]{1,3}[/][ ]{1,3}submitted[ ]{1,3}by
verfasst[ ]{1,3}von[ ]
vorgelegt[ ]von[ ]Diplom\-Ingenieur
vorgelegt[ ]von
submitted[ ]by
von
""")

INTRO = '|'.join(EXAMINERS | AUTHORS | MAGICS)
# pattern can be spread over more than one line
PATTERN = utila.compiles(rf"""
    (?P<examiner>({INTRO})[:]?\s?)?
    ([ ]{0,4}(Herr|Frau)[ ]{0,4})?
""" + detector.titlepage.persons.utils.ACADEMIC_TITLES.pattern + r"""+\s?
    (?P<fname>([A-Z]\.[ ]?|\w{3,}(-|\ )?){1,5})[ ](?P<name>[\w|\-]{3,})
""")
