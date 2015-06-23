import click
import os

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
