from flask import (render_template, url_for, flash, redirect,
                    request, abort, Blueprint)
from flask_login import login_user, current_user, logout_user, login_required
from bloglite import db, bcrypt
from bloglite.models import User, Post
from bloglite.users.forms import (RegistrationForm, LoginForm, EditProfileForm, DeleteAccountForm,
                                    FollowForm, SearchForm, )
from bloglite.users.utils import save_picture, post_count, following

users = Blueprint('users', __name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(name=form.username.data,email_address=form.email_address.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created Succesfully. Please Login to Continue','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title='Register',form=form)


@users.route("/", methods=['GET', 'POST'])
@users.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email_address=form.email_address.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check your email and password')
    return render_template('login.html',title='login',form=form)


@users.route("/profile/<username>",methods=['GET','POST'])
@login_required
def user_profile(username):
    user=User.query.filter_by(name=username).first()
    image=url_for('static',filename='images/'+ user.image)
    follow_form=FollowForm()
    del_form=DeleteAccountForm()
    return render_template('userprofile.html',user=user,post_count=post_count(user),
                            follow_form=follow_form, image=image, del_form=del_form)

@users.route("/profile/<username>/editprofile", methods=['GET','POST'])
@login_required
def editprofile(username):
    form=EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image=picture_file
        current_user.name=form.username.data
        current_user.bio=form.bio.data
        current_user.email_address=form.email_address.data
        db.session.commit()
        return redirect(url_for('users.user_profile',username=current_user.name))
    elif request.method == 'GET':
        form.username.data=current_user.name
        form.email_address.data=current_user.email_address
        form.bio.data=current_user.bio
        form.picture.data = current_user.image
    return render_template('editprofile.html',form=form,user=current_user)

@users.route('/delete/<username>', methods=['POST'])
@login_required
def delete_user(username):
    form=DeleteAccountForm()
    if form.validate_on_submit():
        user=User.query.filter_by(name=username).first()
        if user:
            for post in user.posts:
                db.session.delete(post)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('users.login'))

@users.route('/follow/<username>', methods=['GET', 'POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=username).first()
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}')
        return redirect(url_for('users.user_profile', username=username))

@users.route('/unfollow/<username>', methods=['GET', 'POST'])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=username).first()
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are no longer following {username}')
        return redirect(url_for('users.user_profile', username=username))

    
@users.route("/search", methods=['GET','POST'])
@login_required
def search():
    form=SearchForm()
    if form.validate_on_submit():
        input=form.usertosearch.data
        users=User.query.filter(User.name.like('%'+input+'%'))
        return render_template('search.html',form=form, users=users, input=input)
    else:
        return render_template('search.html',form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route("/<username>/followers", methods=['GET', 'POST'])
@login_required
def user_followers(username):
    user=User.query.filter_by(name=username).first()
    return render_template('followers.html', user=user)

@users.route("/<username>/following", methods=['GET', 'POST'])
@login_required
def user_following(username):
    user=User.query.filter_by(name=username).first()
    followed_users=following(user.name)
    print(followed_users)
    return render_template('following.html', user=user, followed_users=followed_users)