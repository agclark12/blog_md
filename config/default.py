from blog_md import app

from flask import render_template_string, Markup
from flask_flatpages import pygments_style_defs, pygmented_markdown

#this is so jinja text gets rendered in the markdown blog
def prerender_jinja(text):
    prerendered_body = render_template_string(Markup(text))
    return pygmented_markdown(prerendered_body)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_ROOT = 'static/content'
FLATPAGES_EXTENSION = '.md'
FLATPAGES_MARKDOWN_EXTENSIONS = ['fenced_code','codehilite']
app.config['FLATPAGES_HTML_RENDERER'] = prerender_jinja
pygments_style_defs(style='default')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
