from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
articles = Table('articles', post_meta,
    Column('articleId', Integer, primary_key=True, nullable=False),
    Column('userId', Integer),
    Column('sectionId', Integer),
    Column('articletitle', String(length=255)),
    Column('text', Text),
    Column('pubdate', SmallInteger, default=ColumnDefault(0)),
    Column('datetime', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['articles'].columns['sectionId'].create()
    post_meta.tables['articles'].columns['userId'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['articles'].columns['sectionId'].drop()
    post_meta.tables['articles'].columns['userId'].drop()
