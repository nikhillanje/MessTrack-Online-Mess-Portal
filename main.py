# type: ignore
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, ValidationError
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_mail import Mail
from datetime import datetime, timedelta
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
attendance_col = mongo.db.attendance

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



#--------------------------------------------------------------------------------------------------#
# Students
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
            form.captcha.data = ''
            return render_template('login.html', form=form, captcha=session['captcha_text'])

        user_data = mongo.db.users.find_one({'username': form.username.data})
        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            login_user(User(user_data))
            session['_id'] = str(user_data['_id'])
            session['username'] = user_data['username']
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
    timetable_collection = mongo.db.timetable

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    timetable = list(timetable_collection.find())

    # If empty, initialize with default NULL values
    if not timetable:
        timetable = [{"day": day, "breakfast": "NULL", "lunch": "NULL", "dinner": "NULL"} for day in days]

    # Sort timetable by day order
    day_order = {day: i for i, day in enumerate(days)}
    timetable.sort(key=lambda x: day_order.get(x.get("day", ""), 100))

    return render_template('timetable.html', timetable=timetable)


# Render attendance page
@app.route('/attendance')
def attendance():
    if '_id' not in session:
        return redirect('/login')

    student_id = session['_id']
    today = datetime.utcnow().date().strftime("%Y-%m-%d")

    # Check if this student has marked attendance today
    record = attendance_col.find_one({
        "student_id": student_id,
        "date": today,
        "present": "yes"
    })

    attendance_status = "yes" if record else None

    return render_template('attendance.html', attendance_status=attendance_status, today_date=today)


@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    try:
        if '_id' not in session:
            print("User not in session")
            return jsonify({'status': 'unauthorized'}), 401

        data = request.get_json()
        print("Received data:", data)  # DEBUG LINE

        if not data or 'date' not in data:
            return jsonify({'status': 'error', 'message': 'Missing date'}), 400

        date = data['date']
        student_id = session['_id']
        student_username = session.get('username', 'unknown')  # safer access

        existing = attendance_col.find_one({"date": date, "student_id": student_id})
        if existing:
            print("Attendance already marked for", student_id, "on", date)
            return jsonify({'status': 'already_marked'})

        result = attendance_col.insert_one({
            "student_id": student_id,
            "student_username": student_username,
            "date": date,
            "present": "yes",
            "timestamp": datetime.utcnow()
        })

        print("Inserted attendance with ID:", result.inserted_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error in mark_attendance:", str(e))  # DEBUG LINE
        return jsonify({'status': 'error', 'message': str(e)}), 500







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






#-------------------------------------------------------------------------------------------#
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
    return redirect(url_for('home'))





timetable_collection = mongo.db.timetable
@app.route('/admintimetable', methods=['GET', 'POST'])
def admintimetable():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    if request.method == 'POST':
        for i, day in enumerate(days):
            updated = {
                "day": day,
                "breakfast": request.form.get(f"breakfast_{i}", ""),
                "breakfast_time": request.form.get(f"breakfast_time_{i}", ""),
                "lunch": request.form.get(f"lunch_{i}", ""),
                "lunch_time": request.form.get(f"lunch_time_{i}", ""),
                "dinner": request.form.get(f"dinner_{i}", ""),
                "dinner_time": request.form.get(f"dinner_time_{i}", "")
            }
            timetable_collection.update_one({"day": day}, {"$set": updated}, upsert=True)
        return redirect('/adminindex')

    # Fetch or initialize if empty
    timetable = list(timetable_collection.find())
    if not timetable:
        timetable = [{"day": day, "breakfast": "", "breakfast_time": "", 
                      "lunch": "", "lunch_time": "", 
                      "dinner": "", "dinner_time": ""} for day in days]

    return render_template('admintimetable.html', timetable=timetable)


@app.route('/adminfeedback')
def adminfeedback():
    feedback_data = list(mongo.db.feedback.find({}, {"_id": 0}))
    return render_template("adminfeedback.html", feedbacks=feedback_data)

@app.route("/admincontact")
def admincontact():
    contact_data = list(mongo.db.contact.find({}, {"_id": 0}))
    return render_template("admincontact.html", contacts=contact_data)

@app.route('/adminallusers')
def adminallusers():
    users = mongo.db.users.find()
    return render_template('adminallusers.html', users=users)



if __name__ == "__main__":
    app.run(debug=True)
