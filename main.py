
from flask import Flask, render_template, request, session, redirect, url_for, flash  # type: ignore
from sqlalchemy import Column, Integer, String, DateTime  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required  # type: ignore
from flask_wtf import FlaskForm  # type: ignore
from wtforms import StringField, PasswordField, SubmitField  # type: ignore
from wtforms.validators import InputRequired, Length, ValidationError  # type: ignore
from wtforms import StringField, PasswordField, SubmitField, IntegerField  # type: ignore
from wtforms.validators import InputRequired, Length, ValidationError, Email  # type: ignore
from flask_mail import Mail  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import random, string
import json  # type: ignore
import os  # type: ignore



config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as c:
    params = json.load(c)["params"]

local_server = True #variable for config file

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key ='super-secret-key' #for log in we need this 
#for send gmail
app.config.update(         
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params['gmail_password']
)
mail = Mail(app)

if(local_server) :
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else :
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']


db = SQLAlchemy(app)

login_manager = LoginManager() # type: ignore
login_manager.init_app(app)
login_manager.login_view = 'login'


 
class User(db.Model, UserMixin):
    __tablename__ = 'login'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))  # <-- Add this line
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    mobile_no = db.Column(db.String(15))  # match form field
    email = db.Column(db.String(120), unique=True)
    academic_branch = db.Column(db.String(100))
    academic_year = db.Column(db.Integer)
    gender = db.Column(db.String(10), nullable=False)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password', validators=[InputRequired()])
    address = StringField('Address', validators=[InputRequired()])
    mobile_no = StringField('Mobile Number', validators=[InputRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    academic_branch = StringField('Academic Branch', validators=[InputRequired()])
    academic_year = IntegerField('Academic Year', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=20)])
    captcha = StringField('Enter CAPTCHA', validators=[DataRequired()])
    submit = SubmitField('Login')




class Feedback(db.Model):
    __tablename__ = 'feedback'
    srn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    suggestion = db.Column(db.String(50), nullable=True)


class Contact(db.Model):
    __tablename__ = 'contact'
    srn = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    query = db.Column(db.String(50), nullable=False)










@app.route("/")
def home():
    return render_template("home.html")







def generate_captcha(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Always generate new captcha on GET (or failed POST)
    if request.method == 'GET' or not form.validate_on_submit():
        session['captcha_text'] = generate_captcha()

    if form.validate_on_submit():
        if form.captcha.data != session.get('captcha_text'):
            flash('Incorrect CAPTCHA. Please try again.', 'danger')
            session['captcha_text'] = generate_captcha()  # regenerate after wrong input
            return render_template('login.html', form=form, captcha=session['captcha_text'])

        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
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
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            password=hashed_password,
            address=form.address.data,
            mobile_no=form.mobile_no.data,
            email=form.email.data,
            academic_branch=form.academic_branch.data,
            academic_year=form.academic_year.data,
            gender = form.gender.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)




@app.route('/index')
@login_required # type: ignore
def index():
    return render_template('index.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))






@app.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        # Safe get with default values
        name = request.form.get('name', '').strip()
        feedback = request.form.get('feedback', '').strip()
        email = request.form.get('email', '').strip()
        suggestion = request.form.get('suggestion', '').strip()

        # Validation: required fields
        if not name or not feedback or not email:
            return render_template('feedback.html', params=params, error="Please fill in all required fields.")

        try:
            # Save to database
            entry = Feedback(name=name, feedback=feedback, email=email, suggestion=suggestion)
            db.session.add(entry)
            db.session.commit()

            # Send email
            mail.send_message(
                'New Feedback from MessTrack',
                sender=email,
                recipients=[params['gmail_user']],
                body=f"Feedback From Mr: {name}\nFeedback: {feedback}\nSuggestion: {suggestion}\nEmail Of Mr {name} Is : {email}"
            )

            return render_template('thankyou.html', params=params , success=1)

        except Exception as e:
            db.session.rollback()
            return render_template('feedback.html', params=params, error="Something went wrong. Please try again.")
    
    return render_template('feedback.html', params=params)






@app.route("/contact", methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        query = request.form.get('query', '').strip()   # In HTML we Want to Write <textarea id="query" name="query" rows="6" required></textarea>

        if not name or not email or not query:
            return render_template('contact.html', params=params, error="Please fill in all required fields.")

        try:
            # Save to DB
            entry = Contact(name=name, email=email, query=query)
            db.session.add(entry)
            db.session.commit()

            # Send Email
            mail.send_message(
                'New Query from MessTrack',
                sender=email,
                recipients=[params['gmail_user']],
                body=f"Query From Mr: {name}\nQuery Is: {query}\nEmail of Mr {name}: {email}"
            )

            return render_template('thankyou.html', params=params , success=2)

        except Exception as e:
            db.session.rollback()
            print("Error in /contact:", e)
            return render_template('contact.html', params=params, error="Something went wrong. Please try again.")

    return render_template('contact.html', params=params)







@app.route("/thankyou" , methods=['POST'])
@login_required
def thankyou():
    return render_template("thankyou.html")









@app.route('/timetable')
def timetable():
    return render_template('timetable.html')

@app.route('/attendence')
def attendence():
    return render_template('attendence.html')

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/monthly_billing')
def monthly_billing():
    return render_template('monthly_billing.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/leave_messtrack')
def leave_messtrack():
    return render_template('leave_messtrack.html')

if __name__ == "__main__":
    app.run(debug=True)