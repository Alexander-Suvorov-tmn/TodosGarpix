import sys
sys.path.insert(0, r'/home/alexandr/work_test/Todo/TodosGarpix')

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from ap.base import app, db
from dotenv import load_dotenv


load_dotenv('.env')

app.config.from_object(os.environ.get('APP_SETTINGS'))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
