# listomania/app/views.py

from flask import render_template, redirect, url_for, request, session, flash, g
from .forms import SignUpForm, LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from app import app, db, lm
from werkzeug import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS
from .emails import follower_notification

#
# Known bugs
# 1. The users name is used as verification, but the name is not required to be unique
#  2. else statement loops infinitely in login function
#
#

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@lm.user_loader
def load_user(id):
    return User.query.get( int(id) )


# ====================== VIEW HANDLERS ====================
@app.route('/', methods = ['POST', 'GET'])
@app.route('/index', methods = ['POST', 'GET'])
@app.route('/index/<int:page>', methods = ['POST', 'GET'])
@login_required
def index(page = 1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body = form.post.data, timestamp = datetime.utcnow(), author = g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html', title = 'Home', user = g.user, form = form, posts = posts)


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data)
        user = User(form.name.data, form.phone_number.data, form.email.data, hashed_password)
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
        db.session.commit()
        login_user(user, remember = True)
        flash('Thanks for registering')
        return redirect(url_for('index'))
    return render_template('signup.html', title = 'Sign Up', form = form)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash('You are already signed in')
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit:
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and check_password_hash(user.password, form.password.data):
            remember_me = False
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember = remember_me)
            return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
def logout():
    remember_me = False
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<name>')
@app.route('/user/<name>/<int:page>')
@login_required
def user(name, page = 1):
    user = User.query.filter_by(name = name).first()
    # !! change later bc it is okay to have more than one user with the same name
    if user == None:
        flash('User %r not found' % name)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    followers = user.followers.all()
    return render_template('user.html', user = user, posts = posts, followers = followers)


@app.route('/edit', methods = ['POST', 'GET'])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.name = form.name.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('index'))
    else:
        form.name.data = g.user.name
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form = form)


@app.route('/follow/<name>')
@login_required
def follow(name):
    user = User.query.filter_by(name = name).first()
    if user is None:
        flash("User %s not found" % user)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You cannot follow yourself. You\'re already doing it.')
        return redirect(url_for('user', name = name))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow %s ' % name)
        return redirect(url_for('user', name = name))
    db.session.add(u)
    db.session.commit()
    flash('You\'re now following %s !' % name)
    follower_notification(user, g.user)
    return redirect(url_for('user', name = name))


@app.route('/unfollow/<name>')
@login_required
def unfollow(name):
    user = User.query.filter_by(name = name).first()
    if user is None:
        flash('User %s not found.' % name)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You cannot unfollow yourself.')
        return redirect(url_for('user', name = name))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow %s .' % name)
        return redirect(url_for('user', name = name))
    db.session.add(u)
    db.session.commit()
    flash('You unfollowed %s ' % name)
    return redirect(url_for('user', name = name))

# collects search query and passes query as argument
@app.route('/search', methods = ['POST'])
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html', query = query, results = results)
