# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utila

import color.pagecolor


def work(path: str, pages: tuple = None) -> str:
    result = determine_statistics(path, pages=pages)
    dumped = dump_statistics(result)
    return dumped


def determine_statistics(path: str, pages: tuple = None) -> list:
    result = []
    colors = color.pagecolor.colors(path, pages=pages)
    for page in colors:
        current = color.pagecolor.histogram(page)
        result.append(current)
    return result


def dump_statistics(colors: list) -> str:
    result = []
    for page, content in enumerate(colors):
        content = [
            f'{color.pagecolor.rgb2int(*item[0])} {item[1]}' for item in content
        ]
        raw = dict(
            page=page,
            content=content,
        )
        result.append(raw)
    dumped = utila.yaml_dump(result)
    return dumped


def load_statistics(content: str) -> iamraw.PageContents:
    loaded = utila.yaml_load(
        content,
        fname='color__statistics_statistics',
    )
    result = []
    for page in loaded:
        data = [
            utila.parse_tuple(item, length=2, typ=int)
            for item in page['content']
        ]
        data = [(color.pagecolor.int2rgb(item[0]), item[1]) for item in data]
        result.append(iamraw.PageContent(
            page=int(page['page']),
            content=data,
        ))
    return result
