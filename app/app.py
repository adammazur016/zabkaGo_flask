from src import app
from src.achievements import sync_achievement_db

# Synchronize achievements in database upon start up
sync_achievement_db()

if __name__ == '__main__':
    app.run()
