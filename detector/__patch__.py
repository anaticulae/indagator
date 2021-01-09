# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import geostrat.utils
import utila


def connect_text(items) -> str:
    """\
    >>> connect_text([''])
    ''
    """
    # TODO: REPLACE WITH MORE GENERAL APPRAOCH FROM A NICER PACKAGE
    with contextlib.suppress(AttributeError, TypeError):
        items = [item.text for item in items]
    # replace space with newline
    items = [item.replace(utila.NEWLINE, ' ') for item in items]
    # replace trennung
    items = [
        item[0:-1] if item and isminus(item[-1]) else item for item in items
    ]
    raw = ''.join(items)
    raw = raw.replace(utila.NEWLINE, ' ').strip()
    return raw


def isminus(item):
    """\
    >>> isminus('-')
    True
    """
    return item in ('-', chr(173))


geostrat.connect_text = connect_text


def parse_tuple(raw: str, length: int = 4, typ=float) -> tuple:
    """Convert `raw` to tuple of `typ`.

    >>> parse_tuple('True false True False true', length=5, typ=bool)
    (True, False, True, False, True)
    >>> parse_tuple('9.0', length=1, typ=int)
    (9,)
    """
    if typ is int:
        typ = utila.str2int
    if typ is bool:
        typ = utila.str2bool
    items = (typ(item) for item in raw.split())
    if typ is float:
        items = utila.math.roundme(*items, convert=False)
    items = tuple(items)
    assert len(items) == length, f'could not parse {raw}'
    return items


utila.parse_tuple = parse_tuple
