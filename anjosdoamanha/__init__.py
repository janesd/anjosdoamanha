from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
track_modifications=False

DOCKER = False
if DOCKER:
    POSTGRES = {
        'user': 'postgres',
        'password': 'secret',
        'db': 'postgres',
        'host': 'db',
        'port': '5432',
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(password)s@%(host)s:%(port)s/%(db)s' % POSTGRES
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anjosdoamanha/anjosdados.db'

app.config['SECRET_KEY'] = 'mysecret' # TODO : generate application key

db.init_app(app)

from anjosdoamanha import routes