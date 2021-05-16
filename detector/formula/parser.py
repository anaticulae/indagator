# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila


def parse(ptcn) -> iamraw.PageContentFormula:
    result = []
    for lineindex, line in enumerate(ptcn):
        extracted = extract_formula(line)
        if not extracted:
            continue
        for item in extracted:
            item.line = lineindex
        result.extend(extracted)
    return iamraw.PageContentFormula(page=ptcn.page, content=result)


def extract_formula(line) -> iamraw.Formulas:
    # TODO: IMPROVE THIS VERY SIMPLE FORMULA CHECKER
    chars = [ord(char) for char in line.text]
    maxchar = utila.maxs(chars)
    # TODO: REPLACE WITH SINGLE FORMULA SIGN DETECTION
    ascii_only = maxchar < 12000
    if ascii_only:
        return None
    raw = line.text.strip()
    # if '=' not in raw:
    #     return None
    result = [
        iamraw.Formula(raw=raw),
    ]
    return result
