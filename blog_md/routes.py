import os
from datetime import date

from flask import render_template, request, redirect, url_for, flash, abort, send_from_directory
from werkzeug.utils import secure_filename
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#imports my modules
from blog_md import app
from blog_md.forms import *
from blog_md.db_setup import *
from blog_md.models import *
from blog_md import utilities as util

#config
NEWS_DIR = app.root_path + '/static/content/news'
POST_DIR = 'posts'

#initialize the packages
flatpages = FlatPages(app)
freezer = Freezer(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('friendly'), 200, {'Content-Type': 'text/css'}

@app.route("/index")
@app.route("/")
def index():
    news_file_list = [_ for _ in os.listdir(NEWS_DIR) if '.txt' in _]
    news_file_list.sort(reverse=True)
    news_file_list = news_file_list[:3]
    news_list = [[[],[],[],[]] for _ in news_file_list]
    for i in range(len(news_file_list)):
        news_file = news_file_list[i]
        ifile = open(os.path.join(NEWS_DIR,news_file),'r')
        lines = ifile.readlines()
        for j in range(4):
            news_list[i][j] = lines[j].split('\n')[0]
    post_list = [p for p in flatpages if p.path.startswith(POST_DIR)]
    post_list.sort(key=lambda item:item['date'], reverse=True)
    return render_template('index.html', news_list=news_list, posts=post_list[:3], title='Home')

@app.route('/news/upload/', methods=['GET', 'POST'])
@login_required
def news_upload():
    form = UploadNews()
    if request.method == 'POST' and form.validate_on_submit:
        if form.submit.data:
            txt = form.text_file.data
            img = form.image_file.data
            text_file = secure_filename(txt.filename)
            image_file = secure_filename(img.filename)
            txt.save(os.path.join('static/content/news', text_file))
            img.save(os.path.join('static/content/news/media', image_file))
            flash('News entry was sucessfully uploaded')
            return redirect(url_for('index'))
        else:
            flash('No file uploaded')
            return redirect(url_for('index'))
    return render_template('news_upload.html',form=form)

@app.route("/posts/")
def posts():
    post_list = [p for p in flatpages if p.path.startswith(POST_DIR)]
    post_list.sort(key=lambda item:item['date'], reverse=True)
    tags = [p['tag'] for p in post_list]
    tags = util.natural_sort(util.get_unique_list(tags))
    return render_template('posts.html', posts=post_list, tags=tags, title="Blog")

@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post, title=post.meta['title'])

@app.route('/posts/upload/', methods=['GET', 'POST'])
@login_required
def post_upload():
    form = UploadPost()
    if request.method == 'POST' and form.validate_on_submit:
        if form.submit.data:
            f = form.file.data
            filename = secure_filename(f.filename)
            f.save(os.path.join('static/content/posts', filename))
            for media_file in [form.media_file1.data,form.media_file2.data,form.media_file3.data,
                               form.media_file4.data,form.media_file5.data]:
                if media_file:
                    filename = secure_filename(media_file.filename)
                    media_file.save(os.path.join('static/content/posts/media', filename))
            flash('Post was sucessfully uploaded')
            return redirect(url_for('posts'))
        else:
            flash('No file uploaded')
            return redirect(url_for('posts'))
    return render_template('post_upload.html',form=form, title="Upload New Post")

@app.route('/posts/by_tag/<tag>/')
def posts_tagged(tag):
    post_list = [p for p in flatpages if p.path.startswith(POST_DIR)]
    post_list.sort(key=lambda item:item['date'], reverse=True)
    tags = [p['tag'] for p in post_list]
    tags = util.natural_sort(util.get_unique_list(tags))
    post_list = [p for p in post_list if p['tag']==tag]
    return render_template('posts_tagged.html', tag=tag, posts=post_list, tags=tags, title="Blog - %s"%tag)

@app.route('/research_interests/')
def research_interests():
    return render_template('research_interests.html', title="Research Interests")

@app.route('/publications/')
def publications():
    return render_template('publications.html', title="Publications")

@app.route('/resources/')
def resources():
    return render_template('resources.html', title="Resources")

@app.route('/about_me/')
def about_me():
    return render_template('about_me.html', title="About Me")

@app.route('/links/')
def links():
    return render_template('links.html', title="Links")

@app.route('/contact/')
def contact():
    return render_template('contact.html', title="Contact")

@app.route('/booklist/')
def booklist():
    query = Book.query.all()
    booklist = [row.__dict__ for row in query]
    bookcount = len(booklist)-1
    pagecount = sum(int(_["no_pages"]) for _ in booklist[:-1])
    updated_date = Date.query.filter_by(key="booklist_last_updated")[0]
    updated_date_string = date(updated_date.year,updated_date.month,updated_date.day).strftime("%d-%m-%Y")
    return render_template('booklist.html', booklist=booklist, bookcount=bookcount, pagecount=pagecount, title="Booklist",
                           updated_date=updated_date_string)

def update_booklist_last_updated():
    today = date.today()
    today_dict = {'day':today.day, 'month':today.month, 'year':today.year}
    updated_date = Date.query.filter_by(key='booklist_last_updated').update(today_dict)
    #note that this does not commit the change!

@app.route('/booklist/add_book/', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBook(request.form)
    if request.method == 'POST' and form.validate():
        if form.submit.data:
            book = Book(form.year_read.data,form.title.data,form.author.data,form.year_published.data,form.no_pages.data)
            db_session.add(book)
            update_booklist_last_updated()
            db_session.commit()
            flash('New Book Added!')
            return redirect(url_for('booklist',_anchor='current'))
        else:
            flash('Nothing was added')
            return redirect(url_for('booklist'))
    return render_template('add_book.html', form=form, title="Add Book")

@app.route('/booklist/edit_book/<id>/', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    query = Book.query.get(id)
    form = EditBook(request.form,obj=query)
    if request.method == 'POST' and form.validate():
        if form.submit.data:
            included_keys = ['year_read','title','author','year_published','no_pages']
            data = {k:v for k,v in form.data.items() if k in included_keys} #gets rid of submit and csrf key
            db_session.query(Book).filter_by(id=id).update(data)
            update_booklist_last_updated()
            db_session.commit()
            flash('Book < %s > has been edited!'%id)
            return redirect(url_for('booklist'))
        else:
            flash('Nothing was edited')
            return redirect(url_for('booklist'))
    return render_template('edit_book.html', form=form, id=id, title="Edit Book")

@app.route('/booklist/delete_book/<id>/', methods=['GET', 'POST'])
@login_required
def delete_book(id):
    query = Book.query.get(id)
    form = DeleteBook(request.form,obj=query)
    if request.method == 'POST' and form.validate():
        if form.submit.data:
            db_session.delete(query)
            update_booklist_last_updated()
            db_session.commit()
            flash('Book %s has been deleted!' % id)
            return redirect(url_for('booklist'))
        else:
            flash('Nothing was deleted')
            return redirect(url_for('booklist'))
    return render_template('delete_book.html', form=form, id=id, title="Delete Book")

@app.route('/CV/')
def cv():
    return send_from_directory('static/content/media', 'Clark_CV.pdf', as_attachment=True)

@app.route('/login/', methods=['GET', 'POST'])
@limiter.limit("10/minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# @app.route('/create_admin') #just to create an admin password at the beginning
# def create_admin():
#     u = User(username="user")
#     u.set_password('dev')
#     db_session.add(u)
#     db_session.commit()
#     flash('Admin account created')
#     return redirect(url_for('index'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized():
    return abort(403)

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(429)
def too_many_requests(e):
    return render_template('429.html'), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
