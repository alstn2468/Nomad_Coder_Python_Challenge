import requests
from flask import Flask, render_template, request


app = Flask("DayNine")
base_url = "http://hn.algolia.com/api/v1"
new = f"{base_url}/search_by_date?tags=story"
popular = f"{base_url}/search?tags=story"
news_db, comment_db = {}, {}


def make_detail_url(id):
    return f"{base_url}/items/{id}"


@app.route("/")
def index():
    order = request.args.get("order", default="popular")

    try:
        if order not in news_db.keys():
            if order == "popular":
                response = requests.get(popular)

            elif order == "new":
                response = requests.get(new)

            news = response.json()["hits"]
            news_db[order] = news

        else:
            news = news_db[order]

        return render_template("index.html", order=order, news=news)
    except Exception:
        error = f"Can't get {order} news."

        return render_template("index.html", order=order, error=error)


@app.route("/<int:object_id>")
def detail(object_id):

    try:
        if object_id not in comment_db.keys():
            detail_url = make_detail_url(object_id)
            response = requests.get(detail_url)
            data = response.json()
            comment_db[object_id] = data

        else:
            data = comment_db[object_id]

        return render_template("detail.html", object_id=object_id, data=data)

    except Exception:
        error = f"Can't get detail information."

    return render_template("detail.html", object_id=object_id, data=data, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
