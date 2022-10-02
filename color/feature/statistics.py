# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import ghost
import iamraw
import serializeraw
import utila

import color.pagecolor


def work(path: str, pages: tuple = None) -> str:
    result = []
    if ghost.HAS_GHOST:
        result = determine_statistics(path, pages=pages)
    else:
        utila.error('install ghost to run `color`')
    dumped = serializeraw.dump_color_statistics(result)
    return dumped


def determine_statistics(path: str, pages: tuple = None) -> list:
    result = []
    colors = color.pagecolor.colors(path, pages=pages)
    pagenumbers = utila.PageGenerator(pages=pages)
    for content in colors:
        pagenumber = next(pagenumbers)
        if color is None:
            utila.error(f'could not determine colors: {path} {pagenumber}, '
                        'may increase number of colors in histogram')
            continue
        current = color.pagecolor.histogram(content)
        result.append(iamraw.PageContent(page=pagenumber, content=current))
    return result
