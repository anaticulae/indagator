# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import re

import elements
import iamraw
import texmex
import utila

from detector.titlepage.parser import textblock_token
from detector.titlepage.parser.date import parse as parse_date
from detector.titlepage.parser.institution import parse as parse_institution
from detector.titlepage.parser.matrikel import parse as parse_matrikel
from detector.titlepage.parser.persons.strategy import parse as parse_person_all
from detector.titlepage.parser.persons.utils import order_persons
from detector.titlepage.parser.thesis import parse as parse_thesis
from detector.titlepage.parser.title import parse as parse_title


def parse(text: texmex.PageTextNavigator) -> iamraw.TitlePage:
    """Extract `TitlePage` out of tile page data

    Args:
        text(PageTextNavigator): content of potential title page
    Returns:
        extracted TitlePage
    """
    assert isinstance(text, texmex.PageTextNavigator), type(text)
    result = iamraw.TitlePage(pageraw=text.page)

    title = parse_title(text)

    text = clean_text(text)

    if isinstance(title, str):
        text.replace(title, '')
        result.title = title
    else:
        # TODO: check title error lstatus
        pass

    result.institution, text = parse_institution(text)
    parsed = textblock_token(text)

    result = run_simple(result, parsed)

    # run complex parsing
    persons, _ = parse_person_all(parsed)
    if persons:
        result.author, result.examiner = order_persons(persons)
    return result


STRATEGY = [
    ('date', parse_date),
    ('thesis', parse_thesis),
    ('matrikel', parse_matrikel),
]


def run_simple(title, parsed):
    undecided = []
    # run single/simple parsing tasks
    for (sink, action) in STRATEGY:
        with utila.profile(sink):
            for index, item in enumerate(parsed):
                collected = action(item)
                if not collected:
                    continue
                setattr(title, sink, collected)
                rest = item.replace(collected.raw, '').strip()
                if not rest:
                    parsed.remove(item)
                else:
                    # after replacement some data is left, try to use a further
                    parsed[index] = rest
                break
            else:
                undecided.append(action)
    return title


def clean_text(text: list) -> str:
    text = utila.NEWLINE.join([item.text for item in text[:]])
    # remove textual horizontal lines cause there slow down persons parsing
    text = re.sub(r'[\-\=\_]{5,}', '', text)
    return text


def valid_titlepage(titlepage: iamraw.TitlePage) -> bool:
    if titlepage is None:
        return False
    assert titlepage.title is None or titlepage.title.strip(
    ) == titlepage.title, f'invalid parsing result "{titlepage.title}"'

    if elements.istoc(titlepage.title):
        return False
    return True
