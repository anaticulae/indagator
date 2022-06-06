# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import configo
import iamraw
import utila

import detector.titlepage.persons.after
import detector.titlepage.persons.notitle
import detector.titlepage.persons.person
import detector.titlepage.persons.utils

PERSON_LENGTH_MAX = configo.HV_INT_PLUS(default=70)


@utila.profile('persons')
def parse(
    items: list,
    person_length_max: int = PERSON_LENGTH_MAX,
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
            with utila.profile(line):
                parsed = parse_strategies(line)
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
            rest.append(line.replace(parsed.raw, '*' * len(parsed.raw)))
            persons.append(parsed)
    # remove double parsed authors
    persons = utila.make_unique(persons)  # TODO: REMOVE LATER
    return persons, rest


def parse_strategies(raw: str) -> iamraw.Person:
    """Parse `Person` out of name line

    Args:
        raw(str): raw parsing text
    Returns:
        Person if parsing was successful, else None
    """
    strategies = [
        detector.titlepage.persons.person,
        detector.titlepage.persons.after,
        detector.titlepage.persons.notitle,
    ]
    for strategy in strategies:
        parsed = strategy.parse(raw)
        if not parsed:
            continue
        return parsed
    return None


def lookbehind(rest):
    complete = '\n'.join(rest)
    parsed = parse_strategies(complete)
    if not parsed:
        return None
    complete = complete.replace(parsed.raw, '*' * len(parsed.raw))
    rest = [item for item in complete.splitlines() if item.strip()]
    return parsed, rest
