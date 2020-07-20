from datetime import datetime
from flask import Flask , render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


# "Import flask and render template ,
app = Flask(__name__)# app is a flask variable whihc is set to an instance ,Add flask variable,
app.config['SECRET_KEY'] = 'f4d64e66de7a5102a52fd22dcd9e08a0'
app.config['sQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.model):
     id = db.Column(db.Interger, primary_key=True)
     username = db.Column(db.String(20), unique=True, nullable=False)
     username = db.Column(db.String(120), unique=True, nullable=False)
     image_file = db.Column(db.Sring(20), nullable=False, default='default.jpg' )
     password = db.Column(db.Sring(60), nullable=False)

     def __repr__(self):
         return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.model):
     id = db.Column(db.Interger, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     date_posted = db.Column(db.DateTime, nullable=False, )

#  Add dictionary which represents a single blog post"
posts = [
    {
        'author': 'Virginiah Wamuyu',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'June 16 , 2020'
    },
    {
        'author': 'Cecilia CC',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'June 1 , 2020'
    }
]


#  Add an app route for the home and about page ,
@app.route("/")
@app.route("/home")
def home():
    return render_template ('home.html', posts = posts)


@app.route("/about")
def about():
    return render_template ('about.html', title = 'About')



@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'passwprd':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unseccessful. Please check your username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


if __name__ == '__main__':
    app.run(debug = True)