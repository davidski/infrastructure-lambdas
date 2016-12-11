#!/bin/env python

from __future__ import print_function
import json
import boto3
#import botocore.exceptions
import logging
#import dateutil.parser
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
    """ Check if a given AWS Inspector Assessment Run is complete
    Return Pending | Completed | Failed
    """
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    assessment_run_arn = event['assessment_run_arn']

    # session = boto3.Session(profile_name='administrator-service')
    client = boto3.client('inspector')
    response = client.describe_assessment_runs(
        assessmentRunArns=[
            assessment_run_arn,
        ]
    )
    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))
    assessment_status = response['assessmentRuns'][0]['state']

    switcher = {
        'CREATED': 'Pending',
        'START_DATA_COLLECTION_PENDING': 'Pending',
        'START_DATA_COLLECTION_IN_PROGRESS': 'Pending',
        'COLLECTING_DATA': 'Pending',
        'STOP_DATA_COLLECTION_PENDING': 'Pending',
        'DATA_COLLECTED': 'Pending',
        'EVALUATING_RULES': 'Pending',
        'FAILED': 'Failed',
        'COMPLETED': 'Completed',
        'COMPLETED_WITH_ERRORS': 'Failed'
    }

    result = switcher.get(assessment_status, 'Failed')
    logger.info("Status is {} ({})".format(result, assessment_status))

    if result != 'Completed':
        raise ValueError("Assessment is not complete. Current state ({} - {})".format(assessment_status, result))

    return result


if __name__ == '__main__':
    results = lambda_handler(event={
        'assessment_run_arn':
            'arn:aws:inspector:us-west-2:754135023419:target/0-uzVNByJq/template/0-rrk7k11d/run/0-3xKsC0qg'},
        context="")
    print(results)
