# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import color

# TODO: MOVE TO SEPARATE PROJECT

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'statistics',
        inputs=[
            utila.Pattern('*', 'pdf'),
        ],
        output=('statistics',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=color.ROOT,
        featurepackage='color.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=color.PROCESS,
            pages=True,
            singleinput=True,
            version=color.__version__,
        ),
    )
