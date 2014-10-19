from app import db
from hashlib import md5
from app import app
import flask.ext.whooshalchemy as whooshalchemy
import re
ROLE_USER = 0
ROLE_ADMIN = 1


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	password = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	articles = db.relationship('Article', backref='user', lazy='dynamic')
	followed = db.relationship('User', 
							secondary = followers,
							primaryjoin = (followers.c.follower_id == id),
							secondaryjoin = (followers.c.followed_id == id),
							backref = db.backref('followers', lazy = 'dynamic'),
							lazy = 'dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_Articles(self):
		return Article.query.join(followers, (followers.c.followed_id == Article.userId)).filter(followers.c.follower_id == self.id).order_by(Article.date.desc())

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname = nickname).first() == None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname = new_nickname).first() == None:
				break
			version += 1
		return new_nickname

	def __repr__(self):
		return '<User %r>' % (self.nickname)

	@staticmethod
	def make_valid_nickname(nickname):
		return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

class Section(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	sectiontitle = db.Column(db.String(255))
	description = db.Column(db.String(512))
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	articles = db.relationship('Article', backref='section', lazy='dynamic')
	def __repr__(self):
		return '<section title %r>' % (self.sectiontitle)

class Article(db.Model):
	__searchable__ = ['text']

	id = db.Column(db.Integer, primary_key = True)
	userId = db.Column(db.Integer, db.ForeignKey('user.id'))
	sectionId = db.Column(db.Integer, db.ForeignKey('section.id'))
	articletitle = db.Column(db.String(255))
	text = db.Column(db.Text())
	datetime = db.Column(db.DateTime)
	pubdate = db.Column(db.DateTime)
	date = db.Column(db.DateTime)
	language = db.Column(db.String(5))

	def __repr__(self):
		return '<article title %r>' % (self.articletitle)

whooshalchemy.whoosh_index(app, Article)
