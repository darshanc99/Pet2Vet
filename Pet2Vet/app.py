#Importing Dependencies
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os.path
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import ForeignKey
import sqlite3 as sql

#Initials
app = Flask(__name__)

#Configuration for the app
app.config['SECRET_KEY'] = 'secret'
db_path = os.path.join(os.path.dirname(__file__),'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
Bootstrap(app)
db = SQLAlchemy(app)

#Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Defining the tables
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#The Forms
class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4,max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class Donate(FlaskForm):
    name = StringField('name',validators=[InputRequired(),Length(max=50)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    phone = StringField('phone', validators=[InputRequired(), Length(max=10)])
    address = StringField('address', validators=[InputRequired(), Length(max=100)])

#Login - Backend
@app.route('/', methods=['GET', 'POST'])
def login():
    options = [
        {"name":"Login","selected":True,"link":url_for("login")},
        {"name":"Signup","selected":False,"link":url_for("signup")},
    ]
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            login_user(user, remember=form.remember.data)
            if check_password_hash(user.password, form.password.data):
                #return redirect(url_for('welcome'))
                #return render_template('feed.html')
                return redirect(url_for('welcome'))

    return render_template('login.html',form = form, nav_options = options)


#SignUp - Backend
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    options = [
        {"name":"Signup","selected":True,"link":url_for("signup")},
        {"name":"Login","selected":False,"link":url_for("login")},
    ]
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        if User.query.filter_by(username=form.username.data).first() == form.username.data:
            flash("Username already exits!")
        # else:
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
        #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form, nav_options = options)

@app.route('/donate/',methods = ['GET','POST'])
@login_required
def donate():
    form = Donate()
    if form.validate_on_submit():
        new_donation = Donation(name=form.name.data, email=form.email.data, phone=form.phone.data, address=form.address.data)
        db.session.add(new_donation)
        db.session.commit()
    return render_template('donate.html', form=form)

#LogOut - Backend
@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))

@app.route('/welcome/')
@login_required
def welcome():
    options = [
        {"name":"Welcome","selected":True,"link":url_for("welcome")},
        {"name": "Logout", "selected": False, "link": url_for("signup")},
    ]
    return render_template('tp.html',nav_options = options)


@app.route('/about/')
@login_required
def about():
    return render_template('about.html')

@app.route('/doctors')
@login_required
def doctors():
    return render_template('doctors.html')



@app.route('/ngo/')
@login_required
def ngo():
    return render_template('ngo.html')

@app.route('/contact/')
@login_required
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    db.create_all()
    app.run(debug=True)