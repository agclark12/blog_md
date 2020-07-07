import os
import sys
import sqlite3

from flask import Flask
from flask_flatpages import pygments_style_defs, pygmented_markdown
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

#configurations
DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code','codehilite']
pygments_style_defs(style='default')
FLATPAGES_ROOT = 'static/content'
csrf = CSRFProtect()

#this is so jinja text gets rendered in the markdown blog
def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    return pygmented_markdown(prerendered_body)

#initializes app
app = Flask(__name__)

#imports my modules
from blog_md.routes import *
from blog_md.db_setup import init_db

#config
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog_md/db/db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rootmittenboy'
app.config['FLATPAGES_HTML_RENDERER'] = prerender_jinja

#initializes extensions
csrf.init_app(app)
db = SQLAlchemy(app)
init_db()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "build":
            freezer.freeze()
        if sys.argv[1] == "listen":
            app.run(host='0.0.0.0',debug=False)
    else:
        app.run(debug=True)