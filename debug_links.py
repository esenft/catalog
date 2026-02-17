import requests
from bs4 import BeautifulSoup
BASE_URL = "https://catalog.northeastern.edu/course-descriptions/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CatalogScraper/1.0)"}
resp = requests.get(BASE_URL, headers=HEADERS)
soup = BeautifulSoup(resp.text, "html.parser")
for a in soup.find_all('a', href=True):
    if a['href'].startswith('/course-descriptions/'):
        print(a['href'], a.text)
