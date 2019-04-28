import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from anjosdoamanha.models import db
from anjosdoamanha import app

MIGRATION_DIR = os.path.join('anjosdoamanha', 'migrations')

manager = Manager(app)
migrate = Migrate(app, db, directory=MIGRATION_DIR)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

