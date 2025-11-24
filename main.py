from bs4 import BeautifulSoup
import asyncio
from playwright.async_api import async_playwright, Playwright
import numpy as np
import pandas as pd
import time
import re
from lang.languages import translations


lang = "pl"
debug = True
extra_debug = False

brand = str(input(translations[lang]["user_input_brand"])).lower()
model = str(input(translations[lang]["user_input_model"])).lower()

URL = f"https://www.otomoto.pl/osobowe/{brand}/{model}/dolnoslaskie?search%5Blat%5D=51.232&search%5Blon%5D=16.907&search%5Border%5D=created_at_first%3Adesc"

titles = []
prices = []
publication_dates = []
urls = []


async def run(playwright: Playwright):
    browser = await playwright.firefox.launch(headless=False)
    context =  await browser.new_context(user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0", locale="pl-PL")
    await context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
    });
    """)
    page = await context.new_page()
    time.sleep(5)
    if debug:
        print(translations[lang]["enter"])
    await page.goto(URL)
    print(translations[lang]["simulating"])
    time.sleep(np.random.uniform(2,5))
    await page.click("#onetrust-accept-btn-handler")
    time.sleep(np.random.uniform(1,1.5))
    for _ in range(np.random.randint(15,30)):
        await page.keyboard.press("ArrowDown")
        time.sleep(np.random.uniform(0.2,1))
    time.sleep(np.random.uniform(2,4))
    for _ in range(np.random.randint(3,6)):
        await page.keyboard.press("ArrowDown")
        time.sleep(np.random.uniform(0.2,1))
    time.sleep(np.random.uniform(3,6))
    for _ in range(np.random.randint(10,40)):
        await page.keyboard.press("ArrowDown")
        time.sleep(np.random.uniform(0.2,1))
    time.sleep(np.random.uniform(5,20))
    if debug:
        print(translations[lang]["fetching"])
    html = await page.content()
    await browser.close()
    
    return html

async def main():
    async with async_playwright() as playwright:
        html = await run(playwright)
        return html
    
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
        div = section.find("section", class_="ooa-ljs66p e1fi2t0p0")
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


while True:
    html = asyncio.run(main())
    if debug:
        print(translations[lang]["parsing"])
    soup = BeautifulSoup(html,'html.parser')

    if debug:
        print(translations[lang]["extract"])
    find_title()
    find_price()
    publication_date()
    find_url()
    if extra_debug:
        print(len(titles), len(prices), len(publication_dates), len(urls))

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
    else:
        print(translations[lang]["none"])
    time.sleep(600)
