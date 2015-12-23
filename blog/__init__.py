import os
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
config_path = os.environ.get("CONFIG_PATH", "blog.config.DevelopmentConfig")
app.config.from_object(config_path)

from . import login
from . import views
from . import filters


##\	DEBUG=True,
#	#EMAIL SETTINGS
#	MAIL_SERVER='smtp.gmail.com',
#	MAIL_PORT=465,
#	MAIL_USE_SSL=True,
#	MAIL_USERNAME = 'your@gmail.com',
#	MAIL_PASSWORD = 'yourpassword'
#	)
#mail = Mail(app)


