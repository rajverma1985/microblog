import os

basedir = os.path.abspath(os.path.dirname(__file__))  ## This sets up the base dir for the entire project


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try-and-you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'microblog_db.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
