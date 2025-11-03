from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import re
from lang.languages import translations

lang = "pl"

brand = str(input(translations[lang]["user_input_brand"])).lower()
model = str(input(translations[lang]["user_input_model"])).lower()

URL = f"https://www.otomoto.pl/osobowe/{brand}/{model}/dolnoslaskie?search%5Blat%5D=51.232&search%5Blon%5D=16.907&search%5Border%5D=created_at_first%3Adesc"

debug = True


while True:
    options = Options()
    options.binary_location = "firefox-144.0.2/firefox/firefox"
    options.add_argument("--headless")
    options.add_argument("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0")
    driver = webdriver.Firefox(options=options)



    if debug:
        print(translations[lang]["enter"])
    time.sleep(5)
    driver.get(URL)
    if debug:
        print(translations[lang]["loading"])
    time.sleep(7)
    html = driver.page_source
    if debug:
        print(translations[lang]["parsing"])
    soup = BeautifulSoup(html, "html.parser")


    titles = []
    prices = []
    publication_dates = []
    urls = []


    def find_title():
        for section in soup.find_all("article", attrs={"data-orientation": "horizontal"}):
            div = section.find("div", class_="ooa-3ux3i6 e8qbg6l0")
            if not div:
                continue
            h2 = div.find("h2", class_="etydmma0 ooa-ezpr21")
            a = h2.find("a")
            titles.append(a.get("aria-label"))

    def find_price():
        for section in soup.find_all("article", attrs={"data-orientation": "horizontal"}):
            h3 = section.find("h3", class_="efzkujb1 ooa-3ewd90")
            if not h3:
                continue
            prices.append(h3.get_text(strip=True))

    def publication_date():
        for section in soup.find_all("article", attrs={"data-orientation": "horizontal"}):
            div = section.find("div", class_="ooa-d3dp2q e13x2f730")
            if not div:
                continue
            ul = div.find("ul", class_="ooa-1o0axny e1a9azt30")
            p = ul.find_all("p")[1]
            publication_dates.append(p.get_text(strip=True))

    def find_url():
        for section in soup.find_all("article", attrs={"data-orientation": "horizontal"}):
            div = section.find("div", class_="ooa-3ux3i6 e8qbg6l0")
            if not div:
                continue
            a = div.find("a")
            urls.append(a.get("href"))


    
    if debug:
        print(translations[lang]["extract"])
    find_title()
    find_price()
    publication_date()
    find_url()

    if debug:
        print(translations[lang]["cleanup"])
    driver.quit()



    df = pd.DataFrame({
        "Title": titles,
        "Price": prices,
        "Publication_date": publication_dates,
        "URL": urls
    })

    df = df[~df['Publication_date'].str.contains('Podbite', case=False)].reset_index(drop=True)

    def change_to_hours(x):
        hours = re.search(r'Opublikowano\s*(\d+)\s*godz',x)
        days = re.search(r'Opublikowano\s*(\d+)\s*dni',x)
        oneday = re.search(r'Opublikowano\s*(\d+)\s*dzień',x)
        weeks = re.search(r'Opublikowano\s*(\d+)\s*tyg',x)
        oneweek = re.search(r'Opublikowano\s*(\d+)\s*tydz',x)
        yesterday = re.search(r'wczoraj',x)
        if hours:
            return int(hours.group(1))
        if days:
            return int(days.group(1))*24
        if oneday:
            return int(oneday.group(1))*24
        if weeks:
            return int(weeks.group(1))*7*24
        if oneweek:
            return int(oneweek.group(1))*7*24
        if yesterday:
            return 24.0
        

    df["hours"] = df["Publication_date"].apply(change_to_hours)
    df.sort_values(by="hours")
    df.drop(columns=["hours"],inplace=True)


    df_local = pd.read_csv("latest_offers.csv")
    equal = df["URL"].equals(df_local["URL"])

    if equal == False:
        if debug:
            print(translations[lang]["new"])
        df.to_csv("latest_offers.csv",index=False)
    print(translations[lang]["done"])
    time.sleep(60)
