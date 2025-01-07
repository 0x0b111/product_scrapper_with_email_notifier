import requests;
from bs4 import BeautifulSoup;
import smtplib;
import os;
from dotenv import load_dotenv;

load_dotenv()

url = "https://appbrewery.github.io/instant_pot/"
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"

}


try:
    response = requests.get(url, headers= header);
    response.raise_for_status()

except requests.exceptions.RequestException as e:
    print(f'{e}')


soup = BeautifulSoup(response.text, "html.parser")

product_title = soup.find(id="productTitle").getText().strip()
price = float(soup.find(name="span", class_ = "a-price-whole").getText().split('.')[0])

print(product_title)
print(price)

BUY_PRICE = 100

if price < BUY_PRICE:
    message = f"{product_title} is on sale: {price} $"

    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADDRESS"],
            to_addrs=os.environ["EMAIL_ADDRESS"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )