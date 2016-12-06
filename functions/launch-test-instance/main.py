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

instance_profile = os.getenv('instance_profile', 'dummyarn')


def lambda_handler(event, context):
    """ Main Lambda event handling loop"""
    logger.info('Received event: ' + json.dumps(event, indent=2))

    image_id = event['imageId']
    user_data = ''
    security_groups = ['foo', 'bar']
    instance_type = 'c3.large'
    subnet_id = ''

    client = boto3.client('ec2')
    response = client.request_spot_instances(
        DryRun=True,
        InstanceCount=1,
        Type='one-time',
        SpotPrice='0.10',
        AvailabilityZoneGroup='string',
        LaunchSpecification={
            'ImageId': image_id,
            'SecurityGroups': security_groups,
            'UserData': user_data,
            'InstanceType': instance_type,
            'Placement': {
                'AvailabilityZone': 'us-west-2a'
            },
            'BlockDeviceMappings': [
                {
                    'DeviceName': 'sda',
                    'VirtualName': 'ephemeral0'
                }
            ],
            'IamInstanceProfile': {
                'Arn': instance_profile
            },
            'SubnetId': subnet_id
        }
    )

    return response['SpotInstancerequests'][0]['SpotInstanceRequestId']


if __name__ == '__main__':
    results = lambda_handler(event={'imageId': 'ami-123456'},
                             context="")
    print(results)
