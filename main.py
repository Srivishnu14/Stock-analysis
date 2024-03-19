import os
from flask import Flask, render_template, redirect, url_for, request
from flask import Flask
import requests
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

API_KEY = os.environ.get('API_KEY'),

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/eod", methods=["GET", "POST"])
def eod():
    success = None
    if success == None:
        success = ""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        today = datetime.datetime.today() - datetime.timedelta(1)
        yesterday = str(today.date())
        print(yesterday)

        parameters = {
            "access_key": API_KEY,
            "symbols": symbol
        }
        url = f"http://api.marketstack.com/v1/eod/{yesterday}"
        response = requests.get(url=url, params=parameters)
        print(response)
        response_is_ok = response.ok

        if response_is_ok:
            data = response.json()["data"][0]
            print(data)
            success = "Symbol Present"
            color = "green"
            return render_template("eod.html", success=success, color=color, data_present=response_is_ok, data=data)
        else:
            data = None
            success = "Symbol Error"
            color = "red"
            return render_template("eod.html", success=success, color=color, data_present=response_is_ok, data=data)

    return render_template("eod.html", success=success)


@app.route("/historical", methods=["GET", "POST"])
def historical():
    success = None
    if success == None:
        success = ""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        print(symbol, from_date, to_date)

        parameters = {
            "access_key": API_KEY,
            "symbols": symbol,
            "date_from" : from_date,
            "date_to" : to_date,
            "limit" : 1000
        }
        url = f"http://api.marketstack.com/v1/eod"
        response = requests.get(url=url, params=parameters)
        print(response)
        response_is_ok = response.ok

        if response_is_ok:
            data_d = response.json()["data"]
            success = "Symbol Present"
            color = "green"
            lens = len(data_d)
            return render_template("historical.html", success=success, color=color, data_present=True, data_d=data_d,
                                   lens=lens)
        else:
            success = "Symbol Error"
            color = "red"
            return render_template("historical.html", success=success, color=color, data_present=False)
    return render_template("historical.html")


if __name__ == "__main__":
    app.run(debug=True)

