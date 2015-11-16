import os
from flask.ext.script import Manager

from blog import app

manager = Manager(app)

from blog.models import Post
from blog.database import session

from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

from flask.ext.migrate import Migrate, MigrateCommand
from blog.database import Base
#import flask
#import flask_resize

#resize = flask_resize.Resize()

#@manager.command
#def create_app(**config_values):
#    app = flask.Flask()
#    app.config.update(**config_values)
#    resize.init_app(app)
#    return app

# And later on...
#app = create_app(RESIZE_URL='http://s14.postimg.org/60aamxeq9/chamonix.png')
@manager.command
def adduser():
    input = raw_input
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()

@manager.command
def seed():
    content = """Test blog content..."""
    for i in range(10):
        post = Post(
            title="Test Post #{}".format(i),
            content=content
        )
        session.add(post)
    session.commit()
    
@manager.command    
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)




class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


  
if __name__ == "__main__":
    manager.run()
    
    