# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import indagator

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'index',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('detected',),
    ),
    utilo.create_step(
        'titlepage',
        inputs=[
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.Pattern(name='rawmaker__images_images/*', ext='yaml'),
        ],
        output=('detected',),
    ),
    utilo.create_step(
        'formula',
        inputs=[
            utilo.ResultFile('rawmaker', 'formula_formula'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('formula',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=indagator.ROOT,
        featurepackage='detector.feature',
        config=utilo.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=indagator.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            version=indagator.__version__,
        ),
    )
