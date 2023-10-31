import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'try-and-you-will-never-guess'
