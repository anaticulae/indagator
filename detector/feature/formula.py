# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw
import utila


def work(
        formula: str,
        text: str,
        textpositions: str,
        sizeandborder: str,
        headerfooter: str,
        pages: tuple,
) -> str:
    loaded = serializeraw.load_rawformulas(formula, pages=pages)
    # TODO: ADD SPECIAL ANALYSIS HERE

    ptcns = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborder,
        headerfooter,
        pages=pages,
    )
    result = []
    for page in loaded:
        ptcn = utila.select_page(ptcns, page.page, default=[])
        extracted = extract_page(page.page, page.content, ptcn)
        if not extracted:
            continue
        result.append(extracted)
    dumped = serializeraw.dump_formulas(result)
    return dumped


def extract_page(page, content, navigator) -> iamraw.PageContentFormula:
    collected = []

    for formula in content:
        collected.append(extract_formula(formula, navigator))

    if not collected:
        return None
    return iamraw.PageContentFormula(page=page, content=collected)


def extract_formula(formula, navigator) -> iamraw.Formula:
    # TODO: MOVE TO FORMULARAW
    raw = ''.join([item.value.strip() for item in formula])
    result = iamraw.Formula(raw=raw)
    formula_bounding = formula.bounding
    lines = []
    for line, item in enumerate(navigator):
        if utila.rectangle_inside(item.bounding, formula_bounding):
            lines.append(line)
        elif utila.rectangle_inside(formula_bounding, item.bounding):
            lines.append(line)
    lines = sorted(lines)
    # TODO: ADD NOT MATCHED HINT
    if lines:
        result.line, result.lineend = lines[0], lines[-1]
    return result
