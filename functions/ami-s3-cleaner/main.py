#!/bin/env python

from __future__ import print_function
import json
import boto3
import botocore.exceptions
import logging
import dateutil.parser

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

    client = boto3.client('ec2')
    response = client.describe_images(
        Owners=['self']
    )
    s3_client = boto3.client('s3')
    logger.debug('Response: ' + json.dumps(response))

    # build the list of image names based on tags
    image_names = set()
    for image in response['Images']:
        if 'Tags' not in image:
            logger.warn("Untagged ami: " + image['Name'])
            continue
        for tag in image['Tags']:
            if tag['Key'] == 'Name':
                image_names.add(tag['Value'])
    logger.debug('Working set of names: ' + str(image_names))

    for name in image_names:
        logger.info("Scrubbing old images for " + name)
        scrub_image(name, client, s3_client)


def scrub_image(name, ec2, s3):
    """ Purge old images for a given Name tag """
    response = ec2.describe_images(
        Owners=['self'],
        Filters=[{'Name': 'tag:Name', 'Values': [name]}]
    )
    # find the date of the newest image
    image_dates = []
    for image in response['Images']:
        logger.debug("Image creation date is " + dateutil.parser.parse(image['CreationDate']).isoformat())
        image_dates.append(dateutil.parser.parse(image['CreationDate']))
    current_image_date = max(image_dates)
    logger.info("Newest image date is " + current_image_date.isoformat())

    # purge all images older than the current one
    for image in response['Images']:
        image_date = dateutil.parser.parse(image['CreationDate'])
        if image_date == current_image_date:
            logger.info("Skipping '" + image['Name'] + "' as it's the newest")
            continue
        else:
            logger.info("Working on " + image['Name'] + " as " + image['CreationDate'] + " is not == " +
                        current_image_date.isoformat())
            try:
                ec2.deregister_image(ImageId=image['ImageId'])
                logger.info("De-registered image: " + image['ImageId'])
            except botocore.exceptions.ClientError as e:
                logger.error(e)

        # identify image objects to purge
        location = image['ImageLocation']
        if location.endswith('.manifest.xml'):
            location = location[:-13]
        logger.debug("image location: " + location)
        objects = s3.list_objects_v2(
            Bucket=location.split('/', 1)[0],
            Prefix=location.split('/', 1)[1]
        )
        delete_list = []
        if 'Contents' not in objects:
            logger.warn("Found no S3 keys for image: " + image['Name'])
            continue
        for s3_key in objects['Contents']:
            delete_list.append({"Key": s3_key['Key']})

        # delete the identified files
        response = s3.delete_objects(
            Bucket=location.split('/', 1)[0],
            Delete={
                'Objects': delete_list
            }
        )
        if 'Errors' in response:
            logger.error("Deletion Errors:" + json.dumps(response['Errors']))
        if 'Deleted' in response:
            logger.info("Deletion objects:" + json.dumps(response['Deleted']))

if __name__ == '__main__':
    lambda_handler(event={'Records': [{'Sns': {'Message': 'foo'}}]}, context="")
