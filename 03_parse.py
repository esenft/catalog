# -----------------------------------------------
#   3. Data Parsing:
# 
#   Objective: Parse course data leveraging
#   HTML elements structure.
# 
#   Tools/Resources: Use resources like the 
#   DOMParser, BeautifulSoup, or Regular Expressions.
#       Beautiful Soup:
#           https://www.crummy.com/software/BeautifulSoup/
#       DOMParser:
#           https://developer.mozilla.org/en-US/docs/Web/API/DOMParser
#       RegEx:
#           https://regexr.com 
#           https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions
# -----------------------------------------------
import os
from bs4 import BeautifulSoup # Import Beautiful Soup for HTML parsing
import re

# Directory containing the consolidated HTML files
HTML_DIR = 'catalog_html'

# Output file for parsed course data
OUTPUT_FILE = 'parsed_courses.tsv'

# In this function, I am aiming to extract the course number, title, credits, and description from the HTML content.
def extract_course_info(soup):
	"""
	Extracts course information from a BeautifulSoup object.
	Returns a list of dicts with keys: number, title, credits, description.
	"""
	courses = []
	# Find all course blocks (div, tr, li with class containing 'course')
	for courseblock in soup.find_all('div', class_='courseblock'):
		title_tag = courseblock.find('p', class_='courseblocktitle')
		desc_tag = courseblock.find('p', class_='cb_desc')
		if not title_tag or not title_tag.find('strong'):
			continue
		title_str = title_tag.find('strong').get_text(strip=True)
		# Regex: ACCT 1201.  Financial Accounting and Reporting.  (4 Hours)
		match = re.match(r'^([A-Z]{2,4}\s*\d{3,4}[A-Z]?)\.\s*(.*?)\.\s*\((\d+(?:-\d+)?(?:\.\d+)?)\s*Hours?\)$', title_str)
		if match:
			number, title, credits = match.groups()
			description = desc_tag.get_text(strip=True) if desc_tag else ''
			courses.append({
				'number': number.strip(),
				'title': title.strip(),
				'credits': credits.strip(),
				'description': description.strip()
			})
		else:
			# Fallback: try to extract number and title only
			fallback_match = re.match(r'^([A-Z]{2,4}\s*\d{3,4}[A-Z]?)\.\s*(.*?)\.$', title_str)
			if fallback_match:
				number, title = fallback_match.groups()
				description = desc_tag.get_text(strip=True) if desc_tag else ''
				courses.append({
					'number': number.strip(),
					'title': title.strip(),
					'credits': '',
					'description': description.strip()
				})
	return courses

# Iterate through all files in the HTML directory
def parse_html_files():
	all_courses = []
	for fname in sorted(os.listdir(HTML_DIR)):
		if not fname.endswith('.html'):
			continue
		fpath = os.path.join(HTML_DIR, fname)
		with open(fpath, 'r', encoding='utf-8') as f:
			soup = BeautifulSoup(f, 'html.parser')
			courses = extract_course_info(soup) # calling the function defined earlier
			all_courses.extend(courses)
	return all_courses

# Take the list of courses and write them to a tab-separated values file
# Organization: the first line is the header (number, title, credits, description), followed by one line per course with the corresponding data separated by tabs
def save_courses(courses, out_file):
	with open(out_file, 'w', encoding='utf-8') as f:
		f.write('number\ttitle\tcredits\tdescription\n')
		for c in courses:
			f.write(f"{c['number']}\t{c['title']}\t{c['credits']}\t{c['description']}\n")

# Execute the function and save courses to the ouptut file
def main():
	courses = parse_html_files()
	save_courses(courses, OUTPUT_FILE)
	print(f"Extracted {len(courses)} courses to {OUTPUT_FILE}") # Confirmation message

if __name__ == '__main__':
	main()
