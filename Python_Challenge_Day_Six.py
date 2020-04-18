import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency


def get_int_input(length, prompt="#: "):
    user_input = input(prompt).strip()

    try:
        user_input = int(user_input)

        if user_input > (length - 1) or user_input < 0:
            raise RuntimeError
        return user_input
    except ValueError:
        return get_int_input(length, prompt="That wasn't a number.\n" + prompt)
    except RuntimeError:
        return get_int_input(length, prompt="Choose a number from the list.\n" + prompt)


def get_currency_input(a_country, b_country, error=None):
    if error:
        print(error)

    user_input = input(
        f"\nHow many {a_country} do you want to convert to {b_country}\n"
    )

    try:
        user_input = int(user_input)

        if user_input < 0:
            raise RuntimeError

        return user_input

    except ValueError:
        return get_currency_input(a_country, b_country, error="That wasn't a number.")

    except RuntimeError:
        return get_currency_input(
            a_country, b_country, error="Money to convert cannot be less than zero."
        )


def parse_data():
    url = "https://www.iban.com/currency-codes"

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    countries = soup.select("table > tbody > tr")
    data = [
        list(filter(lambda x: x != "\n", country.children)) for country in countries
    ]
    filtered_data = list(
        (
            map(
                lambda country: [country[0].text.capitalize(), country[-2].text],
                filter(
                    lambda country: country[1].text != "No universal currency", data
                ),
            )
        )
    )

    return filtered_data


def convert_currency(a_currency, b_currency, amount):
    base_url = "https://transferwise.com/"
    post_fix = (
        f"gb/currency-converter/{a_currency}-to-{b_currency}-rate?amount={amount}"
    )
    url = base_url + post_fix

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    amount_to = int(soup.find("input", id="cc-amount-to").get("value").split(".")[0])

    return [
        format_currency(amount, a_currency),
        format_currency(amount_to, b_currency),
    ]


def main():
    os.system("clear")
    filtered_data = parse_data()
    print("Welcome to CurrencyConvert PRO 2000")
    print("\n".join([f"# {idx:3} {val[0]}" for idx, val in enumerate(filtered_data)]))

    print("\nWhere are you from Choose a country by number.\n")

    a_country = filtered_data[get_int_input(len(filtered_data))]
    print(a_country[0])

    print("\nNow choose another country.\n")

    b_country = filtered_data[get_int_input(len(filtered_data))]
    print(b_country[0])

    money = get_currency_input(a_country[1], b_country[1])
    convert_result = convert_currency(a_country[1], b_country[1], money)

    print(f"{convert_result[0]} is {convert_result[1]}")


if __name__ == "__main__":
    main()
