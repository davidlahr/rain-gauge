import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import pandas as pd

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, InputRequired
import requests
from datetime import datetime, timedelta, timezone
import dateutil.parser

import pytz
from dotenv import load_dotenv
load_dotenv()
import os

from forms import *

############### APPLICATION ########################################
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)


# VARIABLES ##############################################
endpoint = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history?"
api_key = os.getenv('API_KEY')

# USED TO FORMAT DATE COMING BACK IN API - CALLED IN RESULTS.HTML ###########
@app.template_filter()
def format_datetime(value):
    new_date = dateutil.parser.isoparse(value)
    return new_date.strftime('%b %d, %Y')


def get_rain(weather_params):
    response = requests.get(endpoint, params=weather_params)
    response.raise_for_status()

    weather_data = response.json()

    # PARSING
    locate = weather_data["locations"]
    data = locate[weather_params['locations']]['values']

    print(data)
    # TEST DATAFRAME
    dataf = pd.DataFrame([data][0])
    print(dataf)

    # data1 = data[1]
    # print(data1['precip'])

    total = 0

    for d in range(len(data)):
        date = data[d]['datetimeStr']
        precip = data[d]['precip']
        total += precip
        # print(data[d]['datetimeStr']+str(data[d]['precip']))
        print(f"{date} {precip}")

    return total, data

@app.route('/', methods=["GET", "POST"])
def main_page():
    form = CheckRain()
    if form.validate_on_submit():
        weather_params = {
            "locations": form.address.data,
            "aggregateHours": "24",
            "startDateTime": form.start_date.data,
            "endDateTime": form.end_date.data,
            "contentType": "json",
            "key": api_key,
        }
        rain = get_rain(weather_params)
        total = rain[0]
        data = rain[1]

        # return('hello world')
        return render_template("results.html", total=total, form=form, data=data)
    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)