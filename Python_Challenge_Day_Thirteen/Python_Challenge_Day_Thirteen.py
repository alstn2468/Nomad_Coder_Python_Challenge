"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request
from scrapper import aggregate_remote_job

app = Flask("DayThirteen")
db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    term = request.args.get("term").lower()

    if term in db:
        jobs = db[term]
    else:
        jobs = aggregate_remote_job(term)
        db[term] = 
        
    return render_template("search.html", jobs=jobs, term=term)


@app.route("/export")
def export():
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
