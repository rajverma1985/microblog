import flask_babel
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db
from app.forms import (LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm,
                       ResetPasswordRequestForm, ResetPasswordForm)
from app.models import User, Post
from urllib import parse
from datetime import datetime
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        # VERY IMP: To avoid sending the same POST request again when someone hits a refresh button in the browser we
        # send a redirect at the end of the POST, so that last request is GET for the index page.
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    # The below gives all posts by the current user and the posts of the user that this user follows.
    posts = current_user.followed_posts().paginate(page=page,
                                                   per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_p = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_p = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', form=form, posts=posts.items, next=next_p, prev=prev_p)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    # The below gives all posts by all users
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page,
                                                                per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_p = url_for('explore', page=posts.next_num) if posts.has_next else None
    prev_p = url_for('explore', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next=next_p, prev=prev_p)


@app.route('/about')
def about_us():
    return render_template('about.html', title='About Us')


# for deleting a user you can always user: User.query.filter_by(id=1).delete() e.g
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid ID or password provided please check the password again!!")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # To determine if the URL is relative or absolute, We parse it with Werkzeug's url_parse() function and
        # then check if the netloc component is set or not.
        if not next_page or parse.urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for password reset instructions")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title="Reset Password", form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user_profile(username):
    form = EmptyForm()
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page=page,
                                                                per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_p = url_for('user_profile', username=user.username, page=posts.next_num) if posts.has_next else None
    prev_p = url_for('user_profile', username=user.username, page=posts.prev_num) if posts.has_prev else None
    return render_template('profile.html', user=user, posts=posts, form=form, next=next_p, prev=prev_p)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Profile successfully updated!")
        return redirect(url_for('user_profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('profile_editor.html', form=form)


@app.route('/follow/<username>', methods=['POST'])
def follow_user(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("User {} not found".format(username))
            return redirect(url_for('index'))
        elif user == current_user:
            flash("Nice try, You cannot follow yourself!")
        current_user.follow(user)
        db.session.commit()
        flash("You are now following {}".format(username))
        return redirect(url_for('user_profile', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
def unfollow_user(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("User {} not found".format(username))
            return redirect(url_for('index'))
        elif user == current_user:
            flash("Nice try, You cannot follow yourself!")
        current_user.unfollow(user)
        db.session.commit()
        flash("You have un-followed {}".format(username))
        return redirect(url_for('user_profile', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
