import os
from flask import Flask, render_template,request, session, redirect, url_for # type: ignore
from sqlalchemy import Column, Integer, String , DateTime # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime
from werkzeug.utils import secure_filename
import json
import os
from flask_mail import Mail # type: ignore
import os
import math


config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as c:
    params = json.load(c)["params"]

local_server = True #variable for config file

app = Flask(__name__)

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
def index():
    return render_template("index.html")






@app.route("/feedback", methods=['GET', 'POST'])
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