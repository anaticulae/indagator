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
