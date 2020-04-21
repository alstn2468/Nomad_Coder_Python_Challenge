import requests
from flask import Flask, render_template, request


app = Flask("DayNine")
base_url = "http://hn.algolia.com/api/v1"
new = f"{base_url}/search_by_date?tags=story"
popular = f"{base_url}/search?tags=story"
db = {}


def make_detail_url(id):
    return f"{base_url}/items/{id}"


@app.route("/")
def home():
    order = request.args.get("order", default="popular")

    try:
        if order not in db.keys():
            if order == "popular":
                response = requests.get(popular)

            elif order == "new":
                response = requests.get(new)

            news = response.json()["hits"]
            db[order] = news

        else:
            news = db[order]

        return render_template("home.html", order=order, news=news)
    except Exception:
        error = f"Can't get {order} news."

        return render_template("home.html", order=order, error=error)


@app.route("/<int:object_id>")
def detail(object_id):

    try:
        detail_url = make_detail_url(object_id)
        response = requests.get(detail_url)
        data = response.json()
        return render_template("detail.html", object_id=object_id, data=data)

    except Exception:
        error = f"Can't get detail information."

    return render_template("detail.html", object_id=object_id, data=data, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
