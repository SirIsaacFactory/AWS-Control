# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2025 Kazuhiro Tsuzuki
# This software is released under the MIT License see LICENSE.txt
# Overview : Start AWS EC2 Instances
#
#-------------------------------------------------------------------------------
# Author: Isaac Factory (sir.isaac.factory@gmail.com)
# Repository: https://github.com/SirIsaacFactory/EC2-StartStop
#
################################################################################

################################################################################
# History
#-------------------------------------------------------------------------------
# 2025/02/22: Initially created
################################################################################
__VERSION__ = "1.00"


################################################################################
# Libraries
################################################################################
import time
from logging import (
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL
)

from aws_functions.log import logger
from aws_functions import Status
from aws_functions import ListEC2
from aws_functions import ControlEC2


################################################################################
# Variables
################################################################################
status = Status()
NA = "NA"
DEFAULT_LOGLEVEL = INFO
LOGLEVELS = ["DEBUG", "INFO", "WARNING", "ERORR", "CRITICAL"]
STOPPED = "stopped"
RUNNING = "running"
INTERVAL = 120


################################################################################
# Main
################################################################################
def run(event, context):
    logger.debug("start")
    logger.info("----------------------------------------")
    logger.info("- START")
    logger.info("----------------------------------------")

    #-------------------------------------------------------
    # Variables
    #-------------------------------------------------------
    endLambda = lambda stat, msg: {"statusCode": stat, "body": msg}
    expectedBeforeState = STOPPED
    exptectedAfterState = RUNNING


    #-------------------------------------------------------
    # Check Arguments
    #-------------------------------------------------------
    # Loglevel
    if "loglevel" in event:
        if event["loglevel"] in LOGLEVELS:
            loglevel = event["loglevel"]
        else:
            loglevel = DEFAULT_LOGLEVEL
    else:
        loglevel = DEFAULT_LOGLEVEL
    logger.setLevel(loglevel)

    # EC2 search filter
    if "Filters" in event:
        Filters = event["Filters"]
        if type(Filters) != list:
            msg =  f"Invalid Filters: {Filters}"
            logger.error(msg)
            logger.debug("end")
            return endLambda(200, msg)
    else:
        msg =  f"Filters doesn't exist: {Filters}"
        logger.error(msg)
        logger.debug("end")
        return endLambda(200, msg)


    # Minimum expected EC2 instances
    if "minInstNum" in event:
        minInstNum = event["minInstNum"]
        if type(minInstNum) != int:
            msg =  f"Invalid minInstNum: {minInstNum}"
            logger.error(msg)
            logger.debug("end")
            return endLambda(200, msg)
    else:
        minInstNum = 1

    # Maximum expected EC2 instances
    if "maxInstNum" in event:
        maxInstNum = event["maxInstNum"]
        if type(maxInstNum) != int:
            msg = f"Invalid maxInstNum: {maxInstNum}"
            logger.error(msg)
            logger.debug("end")
            return endLambda(200, msg)
    else:
        maxInstNum = 1

    # Wait interval
    if "interval" in event:
        interval = event["interval"]
        if type(maxInstNum) != int:
            msg = f"Invalid interval: {interval}"
            logger.error(msg)
            logger.debug("end")
            return endLambda(200, msg)
    else:
        interval = INTERVAL


    #-------------------------------------------------------
    # Display Parameters
    #-------------------------------------------------------
    logger.info(f"{Filters = }")
    logger.info(f"{minInstNum = }")
    logger.info(f"{maxInstNum = }")
    logger.info(f"{interval = }")


    #-------------------------------------------------------
    # Search EC2 Instances
    #-------------------------------------------------------
    logger.info("----------------------------------------")
    logger.info("SEARCH EC2 INSTANCES")
    logger.info("----------------------------------------")
    (ret, ec2InstanceList) = ListEC2.getEC2Instances(Filters)
    if ret != status.success:
        msg = f"Failed to get EC2 instances"
        logger.error(msg)
        logger.debug("end")
        return endLambda(200, msg)
    else:
        instanceNum = len(ec2InstanceList)

    if instanceNum == 0:
        msg = "No instance found"
        logger.info(msg)
        logger.debug("end")
        return endLambda(200, msg)
    logger.debug(f"{ec2InstanceList = }")
    logger.info(f"{instanceNum} instance(s) found")


    #-------------------------------------------------------
    # Display EC2 information and make InstanceId List
    #-------------------------------------------------------
    InstanceIds = []
    i = 0
    for ec2Info in ec2InstanceList:
        i += 1
        ec2Params = ["VpcId", "SubnetId", "PrivateIpAddress", "State", "StateReason", "Tags"]
        getEc2Param = lambda keyword: ec2Info[keyword] if keyword in ec2Info else NA

        logger.info(f"EC2 INSTANCE {i:003} ----------------------------------------")
        # Name Tag Value
        Name = NA
        if "Tags" in ec2Info:
            for tags in ec2Info["Tags"]:
                if tags["Key"] == "Name":
                    Name = tags["Value"]

        logger.info(f"{Name = }")
        for ec2Param in ec2Params:
            # Other attributes
            logger.info(f"{ec2Param} = {getEc2Param(ec2Param)}")

        # if the instance state is expectedBeforeState, add the instance to InstanceIds list
        if ec2Info["State"]["Name"] == expectedBeforeState:
            InstanceIds.append(getEc2Param("InstanceId"))


    #-------------------------------------------------------
    # Check the Number of EC2 Instances
    #-------------------------------------------------------
    logger.info(f"The expected instance number(s) is {minInstNum} <= instance(s) <= {maxInstNum}")
    logger.debug(f"instanceNum({instanceNum}) < minInstNum({minInstNum}): {instanceNum < minInstNum}")
    logger.debug(f"instanceNum({instanceNum}) > maxInstNum({maxInstNum}): {instanceNum > maxInstNum}")

    if (instanceNum < minInstNum) or (instanceNum > maxInstNum):
        msg = f"The number of instance(s) is out of range"
        logger.error(msg)
        logger.debug("end")
        return endLambda(200, msg)

    if len(InstanceIds) == 0:
        msg = f"All instances are in {exptectedAfterState} state"
        logger.info(msg)
        logger.debug(msg)
        return endLambda(200, msg)


    #-------------------------------------------------------
    # Start EC2
    #-------------------------------------------------------
    logger.info("----------------------------------------")
    logger.info("START EC2 INSTANCES AND CHECK RESULT")
    logger.info("----------------------------------------")
    ret, ec2StartResult = ControlEC2.start(InstanceIds, DryRun=False)
    ret, ec2StartResult

    if ret != status.success:
        msg = f"Failed to start EC2 instances: {InstanceIds}"
        logger.error(msg)
        logger.debug("end")
        return endLambda(200, msg)

    logger.info("EC2 Instances Started")


    #-------------------------------------------------------
    # Get Result
    #-------------------------------------------------------
    logger.info(f"Check the result in {interval} seconds")
    time.sleep(interval)
    (ret, ec2InstanceList) = ListEC2.getEC2Instances(Filters)
    if ret != status.success:
        msg = f"Failed to get EC2 instances"
        logger.error(msg)
        logger.debug("end")
        return endLambda(200, msg)
    else:
        instanceNum = len(ec2InstanceList)

    if instanceNum == 0:
        msg = "No instance found"
        logger.info(msg)
        logger.debug("end")
        return endLambda(200, msg)
    logger.debug(f"{ec2InstanceList = }")


    #-------------------------------------------------------
    # Check and Display Result
    #-------------------------------------------------------
    i = 0
    successInstanceNum = 0
    for ec2Info in ec2InstanceList:
        i += 1
        ec2Params = ["VpcId", "SubnetId", "PrivateIpAddress", "State", "StateReason", "Tags"]
        getEc2Param = lambda keyword: ec2Info[keyword] if keyword in ec2Info else NA

        logger.info(f"EC2 INSTANCE {i:003} ----------------------------------------")
        # Name Tag Value
        Name = NA
        if "Tags" in ec2Info:
            for tags in ec2Info["Tags"]:
                if tags["Key"] == "Name":
                    Name = tags["Value"]

        logger.info(f"{Name = }")
        for ec2Param in ec2Params:
            # Other attributes
            logger.info(f"{ec2Param} = {getEc2Param(ec2Param)}")

        # if the instance state is expectedBeforeState, add the instance to InstanceIds list
        if ec2Info["State"]["Name"] == exptectedAfterState:
            successInstanceNum += 1

    #-------------------------------------------------------
    # Return Value
    #-------------------------------------------------------
    # Compare of the instances that changed the state
    if instanceNum == successInstanceNum:
        msg = f"Scceeded in starting EC2 instance: {InstanceIds}"
        logger.info(msg)
    else:
        msg = f"Failed to start EC2 instances: {InstanceIds}"
        logger.error(msg)
    logger.debug("end")
    return endLambda(200, msg)
