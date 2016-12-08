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

instance_profile = os.getenv('instance_profile', 'arn:aws:iam::754135023419:instance-profile/aws-packer-ec2')
subnet_id = os.getenv('subnet_id', 'subnet-75bc4d12')

def lambda_handler(event, context):
    """ Given an AMI identifier, launch a spot instance version of the image """
    logger.info('Received event: ' + json.dumps(event, indent=2))

    image_id = event['imageId']
    user_data = ''
    security_groups = ['sg-2a999d53', 'sg-2a999d53']
    instance_type = 'c3.large'

    session = boto3.Session(profile_name='administrator-service')
    client = session.client('ec2')
    response = client.request_spot_instances(
        DryRun=False,
        InstanceCount=1,
        Type='one-time',
        SpotPrice='0.10',
        LaunchSpecification={
            'ImageId': image_id,
            'SecurityGroupIds': security_groups,
            'UserData': user_data,
            'InstanceType': instance_type,
            'BlockDeviceMappings': [
                {
                    'DeviceName': 'sdb',
                    'VirtualName': 'ephemeral0'
                }
            ],
            'IamInstanceProfile': {
                'Arn': instance_profile
            },
            'SubnetId': subnet_id
        }
    )

    #logger.info('Received response: ' + json.dumps(response, indent=2))

    spot_request_id=response['SpotInstanceRequests'][0]['SpotInstanceRequestId']
    # create tags on the spot fleet request to be passed to the instance
    client.create_tags(
        Resources=[spot_request_id],
        Tags=[{
            'Key': 'project',
            'Value': 'infrastructure'
        }, {
            'Key': 'scan_batch',
            'Value': '42'
        }]
    )

    return spot_request_id


if __name__ == '__main__':
    results = lambda_handler(event={'imageId': 'ami-c804d7a8'},
                             context="")
    print(results)
