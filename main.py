from app import app, db
from app.models import User, Tag, Post


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'app': app,
        'User': User,
        'Tag': Tag,
        'Post': Post
    }


if __name__ == '__main__':
    app.run(load_dotenv=True)
