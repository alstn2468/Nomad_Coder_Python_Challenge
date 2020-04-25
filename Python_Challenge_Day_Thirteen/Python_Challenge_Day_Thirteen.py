"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from io import StringIO
from flask import Flask, render_template, request, Response, redirect, url_for
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
        db[term] = jobs

    return render_template("search.html", jobs=jobs, term=term)


@app.route("/export")
def export():
    term = request.args.get("term").lower()
    try:
        output = StringIO()
        output.write("Link,Title,Company\n")

        for job in db[term]:
            for idx, val in enumerate(job.values()):
                output.write(str(val))

                if idx < (len(job) - 1):
                    output.write(",")

            output.write("\n")

        response = Response(
            output.getvalue(),
            mimetype="text/csv",
            content_type="application/octet-stream",
        )
        response.headers["Content-Disposition"] = f"attachment; filename={term}.csv"

        return response
    except Exception:
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
