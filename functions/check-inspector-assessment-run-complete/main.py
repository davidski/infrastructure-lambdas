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
    """ Check if a given AWS Inspector Assessment Run is complete
    Return Pending | Completed | Failed
    """
    logger.info('Received event: ' + json.dumps(event, indent=2))

    assessment_run_arn = event['assessment_run_arn']

    session = boto3.Session(profile_name='administrator-service')
    client = session.client('inspector')
    response = client.describe_assessment_runs(
        assessmentRunArns=[
            assessment_run_arn,
        ]
    )
    assessment_status = response['Status']

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

    # logger.info('Received response: ' + json.dumps(response, indent=2))

    return result


if __name__ == '__main__':
    results = lambda_handler(event={'assessment_run_arn': 'arn:aws:inspect:1234'},
                             context="")
    print(results)
