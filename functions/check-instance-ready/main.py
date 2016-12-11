#!/bin/env python

from __future__ import print_function
import json
import boto3
# import botocore.exceptions
import logging
# import dateutil.parser
# import os
from datetime import datetime

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def lambda_handler(event, context):
    """ Check if a spot instance request is Active (fulfilled)
    Check if the instance fulfilling the request is itself active
    """
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    spot_request_id = event['spot_request_id']

    # session = boto3.Session(profile_name='administrator-service')
    client = boto3.client('ec2')
    response = client.describe_spot_instance_requests(
        DryRun=False,
        SpotInstanceRequestIds=[
            spot_request_id,
        ]
    )
    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))
    spot_request_status = response['SpotInstanceRequests'][0]['State']
    if spot_request_status != "active":
        logger.info("Status not active (%s)." % spot_request_status)
        raise ValueError("Spot request {} not yet ready (status {}".format(spot_request_id, spot_request_status))
    logger.info("Spot request active!")

    instance_id = response['SpotInstanceRequests'][0]['InstanceId']
    logger.info("Using instance_id: %s" % instance_id)

    response = client.describe_instance_status(
        InstanceIds=[instance_id]
    )
    status = response['InstanceStatuses'][0]['InstanceState']['Name']
    if status != 'running':
        raise ValueError("instance {} not yet ready (status {})".format(instance_id, status))
    return {'instanceId': instance_id, 'status': status}


if __name__ == '__main__':
    results = lambda_handler(event={'spot_request_id': 'sir-btxr8rxn'},
                             context="")
    print(results)
