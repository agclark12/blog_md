from blog_md import app
from blog_md.db_setup import Base
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Date(Base):

    __tablename__ = "dates"

    id = Column(Integer, primary_key=True)
    key = Column(String)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

    def __init__(self, key=None, day=None, month=None, year=None):
        self.key = key
        self.day = day
        self.month = month
        self.year = year

class Book(Base):

    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    year_read = Column(String)
    title = Column(String)
    author = Column(String)
    year_published = Column(String)
    no_pages = Column(String)

    def __init__(self, year_read=None, title=None, author=None, year_published=None, no_pages=None):
        self.year_read = year_read
        self.title = title
        self.author = author
        self.year_published = year_published
        self.no_pages = no_pages

    def __repr__(self):
        return '<Book {}>'.format(self.title)

class User(UserMixin,Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String, unique=True)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

