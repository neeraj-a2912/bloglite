from flask_sqlalchemy import SQLAlchemy
from bloglite import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email_address=db.Column(db.String(100),nullable=False)
    bio=db.Column(db.String(40),nullable=True)
    image=db.Column(db.String(30), default='default.png', nullable=False)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)
    followed = db.relationship('User', secondary=followers,
                                primaryjoin=(followers.c.follower_id == id),
                                secondaryjoin=(followers.c.followed_id == id),
                                backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.time_stamp.desc())

    def __init__(self, name, email_address, password):
        self.name=name
        self.email_address=email_address
        self.password=password
    
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    caption=db.Column(db.String(100),nullable=False)
    content=db.Column(db.String(400), nullable=True)
    time_stamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    img_post=db.Column(db.String(30), nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __init__(self, caption, content, user_id, img_post):
       self.caption=caption
       self.user_id=user_id
       self.content=content
       self.img_post=img_post

