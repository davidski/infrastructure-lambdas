#!/bin/env python

from __future__ import print_function

# import json
import logging

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def incident(msg):
    """ Parse a SNS message and relay it on to pusher.com """
    return msg


def plaintext(msg):
    """ Parse a SNS message and relay it on to pusher.com """

    return msg


def cloudwatch(msg):
    """ Parse a SNS message and relay it on to pusher.com """
    return msg


def autoscaling(msg):
    """ Parse a SNS message and relay it on to pusher.com """
    return msg


def alarm(msg):
    """ Parse a SNS message and relay it on to pusher.com """
    return msg


if __name__ == '__main__':
    results = plaintext("Sample plaintext message.")
    print(results)
