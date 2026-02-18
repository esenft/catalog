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
	# This selector may need adjustment based on actual HTML structure
	# Try to find all course blocks (commonly div, tr, or li)
	for course_block in soup.find_all(['div', 'tr', 'li'], class_=re.compile(r'course', re.I)):
		text = course_block.get_text(separator=' ', strip=True)
		# Regex to extract course number, title, credits, description
		# Example: "CS 101 Introduction to Programming (3 credits) Description..."
		match = re.match(r'([A-Z]{2,4} ?\d{3,4}[A-Z]?)\s+(.+?)\s*\((\d+(?:\.\d+)?)\s*credits?\)\s*(.*)', text)
		if match:
			number, title, credits, description = match.groups()
			courses.append({
				'number': number.strip(),
				'title': title.strip(),
				'credits': credits.strip(),
				'description': description.strip()
			})
		else:
			# Fallback: try to extract with less strict pattern
			parts = text.split(' ', 2)
			if len(parts) >= 3:
				number, title, rest = parts[0], parts[1], parts[2]
				credits_match = re.search(r'(\d+(?:\.\d+)?)\s*credits?', rest, re.I)
				credits = credits_match.group(1) if credits_match else ''
				description = rest.split(')', 1)[-1].strip() if ')' in rest else rest
				courses.append({
					'number': number.strip(),
					'title': title.strip(),
					'credits': credits.strip(),
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
