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

    resource_id = event['resource_id']
    tag = event['tag']

    session = boto3.Session(profile_name='administrator-service')
    ec2 = session.resource('ec2')
    response = ec2.Tag('resource_id', tag['key'], tag['value'])

    logger.info('Received response: ' + json.dumps(response, indent=2))

    return response


if __name__ == '__main__':
    results = lambda_handler(event={'resource_id': 'ami-08b93456',
                                    'tag': {'key': 'scan_status', 'value': 'Pass'}},
                             context="")
    print(results)
