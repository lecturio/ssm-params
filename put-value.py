#!/usr/bin/env python3

import argparse
import os
import sys
from lib.ssm import AdapterSSM
import lib.worker as worker

parser = argparse.ArgumentParser(description='Read SSM Parameter')
parser.add_argument('--name', help='SSM Param Name', required=True)
parser.add_argument('--value', help='SSM Param Value', required=True)
# profile from args
parser.add_argument('--profile', help='AWS profile')

args = parser.parse_args()

# TODO: make not dependable on profile, should also work with env vars
ssm = AdapterSSM(profile_name=args.profile)

ssm.put_parameter(args.name, args.value)
