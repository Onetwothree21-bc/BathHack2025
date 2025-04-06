import requests
import GUI
from bs4 import BeautifulSoup

def web_scrapper():
    global text
    response = requests.get(GUI.url)
    soup = BeautifulSoup(response.text, 'html.parser')

    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
