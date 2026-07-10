# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import PIL.Image
import ughost
import utilo

import color

PDF_DPI_MAX = configos.HV_INT_PLUS(default=144)

COLORS_COUNT_MAX = configos.HV_INT_PLUS(default=1024 * 100)

HISTOGRAM_COUNT = configos.HV_INT_PLUS(default=50)


def colors(source: str, pages: tuple = None) -> 'yields':
    tmpdir = utilo.tmpdir(root=color.ROOT)
    ughost.pdfwrite(
        source=source,
        pages=pages,
        root=tmpdir,
        formats='png16m',
        dpi=PDF_DPI_MAX,
    )
    files = utilo.file_list(
        tmpdir,
        absolute=True,
        include='png',
    )
    files.sort(key=lambda x: str(utilo.file_name(x)).zfill(4))
    for path in files:
        yield determine_color(path)


def determine_color(path: str) -> list:
    with PIL.Image.open(path, formats=('png',)) as loaded:
        data = loaded.getcolors(COLORS_COUNT_MAX)
    return data


def histogram(
    data: list,
    count_min: int = HISTOGRAM_COUNT,
) -> list:
    if not data:
        return []
    result = [(item[1], item[0]) for item in data if item[0] >= count_min]
    result.sort(
        key=lambda x: x[1],
        reverse=True,
    )
    return result
