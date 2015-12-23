import mistune
from flask import request, redirect, url_for

from flask import render_template
from blog import app
from .database import session
from .models import Post
from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .models import User
from flask.ext.login import login_required
from flask.ext.login import current_user
from flask.ext.login import logout_user
from flask import make_response 


#from flask import redirect, url_for, render_template

#from . import app
#from .forms import EmailForm
#from .models import User
#from .util import send_email, ts

#from flask import redirect, url_for, render_template

#from . import app, db
#from .forms import PasswordForm
#from .models import User
#from .util import ts
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))

@app.route('/logout')
def logout():
#    session.pop('logged_in', None)
    logout_user()
    flash('You were logged out')
    return redirect(url_for('login_get'))

#def logout_user
#flask.ext.login.logout_user()

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title = request.form["title"],
        content = mistune.markdown(request.form["content"]),
        author = current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("add_post_get"))

@app.route('/reset-password', methods=('GET', 'POST',))
def forgot_password():
    token = request.args.get('token',None)
    form = ResetPassword(request.form) #form
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_token()
            print token
    return render_template('users/reset.html', form=form)

@app.route('/send-mail/')
def send_mail():
	try:
		msg = Message("Send Mail Tutorial!",
		  sender="yoursendingemail@gmail.com",
		  recipients=["recievingemail@email.com"])
		msg.body = "Yo!\nHave you heard the good word of Python???"           
		mail.send(msg)
		return 'Mail sent!'
	except Exception, e:
		return(str(e)) 


@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()

        user.password = form.password.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('signin'))

    return render_template('reset_with_token.html', form=form, token=token)

@app.route("/docs/<id>")
def get_resume():
    if id is not None:
        binary_pdf = get_binary_pdf_data_from_database(id=id)
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'resume_12_15_15.pdf'
            
        return response