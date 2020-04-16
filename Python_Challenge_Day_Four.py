import os
import requests


def print_bar(text=None):
    if text is None:
        print("=" * 70)

    else:
        side_len = (70 - len(text)) // 2

        if len(text) % 2 == 0:
            print("=" * side_len + " " + text + " " + "=" * side_len)

        else:
            print("=" * side_len + " " + text + " " + "=" * (side_len - 1))


def check_url():
    print_bar()
    print("                        Welcome to IsItDown.py!")
    print("  Please write a URL or URLs you want to check. (seperated by comma)")
    print_bar("Write url or urls")

    urls = list(map(lambda url: "http://" + url.strip()
                    if "http://" not in url else url.strip(), input().split(",")))

    print_bar()

    for url in urls:
        try:
            requests.get(url)
            print(f"{url} is up!")

        except Exception as e:
            print(f"{url} is down!")

    print_bar()


def loop():
    check = "y"
    os.system("clear")

    while check == "y":
        check_url()
        check = input("Do you want to start over? (y/n) ")

        while check != "y" and check != "n":
            print("That's not a valid answer")
            print_bar()
            check = input("Do you want to start over? (y/n) ")

        if check == "n":
            print("Ok. bye!")
            print_bar()
            break

        os.system("clear")


if __name__ == "__main__":
    loop()
