import os
import sys
from bs4 import BeautifulSoup

def test_catalog_html(directory="catalog_html"):
    files = sorted([f for f in os.listdir(directory) if f.endswith(".html")])
    print(f"Found {len(files)} HTML files.")
    for fname in files[:5]:  # Check first 5 files
        path = os.path.join(directory, fname)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else None
        print(f"{fname}: title={title!r}, length={len(html)} chars")
    print("... (output truncated)")

def print_first_courses(html_file, n=5):
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    courses = soup.find_all("div", class_="courseblock")
    print(f"Found {len(courses)} courses in {html_file}.")
    for course in courses[:n]:
        title = course.find("p", class_="courseblocktitle")
        desc = course.find("p", class_="cb_desc")
        # Extract course number from the title string
        course_number = "[No course number]"
        if title:
            import re
            m = re.match(r"([A-Z]+\s*\d+)", title.get_text(strip=True))
            if m:
                course_number = m.group(1).replace("\xa0", " ")
        print(f"\n{course_number}:")
        print(title.get_text(strip=True) if title else "[No title]")
        print(desc.get_text(strip=True) if desc else "[No description]")

if __name__ == "__main__":
    test_catalog_html()
    files = [
        "catalog_html/subcategory_000.html",
        "catalog_html/subcategory_001.html"
    ]
    for html_file in files:
        print(f"\n===== {html_file} =====")
        print_first_courses(html_file)
