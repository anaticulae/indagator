# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================


def invalid_title(result) -> True:
    if not result:
        return False
    notitle = len([item for item in result if not item.title])
    rate = notitle / len(result)
    if rate > 0.1:
        return True
    return False
