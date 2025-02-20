# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2025 Kazuhiro Tsuzuki
# This software is released under the MIT License see LICENSE.txt
# Overview : AWS BOTO3 WRAPPER
#
#-------------------------------------------------------------------------------
# Author: Isaac Factory (sir.isaac.factory@gmail.com)
# Repository: https://github.com/SirIsaacFactory/PowerShellLibs
#
################################################################################

################################################################################
# History
#-------------------------------------------------------------------------------
# 2025/02/09: Inistially created
################################################################################
__VERSION__ = "1.00"


################################################################################
# Return Value
################################################################################
class Status:
    @property
    def success(self):
        return 0
    @property
    def warning(self):
        return 1
    @property
    def fail(self):
        return 2

