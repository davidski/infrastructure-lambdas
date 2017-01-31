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
    """ Check if an AMI is available (ready for use)
    """
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    image_id = event['image_id']

    # session = boto3.Session(profile_name='administrator-service')
    client = boto3.resource('ec2')
    image_status = client.Image(image_id).state

    if image_status != "available":
        logger.info("Status not available(%s)." % image_status)
        raise ValueError("Image ID {} not yet ready (status {}".format(image_id, image_status))
    logger.info("Image available!")

    return {'image_id': image_id, 'status': image_status}


if __name__ == '__main__':
    results = lambda_handler(event={'image_id': 'ami-66f44f06'},
                             context="")
    print(results)
