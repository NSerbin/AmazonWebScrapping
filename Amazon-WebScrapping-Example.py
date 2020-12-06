#!/usr/bin/env python3
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


def getURL(parametros):
    """ Generate URL to search """
    base = 'https://www.amazon.es/s?k={}&ref=nb_sb_noss_2'
    
    parametros = parametros.replace(' ', '+')

    url = base.format(parametros)
    url += '&page={}'

    return url

def xiaomiPocoX3NFC(item):
    """ Extract and return data from a single record"""

    # Description and URL
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.es' + atag.get('href')
    try:
    # Price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    result = (description, price, url)
    return result

def main(parametros):
    """ Run Main program Routine """
    
    # Options to use BRAVE BROWSER instead of Chrome
    chromedriver_path = '/usr/bin/chromedriver'
    brave_path = '/usr/bin/brave-browser'
    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)

    records = []
    url = getURL(parametros)

    for page in range(1, 21):
        browser.get(url.format(page))
        sleep(0.5)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        results = soup.find_all('div', {'data-component-type' : 's-search-result'})

        for item in results:
            record = xiaomiPocoX3NFC(item)
            if record:
                records.append(record)

    browser.close()

    #Save data to CSV
    with open ('results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(['Description', 'Price', 'URL'])
        writer.writerows(records)

main('Ultrawide Monitor 144hz')