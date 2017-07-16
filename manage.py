#!/usr/bin/python3

from flask_script import Server, Manager
from catalog import app

manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=9000))

if __name__ == "__main__":
    manager.run()
