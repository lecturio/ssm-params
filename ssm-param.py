#!/usr/bin/env python3

import argparse
import os
import sys

# constant for file eding in .ssm
SSM_FILE_ENDING = '.ssm'
# constant for the prefix of the SSM parameter
SSM_PARAMETER_PREFIX = '<SSM>'
# constant for the suffix of the SSM parameter
SSM_PARAMETER_SUFFIX = '</SSM>'

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

# find all files in the project root recursively that end in .ssm
ssm_files = []
for root, dirs, files in os.walk(project_root):
    for file in files:
        if file.endswith(SSM_FILE_ENDING):
            print('Found SSM file: ' + file)
            afile = os.path.join(root, file)
            # add the file to the list
            ssm_files.append(afile)

            # open the file
            with open(afile, 'r') as f:
                # read file line by line
                lines = f.readlines()
                # for each line set the content between the SSM_PARAMETER_PREFIX and SSM_PARAMETER_SUFFIX as variable
                for line in lines:
                    # find the index of the prefix
                    prefix_index = line.find(SSM_PARAMETER_PREFIX)
                    if prefix_index == -1:
                        continue
                    # find the index of the suffix
                    suffix_index = line.find(SSM_PARAMETER_SUFFIX)
                    if suffix_index == -1:
                        # throw exception if suffix is not found
                        raise Exception('Malformed SSM parameter in file: ' + afile + ' on line: ' + line)
                    
                    # relative file position in the project root
                    relative_path = os.path.relpath(afile, project_root).replace('.ssm', '')

                    # the param name
                    param = relative_path + '/' + line[prefix_index + len(SSM_PARAMETER_PREFIX):suffix_index]
                    print(param)
                        

print(project_root)
print(ssm_files)