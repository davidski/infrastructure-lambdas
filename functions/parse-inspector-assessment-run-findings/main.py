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

    assessment_run_arn = event['assessment_run_arn']

    session = boto3.Session(profile_name='administrator-service')
    client = session.client('inspector')
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

    logger.info('Received response: ' + json.dumps(response, indent=2))

    if response.length >0:
        return 'Fail'
    else:
        return 'Pass'


if __name__ == '__main__':
    results = lambda_handler(event={'spot_request_id': 'sir-08b93456'},
                             context="")
    print(results)
