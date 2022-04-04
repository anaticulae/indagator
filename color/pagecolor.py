# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import ghost
import PIL.Image
import utila

import color

PDF_DPI_MAX = configo.HV_INT_PLUS(default=144)

COLORS_COUNT_MAX = configo.HV_INT_PLUS(default=1024 * 10)

HISTOGRAM_COUNT = configo.HV_INT_PLUS(default=50)


def colors(source: str, pages: tuple = None) -> 'yields':
    tmpdir = utila.tmpdir(root=color.ROOT)
    ghost.pdfwrite(
        source=source,
        pages=pages,
        root=tmpdir,
        formats='png16m',
        dpi=PDF_DPI_MAX,
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
