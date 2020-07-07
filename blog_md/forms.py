from blog_md import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class AddBook(FlaskForm):
    year_read = StringField('Year Read', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year_published = StringField('Year Published', validators=[DataRequired()])
    no_pages = StringField('Number of Pages', validators=[DataRequired()])
    submit = SubmitField('Add to booklist')
    cancel = SubmitField('Cancel')

class EditBook(FlaskForm):
    id = StringField('id', render_kw={'readonly': True})
    year_read = StringField('Year Read', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year_published = StringField('Year Published', validators=[DataRequired()])
    no_pages = StringField('Number of Pages', validators=[DataRequired()])
    submit = SubmitField('Edit booklist entry')
    cancel = SubmitField('Cancel')

class DeleteBook(FlaskForm):
    id = StringField('id', render_kw={'readonly': True})
    year_read = StringField('Year Read', render_kw={'readonly': True})
    title = StringField('Title', render_kw={'readonly': True})
    author = StringField('Author', render_kw={'readonly': True})
    year_published = StringField('Year Published', render_kw={'readonly': True})
    no_pages = StringField('Number of Pages', render_kw={'readonly': True})
    submit = SubmitField('Delete booklist entry')
    cancel = SubmitField('Cancel')

class UploadPost(FlaskForm):
    file = FileField('md Text file', validators=[FileRequired(),FileAllowed(['md'],'Only .md files are allowed!')])
    media_file1 = FileField('Media file', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Only jpg/png/gif files are allowed!')])
    media_file2 = FileField('Media file', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Only jpg/png/gif files are allowed!')])
    media_file3 = FileField('Media file', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Only jpg/png/gif files are allowed!')])
    media_file4 = FileField('Media file', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Only jpg/png/gif files are allowed!')])
    media_file5 = FileField('Media file', validators=[FileAllowed(['jpg', 'png', 'gif'], 'Only jpg/png/gif files are allowed!')])
    submit = SubmitField('Upload File(s)')
    cancel = SubmitField('Cancel')

class UploadNews(FlaskForm):
    text_file = FileField('Text file', validators=[FileRequired(),FileAllowed(['txt'],'Only .txt files are allowed!')])
    image_file = FileField('Image file', validators=[FileRequired(),FileAllowed(['jpg','png'],'Only image files are allowed!')])
    submit = SubmitField('Upload Files')
    cancel = SubmitField('Cancel')