import os
import pkg_resources
import yaml

def default_config():
  return yaml.load(open(pkg_resources.resource_filename('recastfrontend','resources/defaultconfig.yaml')))

def update_config(config):
  #if we are runnning inside a container
  if os.environ.has_key('REDIS_PORT'):
    os.environ['RECAST_REDISURL'] = os.environ['REDIS_PORT'].replace('tcp', 'redis')
  #update config with ENV variables that have RECAST_*
  for k, v in os.environ.iteritems():
    if k.startswith('RECAST_'):
      config.update({k.replace('RECAST_',''): v})
  return config

def mk_config():
  the_config = default_config()
  the_config = update_config(the_config)  
  if os.environ.has_key('RECASTCONTROLCENTER_CONFIG'):
    custom_config = yaml.load(open(os.environ['RECASTCONTROLCENTER_CONFIG']))
    the_config.update(**custom_config)
  return the_config
  
config = mk_config()
