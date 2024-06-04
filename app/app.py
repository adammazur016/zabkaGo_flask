import time

import mysql.connector.errors

from src import app
from src.achievements import sync_achievement_db


def init():
    sync = False
    # Try until achievements are synchronized between db and app
    while not sync:
        try:
            sync_achievement_db()
        except mysql.connector.errors.InterfaceError():
            time.sleep(5)
        else:
            sync = True


# Start using python app.py
if __name__ == '__main__':
    init()
    app.run()
# Start using flask run
else:
    init()
