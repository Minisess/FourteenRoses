from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, StoryPostForm, CommentForm
from app.models import User, StoryPost, Post


# add @login_required to any function to make it require a login to view
@app.route('/')
def home():
    announcements = StoryPost.query.filter_by(title='Announcments').first().comments
    return render_template('home.html', title='Home', announcements=announcements)





@app.route('/index')
def index():
    posts = StoryPost.query.all()
    for x in posts:
        if x.title == 'Announcments':
            posts.remove(x)
    posts = reversed(posts)
    return render_template("index.html", title='Journal', posts=posts, current_user=current_user,)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        else:
            flash('Login requested for user {}, remember me={}'.format(form.username.data,
                                                                       form.remember_me.data, ))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering!")
        login_user(user)
        redirect(url_for('index'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/about_me')
def about_me():
    return render_template('about_me.html', title='About Me')


@app.route('/story/<title>', methods=['GET', 'Post'])
def story(title):
    form = CommentForm()
    current_story = StoryPost.query.filter_by(title=title).first_or_404()
    comments = reversed(current_story.comments)
    if current_user == User.query.filter_by(username='Katie Brethorst').first():
        current_user.is_admin = True
    else:
        current_user.is_admin = False

    if form.validate_on_submit():
        if current_user.is_authenticated:
            author = current_user
        else:
            author = User.query.filter_by(username='Anonymous').first()
        body = form.body.data
        comment = Post(author=author, body=body, story=current_story)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('story', title=current_story.title))

    # has to be below the first validate or it seems to catch and prevent the other kind of validation_on_submit
    if request.method == 'POST':
        if request.form['delete']:
            db.session.delete(current_story)
            db.session.commit()
            flash(f"{current_story.title} has been deleted.")
            return redirect(url_for('index'))

    return render_template('story.html', title=title, current_story=current_story, form=form, comments=comments,
                           current_user=current_user)


@login_required
@app.route('/submission',  methods=['GET', 'POST'])
def submission():
    if current_user != User.query.filter_by(username='Katie Brethorst').first():
        flash('Sorry, you are not registered to post.')
        return redirect(url_for('index'))
    form = StoryPostForm()
    if form.validate_on_submit():
        edit = StoryPost.query.filter_by(title=form.title.data).first()
        if edit and (current_user == edit.author):
            edit.body = form.body.data
        else:
            post = StoryPost(title=form.title.data, body=form.body.data, author=current_user)
            db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template('submission.html', title='Submission', form=form)


