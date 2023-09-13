#!/usr/bin/env python3

import argparse
from src.ssm import AdapterSSM

parser = argparse.ArgumentParser(description='Read SSM Parameter')
parser.add_argument('--project', help='The project scope', required=True)
parser.add_argument('action', help='Action to perform', choices=['enable'])
# profile from args
parser.add_argument('--profile', help='AWS profile')

args = parser.parse_args()

# TODO: make not dependable on profile, should also work with env vars
ssm = AdapterSSM(project=args.project, boto={ 'profile_name': args.profile })

if args.action == 'enable':
  ssm.enableProject()  

