from operator import index

import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import os
import smtplib

URL = os.environ["URL"]
CURRENCY = "USD"
FROM_EMAIL = os.environ["FROM_EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["FROM_EMAIL_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]
SAVINGS = os.environ["SAVINGS"]

response = requests.get(url=URL)
html = response.text

soup = BeautifulSoup(html, "html.parser")

html_currency = soup.select("td.c_symbol")
currency_list = [currency.getText() for currency in html_currency]

if CURRENCY in currency_list:
    currency_index = currency_list.index(CURRENCY)

c_buy_html = soup.select("td.c_buy")
c_buy_list = [value.getText() for value in c_buy_html]

currency_value = float(c_buy_list[currency_index])
savings_in_pln = float(SAVINGS) * currency_value
print(currency_value)
msg = EmailMessage()
msg["Subject"] = "Kurs dolara na dziś :)"
msg["From"] = FROM_EMAIL
msg["To"] = TO_EMAIL
content = f"Aktualny kurs sprzedaży 1 {CURRENCY} na {URL} to {currency_value} PLN \n Dla {SAVINGS} {CURRENCY} - {savings_in_pln} PLN"
msg.set_content(content)
print(msg)

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=FROM_EMAIL, password=EMAIL_PASSWORD)
    connection.send_message(
        from_addr=FROM_EMAIL,
        to_addrs=TO_EMAIL,
        msg=msg)