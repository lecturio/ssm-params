#!/usr/bin/env python3

import argparse
from src.ssm import AdapterSSM

parser = argparse.ArgumentParser(description="Read SSM Parameter")
parser.add_argument("--project", help="The project scope", required=True)
parser.add_argument("action", help="Action to perform", choices=["enable"])

args = parser.parse_args()

ssm = AdapterSSM(project=args.project)

if args.action == "enable":
    ssm.enableProject()
