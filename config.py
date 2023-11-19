import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))  ## This sets up the base dir for the entire project

load_dotenv()


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try-and-you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'microblog_db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
    POSTS_PER_PAGE = 3
