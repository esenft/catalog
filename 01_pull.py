
# -----------------------------------------------
#  1. Data Acquisition:
#  Download all the public course catalog data in raw HTML format from Northeastern University.
# -----------------------------------------------

# To run: type python 01_pull.py in terminal

import requests
from bs4 import BeautifulSoup
import os
import time

BASE_URL = "https://catalog.northeastern.edu/course-descriptions/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CatalogScraper/1.0)"}
SAVE_DIR = "catalog_html"

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_main_page():
	resp = requests.get(BASE_URL, headers=HEADERS)
	resp.raise_for_status()
	return resp.text

def parse_subcategory_links(html):
	soup = BeautifulSoup(html, "html.parser")
	links = []
	for a in soup.find_all('a', href=True):
		href = a['href']
		# Only subcategory pages, not the root
		if href.startswith('/course-descriptions/') and href != '/course-descriptions/':
			full_url = "https://catalog.northeastern.edu" + href
			if full_url not in links:
				links.append(full_url)
	return links

def fetch_and_save_subcategory(url, idx):
	resp = requests.get(url, headers=HEADERS)
	resp.raise_for_status()
	fname = os.path.join(SAVE_DIR, f"subcategory_{idx:03d}.html")
	with open(fname, "w", encoding="utf-8") as f:
		f.write(resp.text)
	print(f"Saved {url} -> {fname}")
	time.sleep(1)  # be polite

def main():
	main_html = fetch_main_page()
	subcat_links = parse_subcategory_links(main_html)
	print(f"Found {len(subcat_links)} subcategories.")
	for idx, url in enumerate(subcat_links):
		fetch_and_save_subcategory(url, idx)

if __name__ == "__main__":
	main()

