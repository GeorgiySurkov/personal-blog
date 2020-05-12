from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db, login

tag_post_relation = db.Table(
    'tag_post_relation',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    md_text = db.Column(db.Text())
    html_text = db.Column(db.Text(), nullable=True)
    date_published = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime)
    tags = db.relationship(
        'Tag',
        secondary=tag_post_relation,
        lazy='subquery',
        backref=db.backref('pages', lazy=True)
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        if 'html_text' not in kwargs:
            # TODO convert markdown to html
            pass
        super(Post, self).__init__(**kwargs)

    def __repr__(self):
        if len(self.md_text) > 15:
            showed_part = f'{self.md_text[:15]}...'
        else:
            showed_part = self.md_text
        if self.id:
            return f'<Post {self.id} {showed_part}>'
        return f'<Post {showed_part}>'


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    color = db.Column(db.String(6))  # Represents tag color in hex, for e.g. '#ebac0c' (hash symbol not included)

    def __repr__(self):
        if self.id:
            return f'<Tag {self.id} {self.name}>'
        return f'<Tag {self.name}>'


user_user_relation = db.Table(
    'user_user_relation',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    subscribers = db.relationship(
        'User',
        secondary=user_user_relation,
        lazy='subquery',
        backref=db.backref('subscriptions', lazy=True),
        primaryjoin=id == user_user_relation.c.user_id,
        secondaryjoin=id == user_user_relation.c.subscriber_id
    )
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        if self.id:
            return f'<User {self.id} {self.username}>'
        return f'<User {self.username}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id: str) -> User:
    return User.query.get(int(user_id))
