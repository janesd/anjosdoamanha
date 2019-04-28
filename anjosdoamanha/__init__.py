from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'anjosdados.db')

app.config['SECRET_KEY'] = 'mysecret' # TODO : generate application key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#import pdb; pdb.set_trace()
db = SQLAlchemy(app)
db.init_app(app)

from anjosdoamanha import routes