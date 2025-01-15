#!/usr/bin/env python3

import argparse
import os
import sys
from src.ssm import AdapterSSM
import src.worker as worker

parser = argparse.ArgumentParser(description="Read SSM Parameter")
parser.add_argument("--project", help="The project scope", required=True)
# operation from args
parser.add_argument(
    "operation", help="Operation to perform", choices=["list", "apply", "fill", "auto-fill"]
)
# project root directory from args
parser.add_argument("--project-root", help="Project root directory", required=True)
# input empty from args
parser.add_argument("--input-empty", help="Input empty values")

args = parser.parse_args()

# find the absolute path to the project root based on this file's location
project_root = os.path.abspath(args.project_root)
# if project root does not exist, exit
if not os.path.exists(project_root):
    print("ERROR: Project root does not exist! Exiting...")
    sys.exit(1)

# TODO: make not dependable on profile, should also work with env vars
ssm = AdapterSSM(project=args.project)
if not ssm.isProjectEnabled():
    print("ERROR: Project is not enabled! Exiting...")
    exit(1)

try:
    # switch call based on operation
    match args.operation:
        case "list":
            worker.list(project_root, ssm, input_empty=args.input_empty)
        case "apply":
            worker.apply(project_root, ssm, input_empty=args.input_empty)
        case "fill":
            worker.fill(project_root, ssm)
        case "auto-fill":
            worker.auto_fill(project_root, ssm)
        case _:
            print("ERROR: Operation not supported! Exiting...")
            exit(1)
except Exception as e:
    print("ERROR: " + str(e))
    exit(1)
