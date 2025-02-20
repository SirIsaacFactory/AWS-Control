# -*- coding: utf-8 -*-
from logging import (
    getLogger,
    StreamHandler,
    Formatter,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)


################################################################################
# VARIABLES
################################################################################
_LOGLEVEL_ = INFO


################################################################################
# Logger
################################################################################
logger = getLogger(__name__)
if len(logger.handlers) == 0:
    logger.setLevel(_LOGLEVEL_)
    logger.propagate = False
    handler = StreamHandler()
    formatter = Formatter("%(asctime)s, %(funcName)s, %(filename)s, %(lineno)s, [%(levelname)s], %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


