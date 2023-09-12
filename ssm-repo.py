#!/usr/bin/env python3

import argparse
import os
import sys
from lib.ssm import AdapterSSM
import lib.worker as worker

parser = argparse.ArgumentParser(description='Read SSM Parameter')
# operation from args
parser.add_argument('operation', help='Operation to perform', choices=['list', 'apply'])
# project root directory from args
parser.add_argument('--project-root', help='Project root directory', required=True)
# profile from args
parser.add_argument('--profile', help='AWS profile')

args = parser.parse_args()

# find the absolute path to the project root based on this file's location
project_root = os.path.abspath(args.project_root)
# if project root does not exist, exit
if not os.path.exists(project_root):
    print('Project root does not exist')
    sys.exit(1)

# TODO: make not dependable on profile, should also work with env vars
ssm = AdapterSSM(profile_name=args.profile)

worker.process(project_root, ssm, list=args.operation == 'list', apply=args.operation == 'apply')

