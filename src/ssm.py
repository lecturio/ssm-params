import boto3

PROJ_ENABLED = '/SSM_ENABLED'

class AdapterSSM:
  def __init__(self, project, boto):
    session = boto3.Session(**boto)
    self.client = session.client('ssm')
    if not project:
      raise Exception('project is required')
    self.project_prefix = '/' + project

  def param(self, name):
    return self.project_prefix + name

  def get_parameter(self, parameter_name):
    param = self.param(parameter_name)
    try:
      return self.client.get_parameter(Name=param, WithDecryption=True)['Parameter']['Value']
    except self.client.exceptions.ParameterNotFound:
      return ''
  
  def put_parameter(self, parameter_name, parameter_value, tier='Standard', data_type='text'):
    param = self.param(parameter_name)
    return self.client.put_parameter(
      Name=param,
      Value=parameter_value,
      Type = 'SecureString',
      Overwrite = True,
      Tier = tier,
      DataType = 'text'
    )
  
  def enableProject(self):
    self.put_parameter(PROJ_ENABLED, 'true')

  def isProjectEnabled(self):
    return self.get_parameter(PROJ_ENABLED) == 'true'