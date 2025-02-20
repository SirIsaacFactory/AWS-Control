# -*- coding: utf-8 -*-
import traceback

import boto3

from . import __VERSION__
from . import Status
from .log import logger


################################################################################
# variables
################################################################################
_MAX_RESULTS = 100


################################################################################
# extractEC2Info
################################################################################
def extractEC2Info(response):
    """
    Extract necessary information to Start/Stop E2 instances
    
    Parameters
    ------------------------------------
    response : dict
        EC2 search result

    Returns
    ------------------------------------
    status: int
        Return code
    EC2InfoList : dict
        EC2 information extract result
    """

    logger.debug("start")
    logger.debug(f"{__VERSION__ = }")

    #-------------------------------------------------------
    # Variables
    #-------------------------------------------------------
    status = Status()
    NA = "NA"
    getEc2Param = lambda keyword: instance[keyword] if keyword in instance else NA
    EC2InfoList = []

    #-------------------------------------------------------
    # Extract EC2 Information
    #-------------------------------------------------------
    for reservation in response["Reservations"]:
        EC2Info = {}
        for instance in reservation["Instances"]:
            # InstanceId
            InstanceId = getEc2Param("InstanceId")
            if InstanceId == NA:
                break

            # VpcId
            VpcId = getEc2Param("VpcId")
            # SubnetId
            SubnetId = getEc2Param("SubnetId")
            # PrivateIpAddress
            PrivateIpAddress = getEc2Param("PrivateIpAddress")
            # Placement
            Placement = getEc2Param("Placement")
            # PlatformDetails
            PlatformDetails = getEc2Param("PlatformDetails")
            # State
            State = getEc2Param("State")
            # StateReason
            StateReason = getEc2Param("StateReason")
            # KeyName
            KeyName = getEc2Param("KeyName")
            # MaintenanceOptions
            MaintenanceOptions = getEc2Param("MaintenanceOptions")
            # Tags
            Tags = getEc2Param("Tags")
            
            EC2Info = {
                "InstanceId": InstanceId,
                "VpcId": VpcId,
                "SubnetId": SubnetId,
                "PrivateIpAddress": PrivateIpAddress,
                "Placement": Placement,
                "PlatformDetails": PlatformDetails,
                "State": State,
                "StateReason": StateReason,
                "KeyName": KeyName,
                "MaintenanceOptions": MaintenanceOptions,
                "Tags": Tags
            }
            EC2InfoList.append(EC2Info)

    #-------------------------------------------------------
    # Return Value
    #-------------------------------------------------------
    logger.debug("end")
    return status.success, EC2InfoList


################################################################################
# getEc2Instances
################################################################################
def getEC2Instances(Filters, MaxResults = _MAX_RESULTS):
    """
    Get AWS EC2 instance information by searching by the filters given
    
    Parameters
    ------------------------------------
    Filters : dict
        EC2 searching filter
        When starting EC2 instances that have Name tag DC01 or DC2,
        Filters is as below:
        Filters = [
            {
                "Name": "tag:Name",
                "Values": [
                    "DC01",
                    "DC02"
                ]
            }
        ]
    MaxResults: int
        The number of EC2 instances the function gets

    Returns
    ------------------------------------
    status: int
        Return code
    EC2InstanceList : dict
        EC2 information
    """

    logger.debug("start")
    logger.debug(f"{__VERSION__ = }")
    logger.debug(f"Filters = {Filters}")
    logger.debug(f"MaxResults = {MaxResults}")

    #-------------------------------------------------------
    # Variables
    #-------------------------------------------------------
    status = Status()
    EC2InstanceList = None

    #-------------------------------------------------------
    # Searching EC2 Initial Loop
    #-------------------------------------------------------
    try:
        client = boto3.client("ec2")
        response = client.describe_instances(
            Filters = Filters,
            MaxResults = MaxResults
        )
        logger.debug(f"response = {response}")
    except Exception as e:
        response = None
        logger.error(f"Exception: {e}\n{traceback.format_exc()}")
        logger.debug("end")
        return status.fail, EC2InstanceList
    _, EC2Instance = extractEC2Info(response)
    EC2InstanceList = EC2Instance
    
    #-------------------------------------------------------
    # Searching EC2 Second Loop in case there are more than MaxResults
    #-------------------------------------------------------
    if response is not None:
        while "NextToken" in response:
            try:
                response = client.describe_instances(
                    Filters = Filters,
                    MaxResults = MaxResults
                )
                logger.debug(f"response = {response}")
            except Exception as e:
                logger.error(f"Exception: {e}\n{traceback.format_exc()}")
                logger.debug("end")
                return status.fail, EC2InstanceList
            _, EC2Instance = extractEC2Info(response)
            EC2InstanceList += EC2Instance

    #-------------------------------------------------------
    # Return Value
    #-------------------------------------------------------
    logger.debug("end")
    return status.success, EC2InstanceList

