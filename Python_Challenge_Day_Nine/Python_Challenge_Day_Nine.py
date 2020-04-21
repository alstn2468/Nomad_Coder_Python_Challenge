import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine")


@app.route("/")
def home():
    order = request.args.get("order", default="popular")

    try:

        if order == "popular":
            response = requests.get(popular)

        elif order == "new":
            response = requests.get(new)

        news = response.json()["hits"]

        return render_template("home.html", order=order, news=news)
    except Exception:
        error = f"Can't get {order} news."

        return render_template("home.html", order=order, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
