from datetime import date
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import os
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm,EditUser
from send_email import send_email

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("API_KEY")
ckeditor = CKEditor(app)
Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # author: Mapped[str] = mapped_column(String(250), nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment", back_populates="parent_post")


class Comment(db.Model):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    post_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)

    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")


with app.app_context():
    db.create_all()


def get_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    posts.reverse()
    return posts


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name_check = db.session.execute(db.select(User).where(User.name == form.name.data)).scalars().all()
        if name_check:
            flash("elige otro nombre, por favor.")
            return redirect(url_for("register"))
        if form.password.data != form.password_confirm.data:
            flash("Las contraseñas no coinciden")
            return redirect(url_for("register"))
        result = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().all()
        if result:
            flash("You where already registered, please log in.")
            return redirect(url_for("login"))
        else:
            new_user = User(name=form.name.data,
                            email=form.email.data,
                            password=generate_password_hash(form.password.data, method="pbkdf2:sha256:600000",
                                                            salt_length=8)
                            )
            db.session.add(new_user)
            db.session.commit()
            flash("Successfully Registered!")
            return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data)).scalars().all()
        if result:
            user_to_validate = result[0]
            if check_password_hash(user_to_validate.password, form.password.data):
                print("yeah!")
                login_user(user_to_validate)
                return redirect(url_for("get_all_posts"))
            else:
                print("nope")
        #     TODO: Terminar de capturar los errores cuando la contraseña está mal
        flash("try again!")
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=get_posts())


@app.route("/post/<int:post_id>", methods=["POST", "GET"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(body=form.body.data,
                              comment_author=current_user,
                              post_id=post_id
                              )
        db.session.add(new_comment)
        db.session.commit()
        print("post added")
    comments = db.session.execute(db.select(Comment).where(Comment.post_id == post_id)).scalars().all()
    return render_template("post.html", post=requested_post, form=form, comments=comments)


@app.route("/new-post", methods=["GET", "POST"])
@login_required
def add_new_post():
    if current_user.id == 1:
        form = CreatePostForm()
        if form.validate_on_submit():
            new_post = BlogPost(
                title=form.title.data,
                subtitle=form.subtitle.data,
                body=form.body.data,
                img_url=form.img_url.data,
                author=current_user,
                date=date.today().strftime("%B %d, %Y")
            )
            print(new_post.author)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("get_all_posts"))
        return render_template("make-post.html", form=form)
    return redirect(url_for("get_all_posts"))


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):
    if current_user.id == 1:
        post_to_delete = db.get_or_404(BlogPost, post_id)
        db.session.delete(post_to_delete)
        db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        send_email(text=request.form.get("message"), user=request.form.get("name"), remitent=request.form.get("email"))
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html")


@app.route("/control-panel")
@login_required
def control_panel():
    if current_user.id == 1:
        users = db.session.execute(db.select(User)).scalars().all()
        return render_template("control-panel.html", all_posts=get_posts(), users=users)
    return redirect(url_for('get_all_posts'))

@app.route("/user/<user_id>", methods=["GET","POST"])
@login_required
def user_data(user_id):
    print(current_user.id)
    if current_user.id == 1 or current_user.id == int(user_id):
        user = db.get_or_404(User,user_id)
        form = EditUser()
        if form.validate_on_submit():
            if check_password_hash(user.password, form.old_password.data):
                if form.new_password.data == form.new_password_again.data:
                    user.password = generate_password_hash(form.new_password.data, method="pbkdf2:sha256:600000",
                                                            salt_length=8)
                    db.session.commit()
                    flash("Datos actualizados")
        # TODO: terminar de capturar los errores de cambiar la contrseña
        # TODO: Terminar el cmabio de nombre


        return render_template("profile.html", user=user, form=form)
    return "culo"#redirect(url_for('get_all_posts'))

if __name__ == "__main__":
    app.run(debug=False, port=8080, host="0.0.0.0")
