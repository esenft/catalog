# -----------------------------------------------
#  5. Data Extraction:
# 
#  Objective: Extract course titles from 
#  the data you cleaned.

# For this task, I set myself up well for data extraction by ensuring previous steps had a well-defined structure for each course
# I had split up each course into four fields: course number, title, credits, and description
# I identified course titles from the HTML files by recoginizing that they were bold and followed a specific pattern (course number, title, credits in parentheses)
# This made it easy to extract just the course titles in this step by reading the cleaned TSV 

import csv

INPUT_FILE = 'cleaned_courses.tsv'
OUTPUT_FILE = 'course_titles.txt'

def extract_course_titles():
	course_titles = []
	with open(INPUT_FILE, 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f, delimiter='\t')
		for row in reader:
			number = row['number'].strip()
			title = row['title'].strip()
			if number and title:
				course_titles.append(f"{number}: {title}")
	return course_titles

def save_titles(titles, out_file):
	with open(out_file, 'w', encoding='utf-8') as f:
		for t in titles:
			f.write(t + '\n')

def main():
	titles = extract_course_titles()
	save_titles(titles, OUTPUT_FILE)
	print(f"Extracted {len(titles)} course titles to {OUTPUT_FILE}")

if __name__ == '__main__':
	main()
# -----------------------------------------------
