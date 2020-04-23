import requests
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


def find_upvotes(html):
    pass


def find_title(html):
    pass


def get_reddit_comment_page(postfix):
    return "https://reddit.com/" + postfix


def parse_content_to_html(content):
    return BeautifulSoup(content, "html.parser")


def get_reddit_response_content(sub_reddit):
    url = f"https://www.reddit.com/r/{sub_reddit}/top/?t=month"

    try:
        response = requests.get(url, headers)

        return response.content

    except Exception:
        return None


def create_error_message(item):
    return f"Can't get {item}'s contents."


def create_result_data(upvotes, title, url):
    return {"upvotes": upvotes, "title": title, "url": url}


@app.route("/")
def home():
    return render_template("home.html", sub_reddits=sub_reddits)


@app.route("/read")
def read():
    items = list(request.args)
    errors, results = [], []

    for item in items:
        content = get_reddit_response_content(item)

        if not content:
            errors.append(create_error_message(item))
            continue

        html = parse_content_to_html(content)
        print(type(html))

    return render_template("read.html", items=items, errors=errors, results=results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
