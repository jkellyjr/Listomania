from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
    Column('phone_number', INTEGER),
    Column('email', VARCHAR(length=120)),
    Column('password', VARCHAR(length=120)),
    Column('about_me', VARCHAR(length=150)),
    Column('last_seen', DATETIME),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['about_me'].drop()
    pre_meta.tables['user'].columns['last_seen'].drop()
    pre_meta.tables['user'].columns['phone_number'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['about_me'].create()
    pre_meta.tables['user'].columns['last_seen'].create()
    pre_meta.tables['user'].columns['phone_number'].create()
