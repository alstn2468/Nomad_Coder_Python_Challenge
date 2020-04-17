import os
import requests
from bs4 import BeautifulSoup


def get_int_input(length, prompt="#: "):
    user_input = input(prompt).strip()

    try:
        user_input = int(user_input)

        if user_input > (length - 1) or user_input < 0:
            raise RuntimeError
        return user_input
    except ValueError:
        return get_int_input(length, prompt="That wasn't a number.\n#: ")
    except RuntimeError:
        return get_int_input(length, prompt="Choose a number from the list.\n#: ")


def parse_data():
    url = "https://www.iban.com/currency-codes"

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    countries = soup.select("table > tbody > tr")
    data = [list(filter(lambda x: x != "\n", country.children))
            for country in countries]
    filtered_data = list(
        (
            map(
                lambda country: [
                    country[0].text.capitalize(), country[-2].text],
                filter(lambda country: country[1].text !=
                       "No universal currency", data),
            )
        )
    )

    return filtered_data


def main():
    os.system("clear")
    filtered_data = parse_data()
    print("Hello! Pease choose select a country by number:")
    print("\n".join([f"# {idx:3} {val[0]}" for idx,
                     val in enumerate(filtered_data)]))

    user_input = get_int_input(len(filtered_data))
    print(user_input)
    print(
        f"""You choose {filtered_data[user_input][0]}
  The currency code is {filtered_data[user_input][1]}"""
    )


if "__name__" == "__main__":
    main()
