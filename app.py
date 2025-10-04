from flask import Flask, request, render_template, redirect, url_for
import requests # Included as requested, though currently unused
import datetime
import random
from bs4 import BeautifulSoup # Included as requested, though currently unused

app = Flask(__name__)


def daily_message(name, email, age):
    """
    Handles age validation and content rendering based on the day of the week.
    
    Returns a rendered template or an error message (rendered via index.html).
    """
    
    # 1. Age Validation
    try:
        if not age or int(age) < 18:
            # If age is not provided or is under 18, return to the form with an error.
            error_msg = "You must be at least 18 years old to use this service."
            # Re-render the index.html template with the error_message
            return render_template("index.html", error_message=error_msg)
    except ValueError:
        # Handle case where age is submitted but is not a valid number
        error_msg = "Please enter a valid number for age."
        return render_template("index.html", error_message=error_msg)

    # 2. Day of Week Logic (For users 18 and older)
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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Ensure 'name', 'email', and 'age' fields match those in index.html
        # If your index.html uses 'user_name' and 'user_age', adjust the lines below:
        name = request.form.get('user_name') 
        email = request.form.get('user_email') 
        age = request.form.get('user_age') 
        
        print(f"Name: {name}, Email: {email}, Age: {age}")
        
        # Crucial Fix: The return value of daily_message MUST be returned by index()
        return daily_message(name, email, age)
        
    # GET request: Render the initial form
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
