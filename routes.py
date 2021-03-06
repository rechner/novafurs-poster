#!/usr/bin/env python

import config

import os
os.chdir(os.path.dirname(config.__file__)) #Override wsgi directory change

from functools import wraps
import bcrypt
import sqlite3
from flask import Flask, render_template, g, session, request, redirect, url_for, flash
from flask import get_flashed_messages
#import tweetpony

# Fields will look something like this:
#
# Subject:
# Message (Long description):
# Short description:
#
# Checkboxes for which sites we'll post to
# Checkboxes to email newsletter

# Long message accepts input formatted with weasyl-flavour markdown, since
# it seems to be the most encompassing.  Rendered to HTML for email,
# parsed to FA's bb-code-ish markup if possible.

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

#Login decorator:
def login_required(original_function):
    @wraps(original_function)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None or session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return original_function(*args, **kwargs)
    return decorated_function

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g.database = connect_db()
    return g.database

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        subject = request.form.get('subject', '')
        summary = request.form.get('summary', '')
        message = request.form.get('message', '') # Raw markdown
        markup = request.form.get('markup', '') # The rendered output
        post_to = request.form.getlist('post-to')

        # Validate the form
        if subject == '':
            flash("The 'subject' field is required", "error")
        if summary == '':
            summary = subject
        if message == '':
            flash("Empty bodies are not allowed. Enter some content!", "error")
        if markup == '':
            flash("There was a problem fetching the message markup", "error")
        if len(post_to) == 0:
            flash("Please select at least one platform to post to", "error")

        if get_flashed_messages(category_filter='error'):
            return render_template('new_post.html', form=request.form)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""INSERT INTO posts(owner, subject, summary, message,
                   markup, timestamp) VALUES (?,?,?,?,?, strftime('%Y-%m-%dT%H:%M:%SZ'));""",
                   (session['user']['id'], subject, summary, message,
                    markup))
        if 'furaffinity' in post_to:
            cursor.execute("UPDATE posts SET link_furaffinity = 'pending' WHERE id = ?", (id,))
        if 'weasyl' in post_to:
            cursor.execute("UPDATE posts SET link_weasyl = 'pending' WHERE id = ?", (id,))
        if 'twitter' in post_to:
            cursor.execute("UPDATE posts SET link_twitter = 'pending' WHERE id = ?", (id,))
        db.commit()

        flash("Successfully saved post {0}.".format(cursor.lastrowid), "success")
        return redirect(url_for('review', id=cursor.lastrowid))

    return render_template('new_post.html', form=request.form)

@app.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
def review(id):
    post = query_db('SELECT * FROM posts WHERE id = ?', (id,), one=True)
    if post is None:
        flash("Invalid post ID", "error")
    else:
        post = dict(post)
        post['fa_markup'] = post['message']
    return render_template('review.html', post=post)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash("You were logged out succesfully", "info")
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in') is not None or \
       session.get('user') is not None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

        for user in query_db('SELECT * FROM users'):
            if email == user['email'] and \
               bcrypt.hashpw(password, user['password']) == user['password']:
                session['logged_in'] = True
                session['user'] = dict(user)
                return redirect(url_for('index'))

            else:
                flash("Username or password is incorrect", "error")

    return render_template('login.html')

if __name__ == "__main__":
    #~ app.run(host='0.0.0.0')
    app.run()
