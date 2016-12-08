#!/bin/env python

from __future__ import print_function
import json
import boto3
#import botocore.exceptions
import logging
from datetime import datetime
#import dateutil.parser
#import os

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
    """ Main Lambda event handling loop"""
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    resource_id = event['resource_id']
    tags = event['tags']

    session = boto3.Session(profile_name='administrator-service')
    ec2 = session.client('ec2')
    for key in tags:
        ec2.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key': key,
                'Value': tags[key]
            }]
        )
        logger.info("Tagged resource {} with tag {}:{}".format(resource_id, key, tags[key]))

    return None


if __name__ == '__main__':
    results = lambda_handler(event={'resource_id': 'ami-c804d7a8',
                                    'tags': {'scan_status': 'pass'}},
                             context="")
    #results = lambda_handler(event={'resource_id': 'i-0a5a7ac125821543e',
    #                                'tags': {'scan_batch': 'urn:uuid:9e62ff6e-bd69-11e6-a713-0014d16bb811'}},
    #                         context="")
    print(results)
