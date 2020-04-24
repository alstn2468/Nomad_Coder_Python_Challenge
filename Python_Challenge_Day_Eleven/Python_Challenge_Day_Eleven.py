import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

sub_reddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django",
]


app = Flask("DayEleven")


def find_all_post_datas(html, item):
    result = []
    regex = re.compile(".*Post.*")
    posts = html.find_all("div", attrs={"class": regex})

    for post in posts:
        upvotes = post.find(
            "div", attrs={"class": "_1rZYMD_4xY3gRcSS3p8ODO"}
        ).get_text()
        url = post.find(
            "a", attrs={"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"}
        )
        title = post.find("h3").get_text()

        if all([upvotes, url, title]):
            if "k" in upvotes:
                upvotes = int(float(upvotes.replace("k", "")) * 1000)

            result.append(
                create_result_data(
                    int(upvotes), title, get_reddit_comment_page(url["href"]), item
                )
            )

    return result


def get_reddit_comment_page(postfix):
    return "https://reddit.com" + postfix


def parse_text_to_html(text):
    return BeautifulSoup(text, "html.parser")


def get_reddit_response_text(sub_reddit):
    url = f"https://www.reddit.com/r/{sub_reddit}/top/?t=month"

    try:
        response = requests.get(url, headers=headers)

        return response.text

    except Exception:
        return None


def create_error_message(item):
    return f"Can't get {item}'s texts."


def create_result_data(upvotes, title, url, item):
    return {"upvotes": upvotes, "title": title, "url": url, "item": item}


@app.route("/")
def home():
    return render_template("home.html", sub_reddits=sub_reddits)


@app.route("/read")
def read():
    items = list(request.args)
    errors, results = [], []

    for item in items:
        text = get_reddit_response_text(item)

        if not text:
            errors.append(create_error_message(item))
            continue

        html = parse_text_to_html(text)
        results.extend(find_all_post_datas(html, item))

    results.sort(key=lambda x: x["upvotes"], reverse=True)

    return render_template("read.html", items=items, errors=errors, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
