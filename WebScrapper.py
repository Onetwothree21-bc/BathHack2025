import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def web_scrapper(url):
    try:
        # Try with requests
        response = requests.get(url, timeout=5, headers={
            "User-Agent": "Mozilla/5.0"
        })
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = ' '.join([p.get_text() for p in paragraphs])
        if text.strip():  # If it actually found content
            return text
        else:
            raise Exception("No content in static HTML, using Selenium...")

    except Exception as e:
        print("Switching to Selenium: ", e)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        paragraphs = soup.find_all("p")
        text = ' '.join([p.get_text() for p in paragraphs])
        return text.strip()


def get_headline(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = soup.find('h1')
    if h1 and h1.text.strip():
        return h1.text.strip()

    title = soup.find('title')
    if title and title.text.strip():
        return title.text.strip()

    return "Headline not found"

