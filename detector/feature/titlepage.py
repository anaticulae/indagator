# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""                         TITLE PAGE EXTRACTOR

The title page extractor extracts information like author, type of work,
university, date etc. out of the defined title page. Further `decision unit`s
gets these information and judge them if there are right or something is
missing. A further unit gives advices how to improve the `title` page.

workplan:
    title extractor -> judging unit -> adivice unit -> presentation layer
                                    | - - - - - - - -> presentation layer

Shortcuts:

    TPE - Title Page Extractor
    JU  - Judging Unit
    AU  - Advice unit
    PL  - Presentation layer

How does the `TPE` work:

Extract Strings
        Numbers
        Date

        FontSizes
        Boundings



Requirements - "Wissenschaftliches Arbeiten" - Manuel Rene Theisen:

   + Universitaets, Fakultaet, Institut, Seminar
   + Pruefungszeit, laufendes Semenster
   + Art: Thesis, Seminar, Bachelor, Master, Disteration
   + Thema
   + Namensangabe des Pruefers
   + Name, Vorname des Verfassers mit eventuellem akademischem Titel
   + Matrikelnummer
   + Studienadresse
   + Studiengang, Fachrichtung, (Semesterzahl?)
   + Termin der Abgabe/Einreichung
"""

import collections

import picture
import serializeraw
import texmex
import utila

import detector.titlepage.parser.complete
import detector.titlepage.strategy

# TODO: MOVE TO MORE GENERAL POSITION
# TODO: check 0.1, use a higher number?
RAWMAKER_CONFIGURATION = (
    '--prefix=oneline '
    '--font --text '
    '--boxes_flow=1.0 --char_margin=100.0 --line_margin=0.0001')

# Include first 5 pages into TitlePage detection
SELECTED_PAGES = (0, 1, 2, 3, 4)


def work(
    text: str,
    textpositions: str,
    *images: list,
    pages: tuple = None,
) -> str:
    # first five pages
    pages = pages if pages else SELECTED_PAGES
    navigators = serializeraw.ptn_fromfile(
        text,
        textpositions,
        pages=pages,
    )
    images = load_images(images, pages=pages)
    images = convert_images(images)

    parsed = parse_titlepages(navigators, images, pages)
    best = detector.titlepage.strategy.select_best(parsed)

    dumped = serializeraw.dump_titlepage(best)
    return dumped


def parse_titlepages(
    navigators: texmex.PTNs,
    images: dict,
    pages=None,
):
    pages = pages if pages else SELECTED_PAGES
    result = []
    for page in pages:
        navigator = utila.select_page(navigators, page=page)
        selected = utila.select_page(images, page=page) if images else None
        if navigator is None:  # pylint:disable=W0160
            # white page
            parsed = None
        else:
            parsed = detector.titlepage.parser.complete.parse(
                navigator,
                images=selected,
            )
        result.append(parsed)
    return result


def load_images(images, pages: tuple = None) -> dict:
    images = serializeraw.load_image_infos_fromfiles(
        images,
        pages=pages,
        skip_hidden=True,
        path_append=True,
    )
    if not images:
        return {}
    result = collections.defaultdict(list)
    for page in images:
        for image in page.content:
            path = image[1]
            # TODO: TRY OTHER FILE EXT?
            path = utila.rreplace(path, '.yaml', '.png')
            if utila.exists(path):
                result[page.page].append(picture.imageload(path))
                continue
    result: dict = dict(result)
    return result


def convert_images(images: dict) -> dict:
    result = {}
    for page, values in images.items():
        converted = []
        for image in values:
            detected = picture.detect(image)
            if not detected:
                continue
            converted.append(detected.text)
        if not converted:
            continue
        result[page] = converted
    return result
