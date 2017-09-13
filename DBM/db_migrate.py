#!flask/bin/python

# This script aids in the migration of databases (migration being any change to the structure of the database).
# It compares the old db structure against the structure of the models and generates,
# and the differences are recorded as a script.
# The scripts know how to apply the migration or undo it, making it possible to updgrade/downgrade db format
# The scripts generated reside: root/db_repository/versions/script_name.py
# For better results: Don't alter the field names, only add / remove fields/models
# -----------------------------
# How to Run:
#   1. Ensure virtual enviornment is intalled (python3 -m venv flask)
#   2. Change permissions of the script to executable (chmod a+x script.py)
#   3. Run (./script.py <arguments>)


import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))

tmp_module = imp.new_module('old_model')
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_model, tmp_module.__dict__)

script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
