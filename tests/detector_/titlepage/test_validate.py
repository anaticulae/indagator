# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import pytest
import serializeraw
import utilo
import utilotest

import indagator.path
import tests.conftest
import tests.detector_

ARCHIVE = utilo.join(
    indagator.ROOT,
    'tests/detector_/titlepage/expected',
    exist=True,
)

RESOURCES = utilotest.test_resources(tests.conftest.RESOURCES)


@utilotest.longrun
@pytest.mark.parametrize('source', RESOURCES)
def test_validate_titlepage(
    source,
    td,
    mp,
):
    TitleCompare(
        source,
        td,
        mp,
    ).evaluate()


class TitleCompare(utilotest.BaseLiner):

    def __init__(self, source, td, mp):
        super().__init__(
            program=functools.partial(
                tests.detector_.run,
                mp=mp,
            ),
            step='titlepage',
            pages=':',
            source=source,
            workdir=td.tmpdir,
            archive=ARCHIVE,
            loader=serializeraw.load_titlepage,
        )

    def load(self) -> str:
        path = indagator.path.titlepage_detected(self.workdir)
        loaded = self.loader(path)
        return loaded

    def raw(self, value) -> str:
        return rawtitle(value)


def rawtitle(value) -> str:
    if not value:
        return 'NO TITLE PAGE'
    author = ''
    if value.author:
        author = f'{value.author.title.name}    '
        author += f'{value.author.firstname}    {value.author.name}    '
        author += value.author.raw.replace('\n', ' ')
    thesis = ''
    if value.thesis:
        thesis = f'{value.thesis.typ.name}    {value.thesis.title}'
    examiner = [
        f'{item.title.name}    {item.raw}'.replace('\n', ' ')
        for item in value.examiner
    ]
    examiner: str = '\n                    '.join(examiner)
    data = dict(
        author=author,
        title=value.title,
        thesis=thesis,
        date=value.date.raw if value.date else None,
        matrikel=value.matrikel.number if value.matrikel else None,
        examiner=examiner,
    )
    result = utilo.dict_dump(data)
    # remove trailing white spaces
    result: str = '\n'.join(item.rstrip() for item in result.splitlines())
    return result
