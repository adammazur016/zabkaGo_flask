from app.src.config.default_config import DefaultConfig
from dotenv import load_dotenv
import os

# loading environment variables
load_dotenv()


class Config:
    # Load default config and replace all variables found in .env
    def __init__(self):
        self.config = DefaultConfig()
        # Flask Part
        if os.environ.get("APP_NAME"):
            self.config.APP_NAME = os.environ.get("APP_NAME")
        # MySQL part
        if os.environ.get("MYSQL_HOST"):
            self.config.MYSQL_HOST = os.environ.get("MYSQL_HOST")
        if os.environ.get("MYSQL_PORT"):
            self.config.MYSQL_PORT = os.environ.get("MYSQL_PORT")
        if os.environ.get("MYSQL_USER"):
            self.config.MYSQL_USER = os.environ.get("MYSQL_USER")
        if os.environ.get("MYSQL_PASSWORD"):
            self.config.MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
        if os.environ.get("MYSQL_DB"):
            self.config.MYSQL_DB = os.environ.get("MYSQL_DB")
        self.config.MYSQL_CONFIG = {"host": self.config.MYSQL_HOST,
                                    "port": self.config.MYSQL_PORT,
                                    "user": self.config.MYSQL_USER,
                                    "password": self.config.MYSQL_PASSWORD,
                                    "database": self.config.MYSQL_DB}
