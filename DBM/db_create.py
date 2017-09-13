#!flask/bin/python


#  This script creates a SQLite database using SQLAlchemy
# Creates: An empty app.db file is created at start to support migrations
# Creates: A db_repository directory is created as the lcoation  where SQLAlchemy-migrate stores its data files
# If db_repository exists, it will not be overwritten allowing you to recreate the database while leaving the existing repository if necessary
# -----------------------------
# How to Run:
#   1. Ensure virtual enviornment is intalled (python3 -m venv flask)
#   2. Change permissions of the script to executable (chmod a+x script.py)
#   3. Run (./script.py <arguments>)


from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control( SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO) )
