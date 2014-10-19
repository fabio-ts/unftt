# -*- coding: utf-8 -*-

import os

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' },
    { 'name': 'Facebook', 'url': 'https://www.facebook.com'}]

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'fabioquintilii@gmail.com'
MAIL_PASSWORD = 'javelin23'

# administrator list
ADMINS = ['fabioquintilii@gmail.com']


# pagination
POSTS_PER_PAGE = 2

# available languages
LANGUAGES = {
    'es': 'Español',
    'en': 'English',
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = 'fabio1971' # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = 'sT1RhC1nTmFEKwrRK3bC5cEyFnNiTyglaPqz' # enter your MS translator app secret here

