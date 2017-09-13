# listomania/app/models.py

from hashlib import md5
from app import db,  app
import flask_whooshalchemy as whooshalchemy
# import sys
# if sys.version_info >= (3, 0):
#     enable_search = False
#     print('----- search not enabled ----')
# else:
#     enable_search = True
#     import flask_whooshalchemy as whooshalchemy
enable_search = True

#=================== TABLES =====================

# auxillary table with only foreign keys does not require models
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

#================== MODELS =====================
# user model
class User(db.Model):

    def __init__(self, name, phone_number, email, password):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.password = password

    id = db.Column(db.Integer, unique = True, primary_key = True)
    name = db.Column(db.String(64), index = True)
    phone_number = db.Column(db.Integer, index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User', secondary = followers, primaryjoin = (followers.c.follower_id == id),
                    secondaryjoin = (followers.c.followed_id == id), backref = db.backref('followers', lazy = 'dynamic'),
                    lazy = 'dynamic')

    # flask_login expects these certain properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False    # only fake users would be True

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)


    # define how to display the user object
    def __repr__(self):
        return '<User %r :: %r :: %r :: %r>' % (self.name, self.phone_number, self.email, self.password)

    # let gravatar handle heavy lifting of pictures
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    # follow user
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    # unfollow user
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    # determine if following
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # return posts of followed users
    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())



# posts model (one-to-many relationship)
class Post(db.Model):
    # only search the body of the posts
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


if enable_search:
    whooshalchemy.whoosh_index(app, Post)
