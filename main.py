from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

with app.app_context():
    db.drop_all
    db.create_all


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


if __name__ == '__main__':
    app.run()
