#!/bin/env python

from __future__ import print_function
import json
import boto3
#import botocore.exceptions
import logging
from datetime import datetime
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

    assessment_run_arn = event['assessment_run_arn']

    # session = boto3.Session(profile_name='administrator-service')
    client = boto3.client('inspector')
    response = client.list_findings(
        assessmentRunArns=[
            assessment_run_arn,
        ],
        filter={
            'severities': [
                'Medium', 'High',
            ]
        }
    )

    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))

    if len(response) > 0:
        return {'scan_result': [{'scan_status': 'fail'}], 'failed_finding_arns': response['findingArns']}
    else:
        return {'scan_result': [{'scan_status': 'pass'}]}


if __name__ == '__main__':
    results = lambda_handler(event={
        'assessment_run_arn':
            'arn:aws:inspector:us-west-2:754135023419:target/0-uzVNByJq/template/0-rrk7k11d/run/0-3xKsC0qg'},
                             context="")
    print(results)
