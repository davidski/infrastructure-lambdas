#!/bin/env python

from __future__ import print_function
import json
import logging
from datetime import datetime
import handlers
import os
try:
    from http.client import HTTPSConnection
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    from httplib import HTTPSConnection

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

pushover_token = os.environ['pushover_token']
pushover_user = os.environ['pushover_user']


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


def pushover_handler(message):
    """ Send parsed message to Pushover """
    logger.info('Received message' + json.dumps(message))
    conn = HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urlencode({
                     "token": pushover_token,
                     "user": pushover_user,
                     "message": message['text'],
                     "sound": message['sound'],
                     "priority": message['priority'],
                     "title": message['title']
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    return response.status


def lambda_handler(event, context):
    """ Parse a SNS message and relay it on to pusher.com """
    logger.info('Received event: ' + json.dumps(event, default=json_serial, indent=2))

    msg = event['Records'][0]['Sns']

    logger.info('Got %s via %s, timestamped %s with %s characters.' % (msg['Type'], msg['TopicArn'],
                                                                       msg['Timestamp'], msg['Message'].__len__()))


    msg['text'] = msg['Message']

    if 'incident' in msg:
        opts = handlers.incident(msg)
    elif 'AlarmName' in msg:
        opts = handlers.cloudwatch(msg)
    elif 'AutoScalingGroupName' in msg:
        opts = handlers.autoscaling(msg)
    elif 'type' in msg:
        opts = handlers.alarm(msg)
    elif 'text' in msg:
        opts = handlers.plaintext(msg)
    else:
        opts = {
            'message': 'Unrecognized SNS message: `' + msg.Message + '`'
        }

    if 'name' not in opts and 'rich' not in opts:
        if 'Subject' in event:
            opts['title'] = msg['Subject']
        else:
            opts['title'] = 'AWS SNS Bridge'

    if 'sound' not in opts:
        opts['sound'] = 'pushover'

    if 'priority' not in opts:
        opts['priority'] = 0

    return pushover_handler(opts)


if __name__ == '__main__':
    lambda_handler(event=json.dumps({'Records': [
        {'Message': 'Test message body',
         'Type': 'Notification',
         'TopicArn': 'Console',
         'Subject': 'Test message',
         'Timestamp': datetime.now().isoformat()}]}),
        context="")

