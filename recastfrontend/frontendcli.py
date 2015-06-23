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
  app.run(host='0.0.0.0',port = 5000)
  
@frontendcli.command()
@click.option('--config','-c')
def celery(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from frontendconfig import config as frontendconf
  subprocess.call(['celery','worker','-A',frontendconf['CELERYAPP'],'-I','recastfrontend.asynctasks','-l','debug'])

@frontendcli.command()
@click.option('--config','-c')
def rest_api(config):
  if config:
    os.environ['RECASTCONTROLCENTER_CONFIG'] = config
  from rest_server import app
  app.run()