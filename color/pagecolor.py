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


def colors(source: str, pages: tuple = None) -> list:
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
    result = [determine_color(path) for path in files]
    return result


def determine_color(path: str) -> list:
    with PIL.Image.open(path, formats=('png',)) as loaded:
        data = list(loaded.getdata())
    return data
