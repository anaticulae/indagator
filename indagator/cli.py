# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import indagator

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'index',
        inputs=[
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('detected',),
    ),
    utila.create_step(
        'titlepage',
        inputs=[
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.Pattern(name='rawmaker__images_images/*', ext='yaml'),
        ],
        output=('detected',),
    ),
    utila.create_step(
        'formula',
        inputs=[
            utila.ResultFile('rawmaker', 'formula_formula'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'hefopa_result'),
        ],
        output=('formula',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=indagator.ROOT,
        featurepackage='detector.feature',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=indagator.PROCESS,
            pages=True,
            singleinput=False,  # require result folder, ignore single pdf file
            version=indagator.__version__,
        ),
    )
