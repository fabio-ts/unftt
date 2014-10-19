#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Article, Section
from datetime import datetime, timedelta

from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()




class TestCase(unittest.TestCase):
		def setUp(self):
			app.config['TESTING'] = True
			app.config['CSRF_ENABLED'] = False
			app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
			self.app = app.test_client()
			db.create_all()

		def tearDown(self):
			db.session.remove()
			db.drop_all()

		def test_avatar(self):
			u = User(nickname = 'john', email = 'john@example.com')
			avatar = u.avatar(128)
			expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
			assert avatar[0:len(expected)] == expected

		def test_make_unique_nickname(self):
			u = User(nickname = 'john', email = 'john@example.com')
			db.session.add(u)
			db.session.commit()
			nickname = User.make_unique_nickname('john')
			assert nickname != 'john'
			u = User(nickname = nickname, email = 'susan@example.com')
			db.session.add(u)
			db.session.commit()
			nickname2 = User.make_unique_nickname('john')
			assert nickname2 != 'john'
			assert nickname2 != nickname

		def test_follow(self):
			u1 = User(nickname = 'john', email = 'john@example.com')
			u2 = User(nickname = 'susan', email = 'susan@example.com')
			db.session.add(u1)
			db.session.add(u2)
			db.session.commit()
			assert u1.unfollow(u2) == None
			u = u1.follow(u2)
			db.session.add(u)
			db.session.commit()
			assert u1.follow(u2) == None
			assert u1.is_following(u2)
			assert u1.followed.count() == 1
			assert u1.followed.first().nickname == 'susan'
			assert u2.followers.count() == 1
			assert u2.followers.first().nickname == 'john'
			u = u1.unfollow(u2)
			assert u != None
			db.session.add(u)
			db.session.commit()
			assert u1.is_following(u2) == False
			assert u1.followed.count() == 0
			assert u2.followers.count() == 0
		def test_follow_Articles(self):
			# make four users
			u1 = User(nickname = 'john', email = 'john@example.com')
			u2 = User(nickname = 'susan', email = 'susan@example.com')
			u3 = User(nickname = 'mary', email = 'mary@example.com')
			u4 = User(nickname = 'david', email = 'david@example.com')
			s1 = Section(sectiontitle="S1", description="Sezione principale")
			db.session.add(u1)
			db.session.add(u2)
			db.session.add(u3)
			db.session.add(u4)
			# make four Articles
			utcnow = datetime.utcnow()
			p1 = Article(sectionId=s1.id,articletitle="t1", text = "Article from john", userId = u1.id, datetime=utcnow + timedelta(seconds = 1), pubdate=utcnow + timedelta(seconds = 1), date = utcnow + timedelta(seconds = 1))
			p2 = Article(sectionId=s1.id,articletitle="t2", text = "Article from susan", userId = u2.id, datetime=utcnow + timedelta(seconds = 2), pubdate=utcnow + timedelta(seconds = 2),date = utcnow + timedelta(seconds = 2))
			p3 = Article(sectionId=s1.id,articletitle="t3",text = "Article from mary", userId = u3.id,datetime=utcnow + timedelta(seconds = 3), pubdate=utcnow + timedelta(seconds = 3), date = utcnow + timedelta(seconds = 3))
			p4 = Article(sectionId=s1.id,articletitle="t4",text = "Article from david", userId = u4.id, datetime=utcnow + timedelta(seconds = 4), pubdate=utcnow + timedelta(seconds = 4),date = utcnow + timedelta(seconds = 4))
			db.session.add(p1)
			db.session.add(p2)
			db.session.add(p3)
			db.session.add(p4)
			db.session.commit()
			# setup the followers
			u1.follow(u1) # john follows himself
			u1.follow(u2) # john follows susan
			u1.follow(u4) # john follows david
			u2.follow(u2) # susan follows herself
			u2.follow(u3) # susan follows mary
			u3.follow(u3) # mary follows herself
			u3.follow(u4) # mary follows david
			u4.follow(u4) # david follows himself
			db.session.add(u1)
			db.session.add(u2)
			db.session.add(u3)
			db.session.add(u4)
			db.session.commit()
			# check the followed Articles of each user
			f1 = u1.followed_Articles().all()
			f2 = u2.followed_Articles().all()
			f3 = u3.followed_Articles().all()
			f4 = u4.followed_Articles().all()
#			assert len(f1) == 3
#			assert len(f2) == 2
#			assert len(f3) == 2
#			assert len(f4) == 1
#			assert f1 == [p4, p2, p1]
#			assert f2 == [p3, p2]
#			assert f3 == [p4, p3]
#			assert f4 == [p4]
		def test_delete_post(self):
			# create a user and a post
			u = User(nickname='john', email='john@example.com')
			p = Article(text='test post', userId=u.id, datetime=datetime.utcnow(), pubdate=datetime.utcnow(), date=datetime.utcnow())
			db.session.add(u)
			db.session.add(p)
			db.session.commit()
			# query the post and destroy the session
			p = Article.query.get(1)
			db.session.remove()
			# delete the post using a new session
			db.session = db.create_scoped_session()
			db.session.delete(p)
			db.session.commit()


if __name__ == '__main__':
	try:
		unittest.main()
	except:
		pass
	cov.stop()
	cov.save()
	print "\n\nCoverage Report:\n"
	cov.report()
	print "HTML version: " + os.path.join(basedir, "tmp/coverage/index.html")
	cov.html_report(directory='tmp/coverage')
	cov.erase()
