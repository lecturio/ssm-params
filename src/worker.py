#!/usr/bin/env python3

import os
import src.ssm as ssm
import shutil

# constant for file eding in .ssm
SSM_FILE_ENDING = '.ssm'
# constant for the prefix of the SSM parameter
SSM_PARAMETER_PREFIX = '<SSM>'
# constant for the suffix of the SSM parameter
SSM_PARAMETER_SUFFIX = '</SSM>'

def process(project_root, ssm, list=False, apply=False):
  # find all files in the project root recursively that end in .ssm
  ssm_files = []
  for root, dirs, files in os.walk(project_root):
      for file in files:
          if file.endswith(SSM_FILE_ENDING):
              ssm_file = os.path.join(root, file)
              param_prefix = '/' + os.path.relpath(ssm_file, project_root).replace('.ssm', '') + '/'
              non_ssm_file = ssm_file.replace('.ssm', '')

              # add the file to the list
              ssm_files.append(ssm_file)
              if apply:
                shutil.copy(ssm_file, non_ssm_file)
              
              replacements = get_params(ssm_file, ssm, param_prefix, apply)
              
              if list:
                 for replacement in replacements:
                   print(param_prefix + replacement[0] + ' = ' + replacement[1])

              if apply:
                # read the content of non_ssm_file
                with open(non_ssm_file, 'r') as rf:
                  content = rf.read()

                with open(non_ssm_file, 'w') as wf:
                  for replacement in replacements:
                    content = content.replace(SSM_PARAMETER_PREFIX + replacement[0] + SSM_PARAMETER_SUFFIX, replacement[1])
                    wf.write(content)

              
def get_params(ssm_file, ssm, param_prefix, stop_on_empty=False):
  # open the file
  with open(ssm_file, 'r') as f:
    # read file line by line
    lines = f.readlines()
    replacements = []
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
        param = param_prefix + replace

        value = ssm.get_parameter(param)

        if not value and stop_on_empty:
          raise Exception('Empty SSM parameter: ' + param)

        replacements.append((replace, value)) 
        return replacements