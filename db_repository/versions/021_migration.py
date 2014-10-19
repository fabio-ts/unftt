from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
article = Table('article', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('userId', Integer),
    Column('sectionId', Integer),
    Column('articletitle', String(length=255)),
    Column('text', Text),
    Column('datetime', DateTime),
    Column('pubdate', DateTime),
    Column('date', DateTime),
    Column('language', String(length=5)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['article'].columns['language'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['article'].columns['language'].drop()
