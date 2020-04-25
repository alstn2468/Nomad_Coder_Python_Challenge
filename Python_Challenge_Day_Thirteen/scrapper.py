import requests
from bs4 import BeautifulSoup

WEWORK_REMOTELY_URL = "https://weworkremotely.com/remote-jobs/search?utf8=✓&term={}"
STACK_OVERFLOW_URL = "https://stackoverflow.com/jobs?r=true&q={}"
REMOTE_OK_URL = "https://remoteok.io/remote-{}-jobs"


def get_text_response(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception

        return response.text

    except Exception:
        return None


def parse_text_to_html(text):
    return BeautifulSoup(text, "html.parser")


def create_job_dict(url, company, title):
    return {"url": url, "company": company, "title": title}


def aggregate_remote_job(term):
    return [
        *scrape_wework_remotely(term),
        *scrape_stack_overflow(term),
        *scrape_remote_ok(term),
    ]


def scrape_wework_remotely(term):
    text = get_text_response(WEWORK_REMOTELY_URL.format(term))
    html = parse_text_to_html(text)
    features = html.find_all("li", attrs={"class": "feature"})

    result = []

    for feature in features:
        detail = feature.find_all("a")

        if len(detail) > 1:
            detail = detail[1]
        else:
            detail = detail[0]

        url = "https://weworkremotely.com" + detail["href"].strip()
        company = feature.find("span", attrs={"class": "company"}).get_text(strip=True)
        title = feature.find("span", attrs={"class": "title"}).get_text(strip=True)

        result.append(create_job_dict(url, company, title))

    return result


def scrape_stack_overflow(term):
    text = get_text_response(STACK_OVERFLOW_URL.format(term))
    html = parse_text_to_html(text)
    list_results = html.find("div", attrs={"class": "listResults"})
    grids = list_results.find_all("div", attrs={"class": "grid"})

    result = []

    for grid in grids:
        a_tag = grid.find("a", attrs={"class": "s-link stretched-link"})

        if not a_tag:
            continue

        url = "https://stackoverflow.com" + a_tag["href"].strip()
        title = a_tag["title"].strip()
        company = (
            grid.find("h3", attrs={"class": "fc-black-700 fs-body1 mb4"})
            .find("span")
            .get_text(strip=True)
        )

        result.append(create_job_dict(url, company, title))

    return result


def scrape_remote_ok(term):
    text = get_text_response(REMOTE_OK_URL.format(term))
    html = parse_text_to_html(text)
    table = html.find("table", attrs={"id": "jobsboard"})
    jobs = table.find_all(
        "td", attrs={"class": "company position company_and_position"}
    )

    result = []

    for job in jobs:
        url = (
            "https://remoteok.io"
            + job.find("a", attrs={"class": "preventLink"})["href"]
        )
        title = job.find("h2", attrs={"itemprop": "title"}).get_text(strip=True)
        company = job.find("h3", attrs={"itemprop": "name"}).get_text(strip=True)

        result.append(create_job_dict(url, company, title))

    return result
