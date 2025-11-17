from flask import Flask, request, render_template, redirect, url_for
#import requests # Included as requested, though currently unused
import datetime
import random
#from bs4 import BeautifulSoup # Included as requested, though currently unused
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#load environment variables from a .env file if present
load_dotenv()


app = Flask(__name__)

#-----Database Configuration -------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable a deprecation warning

db=SQLAlchemy(app)

#Initialize the login manager
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login' #tells flask-login which view to redirect to for login

#---Database Class model----
class User(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    age=db.Column(db.Integer,nullable=False)
    password=db.Column(db.String(100), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name} ({self.age})>'
    
@login_manager.user_loader
def load_user(user_id):
    # This function must return the User object based on the user_id
    # SQLAlchemy's get() method is perfect for this:
    return db.session.get(User, int(user_id))
#----------------------------------------

#login route
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form.get('user_name')
        email = request.form.get('user_email')
        age = request.form.get('user_age')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with this email already exists: {email}, skipping addition.")
            return render_template("signup.html", error_message="User with this email already exists.")
        try:
            new_user = User(name=name, email=email, age=age, password=password)
            db.session.add(new_user)
            db.session.commit()
            print(f"Added new user: {new_user}")
        except Exception as e:
            print(f"Error adding user to database: {e}")
            db.session.rollback()
            return render_template("signup.html", error_message="An error occurred while saving your data. Please try again later.")
    return render_template('signup.html')

#log_out route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def daily_message(name, email, age):
    """
    Handles age validation and content rendering based on the day of the week.
    
    Returns a rendered template or an error message (rendered via index.html).
    """

    #  Day of Week Logic (For users 18 and older)
    now = datetime.datetime.now()
    day_name = now.strftime("%A")

    # If it is the weekend, show side hustle content
    if day_name in ['Saturday', 'Sunday']:
        message = f"Hi {name}, It's the weekend! Enjoy your day! or Side Hustle Time!"
        theme = "weekend"
        Side_hustle_ideas = [
            "Free lancing",
            "Blogging",
            "Tutoring",
            "Reading Novels",
            "Online Surveys",
            "Learning trading",
            "Selling handmade crafts",
            "Dropshipping",
        ]
        idea = random.choice(Side_hustle_ideas)
        # Note: The original logic dictated returning the sidehustle.html here
        return render_template("sidehustle.html", idea=idea, day=day_name, message=message, theme=theme, user_name=name)
    
    # If it is a weekday, show day activity content
    else:
        task = random.choice(["Stay focused!", "Keep pushing!", "You got this!", "Mail Check", "Walking Time or Stretch Time or Hydration Time"])
        message = f"Hi {name}, Happy {day_name}! {task} Stay productive!"
        theme = "weekday"
        # Note: The original logic dictated returning the day.html here
        return render_template("day.html", day=day_name, message=message, theme=theme, user_name=name)
    
# Here all the added users can be seen    
@app.route('/users',methods=['GET','POST'])
def users():
        all_users = User.query.all()
        return render_template("users.html", users=all_users)

# this is the main route which handles both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Ensure 'name', 'email', and 'age' fields match those in index.html
        # If your index.html uses 'user_name' and 'user_age', adjust the lines below:
        name = request.form.get('user_name') 
        email = request.form.get('user_email') 
        age = request.form.get('user_age') 
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password ==password:
            login_user(user)
            try:
                age= int(age)
            except (ValueError,TypeError):
                return render_template("index.html", error_message="Please enter a valid number for age.")
            
            if age <18:
                return render_template("index.html", error_message="You must be at least 18 years old to use this service.")
            
            # Crucial Fix: The return value of daily_message MUST be returned by index()
            return daily_message(name, email, age)
        
    # GET request: Render the initial form
    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # This line creates the 'user' table if it doesn't exist.
    app.run(debug=True)