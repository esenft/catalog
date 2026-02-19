import requests
from bs4 import BeautifulSoup
import re
import json
import time
import string

BASE_URL = "https://student.mit.edu/catalog/"
OUTPUT_FILE = "11_mit_2026.json"

COURSE_PAT = re.compile(r"^([A-Z0-9]{1,4}\.[A-Za-z0-9]{2,4}(?:\[J\])?)\s+(.+?)\s*$")

DEPARTMENT_CODES = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "14", "15", "16", "17", "18", "20", "21", "22", "24",
    "21A", "CMS", "21W", "21G", "21H", "21L", "21M", "21T", "WGS", "CC", "CG", "CSB", "CSE", "EC", "EM", "ES", "HST", "IDS", "MAS", "SCM", "STS", "SWE",
    "AS", "MS", "NS"
]

SUFFIXES_GENERAL = ["a", "b", "c", "d", "e"]
SUFFIXES_COURSE4 = ["a", "b", "c", "d", "e", "f", "g"]

def extract_courses_from_dept(url):
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        courses = []
        for h3 in soup.find_all("h3"):
            text = h3.get_text(separator=" ", strip=True)
            match = COURSE_PAT.match(text)
            if match:
                number, title = match.groups()
                courses.append({"number": number, "title": title})
        return courses
    except Exception:
        return []

def main():
    all_courses = []
    print(f"Using explicit department codes: {DEPARTMENT_CODES}")
    for code in DEPARTMENT_CODES:
        found_any = False
        suffixes = SUFFIXES_COURSE4 if code == "4" else SUFFIXES_GENERAL
        for suffix in suffixes:
            url = f"{BASE_URL}m{code}{suffix}.html"
            print(f"Trying {url} ...")
            dept_courses = extract_courses_from_dept(url)
            if dept_courses:
                print(f"  Found {len(dept_courses)} courses.")
                all_courses.extend(dept_courses)
                found_any = True
            time.sleep(0.2)
        if not found_any:
            print(f"  No courses found for department {code}.")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_courses, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(all_courses)} courses to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
