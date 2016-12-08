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


rules_arns = {"arn:aws:inspector:us-west-2:758058086616:rulespackage/0-9hgA516p": "CVE",
              "arn:aws:inspector:us-west-2:758058086616:rulespackage/0-H5hpSawc": "CIS Benchmarks",
              "arn:aws:inspector:us-west-2:758058086616:rulespackage/0-JJOtZiqQ": "AWS Security Best Practices"
              }

def lambda_handler(event, context):
    """ Main Lambda event handling loop"""
    logger.info('Received event: ' + json.dumps(event, indent=2))

    instance_id = event['instance_id']

    session = boto3.Session(profile_name='administrator-service')
    client = session.client('inspector')
    response = client.create_assessment_template(
        assessmentTargetArn='string',
        assessmentTemplateName='Image Validation',
        durationInSeconds=15*60,
        rulesPackageArns=[
            rules_arns.keys()
        ]
    )
    assessment_run_template_arn = response['AssessmentTemplate']

    response = client.start_assessment_run(
        assessmentTemplateArn=assessment_run_template_arn,
        assessmentRunName='Image Validation'
    )

    assessment_run_arn = response['assessmentRunArn']

    # logger.info('Received response: ' + json.dumps(response, indent=2))

    return assessment_run_arn


if __name__ == '__main__':
    results = lambda_handler(event={'spot_request_id': 'sir-08b93456'},
                             context="")
    print(results)
