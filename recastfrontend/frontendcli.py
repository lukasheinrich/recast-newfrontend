import click
import os
import subprocess
import logging
from admincli import set_config
logging.basicConfig(level = logging.INFO)

@click.group()
def frontendcli():
  pass

@frontendcli.command()
@click.option('--config','-c')
def server(config):
    set_config(config)
    from server import app
    port = int(os.environ.get("RECAST_FRONTEND_PORT", 5000))

    app.run(host='0.0.0.0', port=port, ssl_context = (os.environ['RECAST_SSL_CERT'],os.environ['RECAST_SSL_KEY']))

@frontendcli.command()
@click.option('--config','-c')
def celery(config):
    set_config(config)
    subprocess.check_call(['celery','worker','-A',frontendconf['CELERYAPP'],'-I','recastfrontend.asynctasks','-l','debug','-c','1'])
