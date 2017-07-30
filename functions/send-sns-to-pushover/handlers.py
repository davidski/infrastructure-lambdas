#!/bin/env python

from __future__ import print_function

# import json
import logging

# set up logging
logger = logging.getLogger('SNS-Pushover Bridge')
logger.setLevel(logging.INFO)


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
