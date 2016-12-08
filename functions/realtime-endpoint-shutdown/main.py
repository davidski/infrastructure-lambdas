#!/bin/env python

from __future__ import print_function
import json
import boto3
import os
import logging

# fetch environment variables
model_id = os.environ['MLModelId']

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def lambda_handler(event, context):
    logger.info('Received event: ' + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    logger.info('From SNS: ' + message)
    client = boto3.client('machinelearning', region_name='us-east-1')
    results = client.delete_realtime_endpoint(MLModelId = model_id)
    logger.info('Endpoint deleted')
    return results

if __name__ == '__main__':
    results = lambda_handler(event={'Records': [{'Sns': {'Message': 'foo'}}]},
                   context="")
    print(results)
