from flask import (render_template, url_for, flash, redirect,
                    request, abort, Blueprint)
from flask_login import current_user, login_required
from bloglite import db
from bloglite.models import Post
from bloglite.posts.forms import PostForm, DeletePostForm
from bloglite.users.utils import save_picture

posts = Blueprint('posts', __name__)


@posts.route("/addpost",methods=['GET','POST'])
@login_required
def addpost():
    form=PostForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            filename=save_picture(form.picture.data)
            new_post=Post(caption=form.caption.data, user_id=current_user.id, content=form.content.data, img_post=filename)
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('users.user_profile', username=current_user.name))
    return render_template('addpost.html',form=form)

@posts.route("/post/<int:post_id>")
def post(post_id):
    post=Post.query.get(post_id)
    form=DeletePostForm()
    return render_template('post.html', post=post, title = post.caption, form=form)

@posts.route("/post/<int:post_id>/edit", methods = ['GET', 'POST'])
@login_required
def editpost(post_id):
    post=Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.caption=form.caption.data
        if form.content.data:
            post.content=form.content.data
        if form.picture.data:
            filename=save_picture(form.picture.data)
            post.img_post=filename
        db.session.commit()
        return redirect(url_for('users.user_profile', username=current_user.name))
    elif request.method == 'GET':
        form.caption.data = post.caption
        if form.content.data:
            form.content.data=post.content
        if form.picture.data:
            form.picture.data = post.img_post
    return render_template('addpost.html', form=form)

@posts.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    form=DeletePostForm()
    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()
    flash('Post Deleted Successfully!')
    return redirect(url_for('users.user_profile', username=current_user.name))