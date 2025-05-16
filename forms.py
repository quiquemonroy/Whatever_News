from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()],render_kw={"placeholder": "nombre"})
    email = EmailField(label="Email", validators=[DataRequired()],render_kw={"placeholder": "email"})
    password = PasswordField(label="Password", validators=[DataRequired()],render_kw={"placeholder": "password"})
    password_confirm = PasswordField(label="Confirm Password", validators=[DataRequired()],render_kw={"placeholder": "confirma password"})
    submit = SubmitField(label="REGISTRARSE")


class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired()],render_kw={"placeholder": "email"})
    password = PasswordField(label="Password", validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit = SubmitField(label="LOGIN")


class CommentForm(FlaskForm):
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField(label="Comment")


class EditUser(FlaskForm):
    new_name = StringField(label="Name")
    old_password = PasswordField(label="Actual Password", validators=[DataRequired()])
    new_password = PasswordField(label="New Password")
    new_password_again = PasswordField(label="Repite Password")
    submit = SubmitField(label="Submit")
