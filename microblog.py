from app import app, db
from app.models import User, Post


@app.shell_context_processor
# While you work on your application, you will need to test things out in a Python shell very often, so having to
# repeat the above statements every time is going to get tedious, so this is a good time to address this problem.
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
