# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import utila
import utilatest

import detector
import detector.cli

#pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=detector.cli.main,
    process=detector.PROCESS,
    success=True,
)

fail = functools.partial(
    utilatest.run_command,
    main=detector.cli.main,
    process=detector.PROCESS,
    success=False,
)


def write_capsys(capsys, path: str = None):
    """Save logged capsys to filespace"""
    # TODO: REPLACE WITH UTILA
    stdout, stderr = capsys.readouterr()
    change = utila.chdir if path else utila.nothing
    with change(path):
        utila.file_create('logging.txt', stdout)
        utila.file_create('error.txt', stderr)
