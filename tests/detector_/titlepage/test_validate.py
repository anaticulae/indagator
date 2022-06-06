# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import pytest
import serializeraw
import utila
import utilatest

import detector.path
import tests.conftest
import tests.detector_

ARCHIVE = utila.join(
    detector.ROOT,
    'tests/detector_/titlepage/expected',
    exist=True,
)
RESOURCES = [
    item[0] if isinstance(item, tuple) else item
    for item in tests.conftest.RESOURCES
]
RESOURCES = [pytest.param(item, id=utila.file_name(item)) for item in RESOURCES]


@utilatest.longrun
@pytest.mark.parametrize('source', RESOURCES)
def test_validate_titlepage(
    source,
    testdir,
    monkeypatch,
):
    TitleCompare(
        source,
        testdir,
        monkeypatch,
    ).evaluate()


class TitleCompare(utilatest.BaseLiner):

    def __init__(self, source, testdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.detector_.run,
                monkeypatch=monkeypatch,
            ),
            step='titlepage',
            pages=':',
            source=source,
            workdir=testdir.tmpdir,
            archive=ARCHIVE,
            loader=serializeraw.load_titlepage,
        )

    def load(self) -> str:
        path = detector.path.titlepage_detected(self.workdir)
        loaded = self.loader(path)
        return loaded

    def raw(self, value) -> str:
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
        result = utila.dict_dump(data)
        # remove trailing white spaces
        result: str = '\n'.join(item.rstrip() for item in result.splitlines())
        return result
