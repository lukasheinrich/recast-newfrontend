import click
import IPython
import os
import yaml

@click.group()
def admincli():
  pass
  
@admincli.command()
@click.option('--config','-c')
def dbshell(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from recastfrontend.server import app
  with app.app_context():
    from recastfrontend.server import db
    import recastdb.models as models
    print "models and db modules are available"
    IPython.embed()

@admincli.command()
@click.option('--config','-c')
def create_db(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from recastfrontend.server import app
  with app.app_context():
    from recastfrontend.server import db
    db.create_all()
    click.secho('created database at: {}'.format(db.engine.url), fg = 'green')
    
@admincli.command()
@click.option('--output','-o')
def mk_config(output):
  config_data = {}
  for k,v in os.environ.iteritems():
    if k.startswith('RECAST_'):
        config_data[k.replace('RECAST_','')] = v
  with open(output,'w') as outfile:
     outfile.write(yaml.dump(config_data,default_flow_style=False))
  