from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
from pprint import pprint

CHROME_DRIVER_PATH = "C:/Users/Dep. Técnico/Documents/Development/chromedriver.exe"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScp-DU7bYGbY9Z6xEFi7CrRkvfLeg1Qx7py8ULRhpv4S30qOw/viewform?usp=sf_link"
VIVA_URL = "https://www.vivareal.com.br/aluguel/parana/curitiba/bairros/cabral/apartamento_residencial/#preco-ate=1800&preco-total=sim&quartos=2"


class Viva:
    def __init__(self) -> None:
        response = requests.get(url=VIVA_URL)
        webpage = response.text
        soup = BeautifulSoup(webpage, "html.parser")
        prices = [
            price.getText().split("/")[0].replace(".", "").strip()
            for price in soup.find_all(class_="js-property-card-prices")
        ]
        address = [
            local.getText()
            for local in soup.find_all(name="span", class_="property-card__address")
        ]
        urls = [
            url.get("href")
            for url in soup.find_all(name="a", class_="property-card__content-link")
        ]
        self.rents = {}
        for index in range(len(prices)):
            self.rents.update(
                {
                    index: {
                        "price": prices[index],
                        "address": address[index],
                        "url": urls[index],
                    }
                }
            )


class Form:
    def __init__(self, address, price, url) -> None:
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        driver.get(url=FORM_URL)
        time.sleep(1)
        address_input = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        address_input.send_keys(address)
        price_input = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        price_input.send_keys(price)
        url_input = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
        )
        url_input.send_keys(url)
        button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
        button.click()

        driver.quit()


viva = Viva()
# pprint(viva.rents)
for rent in viva.rents.values():
    a = rent["address"]
    p = rent["price"]
    u = rent["url"]
    form = Form(address=a, price=p, url=f"https://www.zapimoveis.com.br/{u}")

