import click
import IPython
import os
import yaml

def set_config(config):
    if config:
        os.environ['RECASTFRONTEND_CONFIG'] = config
    from frontendconfig import config as frontendconf


@click.group()
def admincli():
    pass

@admincli.command()
@click.option('--config','-c')
def dbshell(config):
    set_config(config)
    from recastfrontend.server import app
    with app.app_context():
        from recastfrontend.server import db
        import recastdb.models as models
        print "models and db modules are available"
        IPython.embed()

@admincli.command()
@click.option('--config','-c')
def create_db(config):
    set_config(config)
    from recastfrontend.server import app
    with app.app_context():
        from recastfrontend.server import db
        db.create_all()
        click.secho('created database at: {}'.format(db.engine.url), fg = 'green')

@admincli.command()
@click.option('--config','-c')
def drop_db(config):
    set_config(config)
    from recastfrontend.server import app
    with app.app_context():
        from recastfrontend.server import db
        db.drop_all()

@admincli.command()
@click.option('--config', '-c')
def fill_db(config):
    set_config(config)
    import populate_db
    from recastfrontend.server import db
    click.secho('filled database at: {}'.format(db.engine.url), fg='green')

@admincli.command()
@click.option('--config', '-c')
def test(config):
    set_config(config)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
