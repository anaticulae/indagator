# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import ghost
import PIL.Image
import utila

import color


def colors(source: str, pages: tuple = None) -> 'yields':
    tmpdir = utila.tmpdir(root=color.ROOT)
    ghost.pdfwrite(
        source=source,
        pages=pages,
        root=tmpdir,
        formats='png16m',
        dpi=144,
    )
    files = utila.file_list(
        tmpdir,
        absolute=True,
        include='png',
    )
    files.sort(key=lambda x: str(utila.file_name(x)).zfill(4))
    for path in files:
        yield determine_color(path)


def determine_color(path: str) -> list:
    with PIL.Image.open(path, formats=('png',)) as loaded:
        data = loaded.getcolors(1024 * 10)
    return data


def histogram(data: list, count_min: int = 50) -> list:
    result = [(item[1], item[0]) for item in data if item[0] >= count_min]
    result.sort(
        key=lambda x: x[1],
        reverse=True,
    )
    return result


def rgb2int(red, green, blue) -> int:
    """\
    >>> rgb2int(255, 255, 255)
    16777215
    >>> int2rgb(rgb2int(244, 25, 139))
    (244, 25, 139)
    """
    return red << 16 | green << 8 | blue


def int2rgb(value) -> tuple:
    """\
    >>> int2rgb(16777215)
    (255, 255, 255)
    """
    return (
        255 & value >> 16,
        255 & value >> 8,
        255 & value,
    )
