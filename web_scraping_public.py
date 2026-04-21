import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/finance/quote/RELIANCE:NSE"
headers = {"User-Agent": "Mozilla/5.0"}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

price_element = soup.find("div", attrs={"data-last-price": True})

if price_element:
    print("Reliance Price:", price_element.text)
else:
    print("Price not found")