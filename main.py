# type: ignore
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, ValidationError
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from functools import wraps
from flask import session, jsonify
from flask import session, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 
import random, string
import json

# Load config
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = params['secret_key']


# Mail setup
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail_user'],
    MAIL_PASSWORD=params['gmail_password']
)
mail = Mail(app)

# MongoDB setup
app.config["MONGO_URI"] = params["mongo_uri"]
mongo = PyMongo(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader
@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user) if user else None

# Flask-Login User class
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.password = user_data['password']

# Forms
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    mobile_no = StringField('Mobile No', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    academic_branch = StringField('Branch', validators=[InputRequired()])
    academic_year = IntegerField('Year', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if mongo.db.users.find_one({'username': username.data}):
            raise ValidationError('Username already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    captcha = StringField('Enter CAPTCHA', validators=[InputRequired()])
    submit = SubmitField('Login')

# CAPTCHA generator
def generate_captcha(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' or not form.validate_on_submit():
        session['captcha_text'] = generate_captcha()

    if form.validate_on_submit():
        if form.captcha.data != session.get('captcha_text'):
            flash('Incorrect CAPTCHA.', 'danger')
            session['captcha_text'] = generate_captcha()
            return render_template('login.html', form=form, captcha=session['captcha_text'])

        user_data = mongo.db.users.find_one({'username': form.username.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            login_user(User(user_data))
            session.pop('captcha_text', None)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
            session['captcha_text'] = generate_captcha()

    return render_template('login.html', form=form, captcha=session['captcha_text'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = {
            "name": form.name.data,
            "username": form.username.data,
            "password": hashed_password,
            "address": form.address.data,
            "mobile_no": form.mobile_no.data,
            "email": form.email.data,
            "academic_branch": form.academic_branch.data,
            "academic_year": form.academic_year.data,
            "gender": form.gender.data
        }
        mongo.db.users.insert_one(new_user)
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        feedback_text = request.form['feedback']
        email = request.form['email']
        suggestion = request.form.get('suggestion', '')

        if not name or not feedback_text or not email:
            return render_template('feedback.html', params=params, error="Fill all fields.")

        mongo.db.feedback.insert_one({
            "name": name,
            "feedback": feedback_text,
            "email": email,
            "suggestion": suggestion
        })

        mail.send_message(
            'New Feedback from MessTrack',
            sender=email,
            recipients=[params['gmail_user']],
            body=f"Feedback from {name}:\n\n{feedback_text}\n\nSuggestion: {suggestion}\nEmail: {email}"
        )
        return render_template('thankyou.html', params=params, success=1)

    return render_template('feedback.html', params=params)

@app.route("/contact", methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        query = request.form['query']

        if not name or not email or not query:
            return render_template('contact.html', params=params, error="Fill all fields.")

        mongo.db.contact.insert_one({
            "name": name,
            "email": email,
            "query": query
        })

        mail.send_message(
            'New Query from MessTrack',
            sender=email,
            recipients=[params['gmail_user']],
            body=f"Query from {name}:\n\n{query}\n\nEmail: {email}"
        )
        return render_template('thankyou.html', params=params, success=2)

    return render_template('contact.html', params=params)

@app.route("/thankyou")
@login_required
def thankyou():
    return render_template("thankyou.html")

@app.route('/timetable')
def timetable():
    return render_template('timetable.html')

@app.route('/attendance')
def attendence():
    return render_template('attendance.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/leave')
def leave_messtrack():
    return render_template('leave.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))







#Admin
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'GET':
        # Generate and store a new CAPTCHA in session for GET requests (login form load)
        session['captcha_text'] = generate_captcha()
        return render_template("adminlogin.html", captcha=session['captcha_text'])

    # POST request handling (form submission)
    email = request.form['email']
    password = request.form['password']
    captcha_input = request.form.get('captcha', '').strip()

    # Check CAPTCHA first
    if captcha_input.upper() != session.get('captcha_text', '').upper():
        flash("Incorrect CAPTCHA.", "danger")
        session['captcha_text'] = generate_captcha()  # Regenerate CAPTCHA on failure
        return render_template("adminlogin.html", captcha=session['captcha_text'])

    # CAPTCHA correct, check admin credentials
    admin = mongo.db.adminlogin.find_one({"email": email})
    if admin and check_password_hash(admin['password'], password):
        session.clear()  # Clear previous session data
        session['admin_logged_in'] = True
        session['admin_email'] = email
        return redirect(url_for('adminindex'))
    else:
        flash("Invalid email or password", "danger")
        session['captcha_text'] = generate_captcha()  # Regenerate CAPTCHA on failure
        return render_template("adminlogin.html", captcha=session['captcha_text'])


@app.route('/refresh_captcha')
def refresh_captcha():
    new_captcha = generate_captcha()
    session['captcha_text'] = new_captcha
    return new_captcha



def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash("Admin login required", "warning")
            return redirect(url_for('adminlogin'))
        return f(*args, **kwargs)
    return decorated_function




@app.route('/adminindex')
@admin_login_required
def adminindex():
    return render_template('adminindex.html')


@app.route('/adminlogout')
def adminlogout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    flash("Logged out successfully", "success")
    return redirect(url_for('adminlogin'))



if __name__ == "__main__":
    app.run(debug=True)
