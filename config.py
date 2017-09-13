# config file for listomania

import os

basedir = os.path.abspath(os.path.dirname(__file__))
#  path to db file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# folder to store sqlalchemy-migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# cross site request forgery prevention
WTF_CSRF_ENABLED = True
SECRET_KEY = 'cryptographic-token-change-tehe'

# pagination
POSTS_PER_PAGE = 3

# whoosh: used for full text search
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'username@gmail.com'
MAIL_PASSWORD = 'password'

# administrator list
ADMINS = ['username@domain.com']
