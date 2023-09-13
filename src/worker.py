#!/usr/bin/env python3

import os
import src.ssm as ssm
import shutil
from tabulate import tabulate

# constant for file eding in .ssm
SSM_FILE_ENDING = '.ssm'
# constant for the prefix of the SSM parameter
SSM_PARAMETER_PREFIX = '<SSM>'
# constant for the suffix of the SSM parameter
SSM_PARAMETER_SUFFIX = '</SSM>'

INDEX_FILE = 0
INDEX_NAME = 1
INDEX_VALUE = 2

def list(project_root, ssm, input_empty=False):
  process(project_root, ssm, list=True, input_empty=input_empty)

def apply(project_root, ssm, input_empty=False):
  stop_on_empty = not input_empty
  process(project_root, ssm, apply=True, input_empty=input_empty, stop_on_empty=stop_on_empty)

def fill(project_root, ssm):
  process(project_root, ssm, input_empty=True)

def process(project_root, ssm, list=False, apply=False, input_empty=False, stop_on_empty=False):
  table = []
  headers = ['File', 'Name', 'Value']
  # find all files in the project root recursively that end in .ssm
  for root, dirs, files in os.walk(project_root):
    for file in files:
      if file.endswith(SSM_FILE_ENDING):
        ssm_file = os.path.join(root, file)
        param_prefix = '/' + os.path.relpath(ssm_file, project_root).replace('.ssm', '')
        non_ssm_file = ssm_file.replace('.ssm', '')

        if apply:
          shutil.copy(ssm_file, non_ssm_file)
        
        replacements = get_params(ssm_file, ssm, param_prefix, stop_on_empty, input_empty)
        table += replacements

        if apply:
          # read the content of non_ssm_file
          with open(non_ssm_file, 'r') as rf:
            content = rf.read()

          with open(non_ssm_file, 'w') as wf:
            for replacement in replacements:
              placeholder = SSM_PARAMETER_PREFIX + replacement[INDEX_NAME] + SSM_PARAMETER_SUFFIX
              content = content.replace(placeholder, replacement[INDEX_VALUE])
              wf.write(content)
  if list:
    print(tabulate(table, headers, tablefmt='grid'))
              
def get_params(ssm_file, ssm, param_prefix, stop_on_empty=False, input_empty=False):
  replacements = []
  # open the file
  with open(ssm_file, 'r') as f:
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
        raise Exception('Malformed SSM parameter in file: ' + ssm_file + ' on line: ' + line)
      
      # the string to be replaced
      replace = line[prefix_index + len(SSM_PARAMETER_PREFIX):suffix_index]
      # the param name
      param = param_prefix + '/' + replace

      value = ssm.get_parameter(param)

      if not value:
        if stop_on_empty:
          raise Exception('Empty SSM parameter: ' + param)
        
        # read value from input until provided
        if input_empty:
          while not value:
            value = input('Enter value for ' + param + ': ')
          # put the value into SSM
          ssm.put_parameter(param, value)
      replacements.append((param_prefix, replace, value)) 

  return replacements
