from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
article = Table('article', pre_meta,
    Column('articleId', Integer, primary_key=True, nullable=False),
    Column('articletitle', String),
    Column('text', Text),
    Column('pubdate', SmallInteger),
    Column('datetime', DateTime),
    Column('userId', String),
)

section = Table('section', pre_meta,
    Column('sectionId', Integer, primary_key=True, nullable=False),
    Column('sectiontitle', String),
    Column('description', String),
    Column('role', SmallInteger),
)

user = Table('user', pre_meta,
    Column('userId', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('password', String),
    Column('email', String),
    Column('role', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['article'].drop()
    pre_meta.tables['section'].drop()
    pre_meta.tables['user'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['article'].create()
    pre_meta.tables['section'].create()
    pre_meta.tables['user'].create()
