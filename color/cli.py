# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import color

# TODO: MOVE TO SEPARATE PROJECT

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'statistics',
        inputs=[
            utilo.Pattern('*', 'pdf'),
        ],
        output=('statistics',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=color.ROOT,
        featurepackage='color.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=color.PROCESS,
            pages=True,
            singleinput=True,
            version=color.__version__,
        ),
    )
