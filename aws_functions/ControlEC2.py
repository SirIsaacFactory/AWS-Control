# -*- coding: utf-8 -*-
import traceback

import boto3

from . import __VERSION__
from . import Status
from .log import logger


################################################################################
# startEC2
################################################################################
def start(InstanceIds, DryRun=False):
    """
    Start E2 instances
    
    Parameters
    ------------------------------------
    InstanceIds : dict
        EC2 Instance Ids
    DryRun : boolean

    Returns
    ------------------------------------
    response : dict
        EC2 Instance Start Result
    """

    logger.debug("start")
    logger.debug(f"{__VERSION__ = }")
    logger.debug(f"{InstanceIds = }")
    #-------------------------------------------------------
    # Variables
    #-------------------------------------------------------
    status = Status()

    #-------------------------------------------------------
    # Start EC2
    #-------------------------------------------------------
    try:
        client = boto3.client("ec2")
        response = client.start_instances(
            InstanceIds = InstanceIds,
            DryRun = DryRun
        )
    except Exception as e:
        response = None
        logger.error(f"Exception: {e}\n{traceback.format_exc()}") 
        logger.debug("end")
        return status.fail, response
    
    #-------------------------------------------------------
    # Return Value
    #-------------------------------------------------------
    logger.debug("end")
    return status.success, response


################################################################################
# stopEC2
################################################################################
def stop(InstanceIds, DryRun=False):
    """
    Stop E2 instances
    
    Parameters
    ------------------------------------
    InstanceIds : dict
        EC2 Instance Ids
    DryRun : boolean

    Returns
    ------------------------------------
    response : dict
        EC2 Instance Stop Result
    """

    logger.debug("start")
    logger.debug(f"{__VERSION__ = }")
    logger.debug(f"{InstanceIds = }")
    #-------------------------------------------------------
    # Variables
    #-------------------------------------------------------
    status = Status()

    #-------------------------------------------------------
    # Stop EC2
    #-------------------------------------------------------
    try:
        client = boto3.client("ec2")
        response = client.stop_instances(
            InstanceIds = InstanceIds,
            DryRun = DryRun
        )
    except Exception as e:
        response = None
        logger.error(f"Exception: {e}\n{traceback.format_exc()}") 
        logger.debug("end")
        return status.fail, response
    
    #-------------------------------------------------------
    # Return Value
    #-------------------------------------------------------
    logger.debug("end")
    return status.success, response
