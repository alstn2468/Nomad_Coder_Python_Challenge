"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask("DayThirteen")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    term = request.args.get("term").lower()
    print(term)
    return render_template("search.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
