from flask_migrate import MigrateCommand
from flask_script import Manager, Server
from __init__ import create_app

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)
manager.add_command("runserver", Server())

if __name__ == '__main__':
    manager.run()
