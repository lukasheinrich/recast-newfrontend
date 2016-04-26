import click
import os
import subprocess

@click.group()
def frontendcli():
  pass

@frontendcli.command()
@click.option('--config','-c')
def server(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from server import app
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
    
@frontendcli.command()
@click.option('--config','-c')
def celery(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from frontendconfig import config as frontendconf
  subprocess.call(['celery','worker','-A',frontendconf['CELERYAPP'],'-I','recastfrontend.asynctasks','-l','debug','-c','1'])

@frontendcli.command()
@click.option('--config','-c')
def rest_api(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from rest_server import app
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)

@frontendcli.command()
@click.option('--config', '-c')
def fill_db(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  import populate_db
  from recastfrontend.server import db
  click.secho('filled database at: {}'.format(db.engine.url), fg='green')
