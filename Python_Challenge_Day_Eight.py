import os
import csv
import requests
from time import sleep
from bs4 import BeautifulSoup


def parse_html(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_super_brand_links():
    alba_url = "http://www.alba.co.kr"

    soup = parse_html(alba_url)

    super_brands = soup.find("div", attrs={"id": "MainSuperBrand"})
    super_brands = [
        [brand.get("href"), brand.find("span", attrs={"class": "company"}).get_text()]
        for brand in super_brands.select("ul > li.impact > a.goodsBox-info")
    ]

    return super_brands


def get_detail_jobs(brand_link):
    sleep(1.5)
    soup = parse_html(brand_link)
    jobs = soup.find("div", attrs={"id": "NormalInfo"})
    jobs = jobs.find("tbody")
    jobs = jobs.find_all("tr")

    result = []

    for job in jobs:
        col = []
        if job.has_attr("class") and (
            "summaryView" in job["class"] or "divide" in job["class"]
        ):
            continue

        for data in [".local", ".company", ".data", ".pay", ".regDate"]:
            tag = job.select(data)
            if len(tag) != 0:
                tag = tag[0]
                col.append(tag.get_text(strip=True).replace("\xa0", " "))

        result.append(col)

    return result


def change_work_dir():
    FOLDER_NAME = "Challenge_Day_Eight_Result"

    if FOLDER_NAME not in os.listdir():
        os.mkdir(FOLDER_NAME)

    os.chdir(FOLDER_NAME)


def export_to_csv(file_name, data):
    with open(f"{file_name}.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f, delimiter=",")
        wr.writerow(["place", "title", "time", "pay", "date"])
        wr.writerows(data)


def main():
    os.system("clear")

    super_brands = get_super_brand_links()

    change_work_dir()

    for idx, super_brand in enumerate(super_brands):
        print(f"========== {super_brand[1]} 구직 데이터 저장 시작")
        print(
            f"========== {idx + 1:2} / {len(super_brands)} ({(idx + 1) / len(super_brands) * 100:.2f} %)"
        )
        result = get_detail_jobs(super_brand[0])
        export_to_csv(super_brand[1], result)
        print(f"========== {super_brand[1]} 구직 데이터 저장 완료")
        print("==========")


if __name__ == "__main__":
    main()
