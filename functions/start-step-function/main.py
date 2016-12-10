#!/bin/env python

from __future__ import print_function
import json
import boto3
# import botocore.exceptions
import logging
# import dateutil.parser
import os

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

sf_arn = os.getenv('stepfunction_arn', None)


def lambda_handler(event, context):
    """ Main Lambda event handling loop"""
    logger.info('Received event: ' + json.dumps(event, indent=2))

    session = boto3.Session(profile_name='administrator-service')
    sf = session.resource('stepfunctions')
    response = sf.start_execution(stateMachineArn=sf_arn, input=event)
    logger.info('Received response: ' + json.dumps(response, indent=2))

    execution_arn = response['executionArn']

    return {'execution_arn': execution_arn}


if __name__ == '__main__':
    results = lambda_handler(event={'responseElement':
                                        {'imageid': 'ami-08b93456'}
                                    }, context="")
    print(results)
