from flask import Flask, request, render_template
import requests
import datetime
import random
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def daily_message():
    now = datetime.datetime.now()
    print(now)
    day_name = now.strftime("%A")

    if day_name in ['Saturday', 'Sunday']:
        message = "It's the weekend! Enjoy your day! or Side Hustle Time!"
        theme = "weekend"
        Side_hustle_ideas=["Free lancing",
                       "Blogging",
                       "Tutoring",
                       "Reading Novels",
                       "Online Surveys",
                       "Learning trading",
                       "Selling handmade crafts",
                       "Dropshipping",]
        idea= random.choice(Side_hustle_ideas)
        return render_template("sidehustle.html",idea=idea, day=day_name, message=message, theme=theme)
    else:
        task = random.choice(["Stay focused!", "Keep pushing!", "You got this!", "Mail Check", "Walking Time or Stretch Time or Hydration Time"])
        message = f"Happy {day_name}! {task}  Stay productive!"
        theme = "weekday"
        return render_template("day.html", day=day_name, message=message, theme=theme)



if __name__ == '__main__':
    app.run(debug=True)
