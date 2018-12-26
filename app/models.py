from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', back_populates='author',)
    story_posts = db.relationship('StoryPost', back_populates='author',)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class StoryPost(db.Model):
    __tablename__ = 'storypost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='story_posts',)
    #relationship to Post
    comments = db.relationship('Post', back_populates='story',)

    def __repr__(self):
        return f'<Story Post {self.title}>'


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')
    #relationship to StoryPost
    story_id = db.Column(db.Integer, db.ForeignKey('storypost.id'))
    story = db.relationship('StoryPost', back_populates='comments')

    def __repr__(self):
        return f'<Post {self.body}>'


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
