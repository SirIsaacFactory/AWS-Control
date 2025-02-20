# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2025 Kazuhiro Tsuzuki
# This software is released under the MIT License see LICENSE.txt
# Overview : Compress program for AWS Lambda functions
#
#-------------------------------------------------------------------------------
# Author: Isaac Factory (sir.isaac.factory@gmail.com)
# Repository: https://github.com/SirIsaacFactory/PowerShellLibs
#
################################################################################

################################################################################
# History
#-------------------------------------------------------------------------------
# 2025/02/09: Initially created
################################################################################
__VERSION__ = "1.00"


################################################################################
# Libraries
################################################################################
import os
import path
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
# Variables
################################################################################
logger = getLogger(__name__)
if len(logger.handlers) == 0:
    logger.setLevel(_LOGLEVEL_)
    logger.propagate = False
    handler = StreamHandler()
    formatter = Formatter("%(asctime)s, %(funcName)s, %(filename)s, %(lineno)s, [%(levelname)s], %(message)s", datefmt="%Y/%m/%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main(lambda_main):




