from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

#initializes app
app = Flask(__name__, instance_relative_config=True)

#import config from files depending on environment
app.config.from_object('config.default') #from config/default.py
app.config.from_pyfile('config.py') #from instance/config
app.config.from_object('config.development') #keep this for dev server, comment out for production
# app.config.from_object('config.production') #keep this for production server, comment out for dev
# app.config.from_object('config.listen') #for running dev server to test on local network (mobile, e.g.)

#imports my modules
from blog_md.routes import *
from blog_md.db_setup import init_db

#initializes extensions
csrf = CSRFProtect()
csrf.init_app(app)
db = SQLAlchemy(app)
init_db()

if __name__ == "__main__":
    app.run()