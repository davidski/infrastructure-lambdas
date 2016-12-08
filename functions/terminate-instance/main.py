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
    """ Main Lambda event handling loop"""
    logger.info('Received event: ' + json.dumps(event, indent=2))

    instance_id = event['instance_id']

    session = boto3.Session(profile_name='administrator-service')
    client = session.client('ec2')
    response = client.terminate_instances(
        DryRun=False,
        InstanceIds=[
            instance_id,
        ]
    )

    #logger.info('Received response: ' + json.dumps(response, indent=2))

    return response


if __name__ == '__main__':
    results = lambda_handler(event={'spot_request_id': 'sir-08b93456'},
                             context="")
    print(results)
