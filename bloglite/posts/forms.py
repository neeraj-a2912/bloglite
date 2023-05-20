from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    caption=StringField("Title",validators=[DataRequired()])
    content=TextAreaField('Description')
    picture=FileField('Add Photos', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit=SubmitField("Post")

class DeletePostForm(FlaskForm):
    submit=SubmitField()