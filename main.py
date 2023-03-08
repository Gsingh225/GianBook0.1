from flask import Flask, session, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String(40), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    user = db.Column(db.String(40), nullable=False)

with app.app_context():
    db.drop_all()
    db.create_all()
    titles = [
        "Exploring the Rocky Mountains",
        "Trying new recipes in the kitchen",
        "Learning to play guitar",
        "Visiting museums in Paris",
        "Welcome to GianBook"
    ]
    bod = [
        "The mountains where cool nay epic.",
        "the recipient where very recipie like",
        "My hands hurt :(",
        "I think i destroyed a 121 million painting...",
        "Feel free to have fun"
    ]
    users = [
        "Mountain",
        "FoodEater",
        "Future_Musician",
        "Traveler",
        "GianBook"
    ]
    for i in range(5):
        title = titles[i]
        text = bod[i]
        user = users[i]
        post = Post(title=title, text=text, user=user)
        db.session.add(post)
        db.session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['newuser']
        password = request.form['newpass']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return f'Your username is "{username}", and password is "{password}. Account created successfully. Please return to the homepage to login!"'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', err="")
    elif request.method == 'POST':
        username = request.form['user']
        password = request.form['pas']
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            session['username'] = username
            session['password'] = password
            return redirect(url_for('account'))
        else:
            return render_template('login.html', err='Invalid Username or Password')


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        username = session.get('username')
        password = session.get('password')
        postz = Post.query.order_by(func.random()).limit(5).all()
        posts = []
        for post in postz:
            dic = {
                "title": post.title,
                "user": post.user,
                "text": post.text
            }
            posts.append(dic)
        return render_template('account.html', username=username, posts=posts)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body-text']
        username = session.get('username')
        post = Post(title=title, text=body, user=username)
        db.session.add(post)
        db.session.commit()
        postz = Post.query.order_by(func.random()).limit(5).all()
        posts = [{"title": title, "user": username, "text": body}]
        for post in postz:
            dic = {
                "title": post.title,
                "user": post.user,
                "text": post.text
            }
            posts.append(dic)
        return render_template('account.html', username=username)


if __name__ == '__main__':
    app.run()
