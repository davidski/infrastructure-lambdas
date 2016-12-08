#!/bin/env python

from __future__ import print_function
import json
import boto3
import botocore.exceptions
import logging
import dateutil.parser
import os

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def lambda_handler(event, context):
    """ Check if a spot instance request is Active (fulfilled)
    Check if the instance fulfilling the request is itself active
    """
    logger.info('Received event: ' + json.dumps(event, indent=2))

    image_id = event['spot_request_id']

    session = boto3.Session(profile_name='administrator-service')
    client = session.client('ec2')
    response = client.describe_spot_instance_requests(
        DryRun=False,
        SpotInstanceRequestIds=[
            spot_request_id,
        ]
    )
    spot_request_status = response['SpotInstanceRequests'][0]['State']
    if spot_request_status != "active": return
    instance_id = response['SpotInstanceRequests'][0]['InstanceId']

    logger.info('Received response: ' + json.dumps(response, indent=2))

    response = client.describe_instance_status(
        InstanceIds=instance_id
    )
    status = response['InstanceStatuses'][0]['InstanceState']['Name']

    return {'InstanceId': instance_id, 'Status': status}


if __name__ == '__main__':
    results = lambda_handler(event={'spot_request_id': 'sir-08b93456'},
                             context="")
    print(results)
