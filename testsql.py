#! flask/bin/python

from app import db, models
import datetime

#u = models.User(nickname='john', email='john@email.com', role=models.ROLE_USER)
#db.session.add(u)
#db.session.commit()


users = models.User.query.all()
print users

for u in users:
	print u.id, u.nickname, u.password, u.email, u.role

u = models.User.query.get(1)
#p = models.Article(id=1,articletitle='tanto va la gazza al lazzo...', text='hhhhhhh hhhhhhh ggggghhghgh GINOOOOOO!!!', datetime=datetime.datetime.utcnow(), pubdate=datetime.datetime.utcnow(), date=datetime.datetime.utcnow(), author=u)

#db.session.add(p)
#db.session.commit()

art = models.Article.query.all()

print art

u = models.User.query.get(1)

print u

a = u.articles.all()

print a

for article in a:
	print article.articletitle, article.text

print models.User.query.order_by('nickname desc').all()


users = models.User.query.all()
posts = models.Article.query.all()

for u in users:
	db.session.delete(u)

for p in posts:
	db.session.delete(p)

db.session.commit()




