import click
import IPython
import os

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
    import recastfrontend.models as models
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