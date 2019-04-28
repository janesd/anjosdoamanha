from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from anjosdoamanha.models import db
from anjosdoamanha import app


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()