from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

import application
import database

migrate = Migrate(application.application, database.db)
manager = Manager(application.application)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
