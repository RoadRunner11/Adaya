from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app


app = create_app('config.liv')
manager = Manager(app)

manager.add_command('db', MigrateCommand)
# ... some more code here ...

if __name__ == "__main__":
    manager.run()