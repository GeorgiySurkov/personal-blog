from . import db

tag_post_relation = db.Table(
    'tag_post_relation',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), foreign_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), foreign_key=True)
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
