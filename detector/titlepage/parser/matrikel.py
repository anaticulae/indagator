# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""The module is able to parse "Matrikel" numbers out of the title page of a
thesis paper.

Matrikel numbers can have different formats:

    Matrikelnummer: 519448
    Matrikel-Nr. 1024577
    vorgelegt von: 321240
    16348
    A 066 673
    ...

There are two parts, the intro, which leads to the number e.g.
`Matrikelnummer:` and the number itself like 321240. Some title pages does
not contains a matrikel-number-intro.

"""

import iamraw
import utila


def parse(raw: str) -> iamraw.Matrikel:
    """Parse matrikel number from text line

    >>> parse('(Student No. 532196)')
    Matrikel(number=532196, intro='Student No.', raw='Student No. 532196')
    >>> parse('B.Sc. Helmut Konrad Fahrendholz 321240')
    Matrikel(number=321240, intro='', raw='321240')
    >>> parse('A 066 673')
    Matrikel(number='A 066 673', intro='', raw='A 066 673')

    Args:
        raw(str): raw text of title page
    Returns:
        parsed `Matrikel` or None if nothing matched
    """
    raw = raw.strip()
    result = MATRIKEL.search(raw)
    if not result:
        return None
    intro = result['intro']
    try:
        number = int(result['number'])
    except ValueError:
        number = result['number']
    matrikel = iamraw.Matrikel(
        number=number,
        intro=intro,
        raw=result[0].strip(),
    )
    return matrikel


MATRIKEL = utila.compiles(r"""
    (?P<intro>
        (
            |
            Matrikel-Nr\.|
            Student[ ]No\.|
            Matrikelnummer|
            vorgelegt[ ]von
        )?
        [:,]?
    )
    \s{0,4}
    (?P<number>
        \d{4,10} |                # number contains from 4 to 10 digits
        A[ ]{1,3}\d{3}[ ]{1,3}\d{3}         # A 066 673
    )
""")
