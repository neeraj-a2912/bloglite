from flask import Blueprint
from flask import render_template
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route("/home",methods=['GET','POST'])
@login_required
def home():
    posts = current_user.followed_posts().all()
    return render_template('home.html',posts=posts,title="Bloglite - Home")