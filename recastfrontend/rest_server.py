import recastdb.models
import recastdb.database

from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy.decorators import registerSchema
from recastfrontend.frontendconfig import config as frontendconf


registerSchema('User')(recastdb.models.User)
registerSchema('Analysis')(recastdb.models.Analysis)

SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI':  frontendconf['DBPATH'],
    'DOMAIN': {
        'User': recastdb.models.User._eve_schema['User'],
        'Analysis': recastdb.models.Analysis._eve_schema['Analysis'],
        }
}

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

Base = recastdb.database.db.Model

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base