import os
import secrets
from bloglite import app
from bloglite.models import Post, User


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    file_name,file_ext=os.path.splitext(form_picture.filename)
    picture_filename=random_hex+file_ext
    picture_path=os.path.join(app.root_path, 'static/images', picture_filename)
    form_picture.save(picture_path)
    return picture_filename

def post_count(user):
    p_count=Post.query.filter_by(user_id=user.id).count()
    return p_count

def following(username):
    p_user=User.query.filter_by(name=username).first()
    following_users=[]
    for user in User.query.all():
        if p_user.is_following(user):
            following_users.append(user)
    return following_users
