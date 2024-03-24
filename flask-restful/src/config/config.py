from .default_config import DefaultConfig
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
        if os.environ.get("PORT"):
            self.config.PORT = os.environ.get("PORT")
        if os.environ.get("HOST"):
            self.config.HOST = os.environ.get("HOST")
        # MySQL part
        if os.environ.get("MYSQL_HOST"):
            self.config.MYSQL_HOST = os.environ.get("MYSQL_HOST")
        if os.environ.get("MYSQL_USER"):
            self.config.MYSQL_USER = os.environ.get("MYSQL_USER")
        if os.environ.get("MYSQL_PASSWORD"):
            self.config.MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
        if os.environ.get("MYSQL_DB"):
            self.config.MYSQL_DB = os.environ.get("MYSQL_DB")
