from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
articles = Table('articles', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('articletitle', String),
    Column('text', Text),
    Column('pubdate', SmallInteger),
    Column('datetime', DateTime),
    Column('userId', Integer),
)

sections = Table('sections', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sectiontitle', String),
    Column('description', String),
    Column('role', SmallInteger),
)

users = Table('users', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String),
    Column('password', String),
    Column('email', String),
    Column('role', SmallInteger),
)

article = Table('article', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('userId', Integer),
    Column('articletitle', String(length=255)),
    Column('text', Text),
    Column('pubdate', SmallInteger, default=ColumnDefault(0)),
    Column('datetime', DateTime),
)

section = Table('section', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('sectiontitle', String(length=255)),
    Column('description', String(length=512)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('password', String(length=64)),
    Column('email', String(length=120)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['articles'].drop()
    pre_meta.tables['sections'].drop()
    pre_meta.tables['users'].drop()
    post_meta.tables['article'].create()
    post_meta.tables['section'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['articles'].create()
    pre_meta.tables['sections'].create()
    pre_meta.tables['users'].create()
    post_meta.tables['article'].drop()
    post_meta.tables['section'].drop()
    post_meta.tables['user'].drop()
