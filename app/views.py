from app import app, db, lm, oid, babel
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, EditForm, PostForm, SearchForm
from models import User, ROLE_USER, ROLE_ADMIN, Article
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES
from datetime import datetime
from emails import follower_notification
from flask.ext.babel import gettext
from guess_language import guessLanguage

@app.route('/articles')
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page=1):
	form = PostForm()

	if form.validate_on_submit():
			language = guessLanguage(form.post.data)
			if language == 'UNKNOWN' or len(language) > 5:
				language = ''
			post = Article(text = form.post.data, datetime = datetime.utcnow(), userId = g.user.id, language = language)
			db.session.add(post)
			db.session.commit()
			flash(gettext('Your post is now live!'))
			return redirect(url_for('index'))

	user = g.user
	posts = g.user.followed_Articles().paginate(page, POSTS_PER_PAGE, False).items

	return render_template('index.htm',
		  title = 'Home',
		  user = user,
			form = form,
		  posts = posts)

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
		user = User.query.filter_by(nickname = nickname).first()
		if user == None:
				flash(gettext('User ' + nickname + ' not found.'))
				return redirect(url_for('index'))
		articles = Article.query.filter_by(userId=g.user.id).order_by(Article.id.desc()).paginate(page, POSTS_PER_PAGE, False)
		return render_template('user.htm', user = user, articles = articles)

def articles():
		articles = [] # [article1, article2]
		return render_template('index.htm', section=section1, articles=articles)

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.htm', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname, g.user)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
	 	db.session.add(g.user)
		db.session.commit()
		flash(gettext('Your changes have been saved.'))
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.htm',form = form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.htm'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.htm'), 500

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash(gettext('Invalid login. Please try again.'))
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
			nickname = resp.nickname
			if nickname is None or nickname == "":
				nickname = resp.email.split('@')[0]
			nickname = User.make_valid_nickname(nickname)
			nickname = User.make_unique_nickname(nickname)
			user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
			db.session.add(user)
			db.session.commit()
			# make the user follow him/herself
			db.session.add(user.follow(user))
			db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash(gettext('User ' + nickname + ' not found.'))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname = nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot follow ' + nickname + '.'))
        return redirect(url_for('user', nickname = nickname))
    db.session.add(u)
    db.session.commit()
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname = nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
	user = User.query.filter_by(nickname = nickname).first()

	if user == None:
		  flash(gettext('User ' + nickname + ' not found.'))
		  return redirect(url_for('index'))
	if user == g.user:
		  flash(gettext('You can\'t unfollow yourself!'))
		  return redirect(url_for('user', nickname = nickname))
	u = g.user.unfollow(user)
	if u is None:
		  flash(gettext('Cannot unfollow ' + nickname + '.'))
		  return redirect(url_for('user', nickname = nickname))
	db.session.add(u)
	db.session.commit()
	flash(gettext('You have stopped following ' + nickname + '.'))
	return redirect(url_for('user', nickname = nickname))

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()
		g.search_form = SearchForm()

@app.route('/search', methods = ['POST'])
@login_required
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_results', query = g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
  results = Article.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
  return render_template('search_results.htm', query = query, results = results, user=g.user)
#g.user e' sbagliato, devo risalire a chi ha scritto il commento non riportare l'utente loggato ora. cmq per scopi didattici va bene cosi'

@babel.localeselector
def get_locale():
    return "es" #request.accept_languages.best_match(LANGUAGES.keys())

@app.route('/delete/<int:id>')
@login_required
def delete(id):
	post = Article.query.get(id)
	if post is None:
		flash('Post not found.')
		return redirect(url_for('index'))
	if post.userId != g.user.id:
		flash('You cannot delete this post.')
		return redirect(url_for('index'))
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted.')
	return redirect(url_for('index'))

