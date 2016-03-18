import recastdb.models
from recastdb.database import db

from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy.decorators import registerSchema
from recastfrontend.frontendconfig import config as frontendconf


registerSchema('users')(recastdb.models.User)
registerSchema('Analysis')(recastdb.models.Analysis)
registerSchema('Subscription')(recastdb.models.Subscription)


SETTINGS = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': frontendconf['DBPATH'],
    'DOMAIN': {
        'users': recastdb.models.User._eve_schema['users'],
        'Analysis': recastdb.models.Analysis._eve_schema['Analysis'],
        'Subscription': recastdb.models.Subscription._eve_schema['Subscription'],
        }
}

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

#app.app_context().push()

Base = recastdb.database.db.Model

# bind SQLAlchemy
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()
#db.init_app(app)
#db.init_app(app)

user = recastdb.models.User('test user', 'test@test.me')
db.session.add(user)
db.session.commit()
