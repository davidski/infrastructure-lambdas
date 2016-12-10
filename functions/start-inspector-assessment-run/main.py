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


rules_arns = {"arn:aws:inspector:us-west-2:758058086616:rulespackage/0-9hgA516p": "CVE",
              "arn:aws:inspector:us-west-2:758058086616:rulespackage/0-H5hpSawc": "CIS Benchmarks",
              "arn:aws:inspector:us-west-2:758058086616:rulespackage/0-JJOtZiqQ": "AWS Security Best Practices"
              }

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def lambda_handler(event, context):
    """ Main Lambda event handling loop"""
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    scan_uuid = event['tags']['scan_batch']

    # session = boto3.Session(profile_name='administrator-service')
    client = boto3.client('inspector')

    # first, create resource group
    response = client.create_resource_group(
        resourceGroupTags = [
            {
                'key': 'scan_batch',
                'value': scan_uuid
            }
        ]
    )
    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))
    resource_group_arn = response['resourceGroupArn']

    # then, create the target ARN
    response = client.create_assessment_target(
        assessmentTargetName=scan_uuid,
        resourceGroupArn=resource_group_arn
    )
    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))
    assessment_target_arn = response['assessmentTargetArn']

    response = client.create_assessment_template(
        assessmentTargetArn=assessment_target_arn,
        assessmentTemplateName='Image Validation',
        durationInSeconds=15*60,
        rulesPackageArns=list(rules_arns)
    )
    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))
    assessment_run_template_arn = response['assessmentTemplateArn']

    response = client.start_assessment_run(
        assessmentTemplateArn=assessment_run_template_arn,
        assessmentRunName='Image Validation'
    )
    logger.info('Received response: ' + json.dumps(response, default=json_serial, indent=2))
    assessment_run_arn = response['assessmentRunArn']

    # clean up our target and resource group
    client.delete_assessment_target(assessmentTargetArn=assessment_target_arn)
    #client.delete_assessment_target(assessmentTargetArn=assessment_target_arn)

    return assessment_run_arn


if __name__ == '__main__':
    results = lambda_handler(event={'tags': {'scan_batch': 'urn:uuid:9e62ff6e-bd69-11e6-a713-0014d16bb811'}},
                             context="")
    print(results)
