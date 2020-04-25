import requests
from bs4 import BeautifulSoup

WEWORK_REMOTELY_URL = "https://weworkremotely.com/"
STACK_OVERFLOW_URL = "https://stackoverflow.com/jobs"
REMOTE_OK_URL = "https://remoteok.io/"


def get_text_response(url):
    try:
        response = requests.get(url)

        return response.text

    except Exception:
        return None


def parse_text_to_html(text):
    return BeautifulSoup(text, "html.parser")


def aggregate_remote_job():
    pass


def scrape_wework_remotely():
    pass


def scrape_stack_overflow():
    pass


def scrape_remote_ok():
    pass
