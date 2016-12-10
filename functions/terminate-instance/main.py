#!/bin/env python

from __future__ import print_function
import json
import boto3
#import botocore.exceptions
import logging
#import dateutil.parser
#import os
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
    """ Terminate an EC2 instance, identified by a passed instance id """
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    instance_id = event['InstanceId']

    # session = boto3.Session(profile_name='administrator-service')
    client = boto3.client('ec2')
    response = client.terminate_instances(
        DryRun=False,
        InstanceIds=[
            instance_id,
        ]
    )

    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))

    return response


if __name__ == '__main__':
    results = lambda_handler(event={'InstanceId': 'i-0a5a7ac125821543e'},
                             context="")
    print(results)
