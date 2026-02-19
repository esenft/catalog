# Extract course numbers and titles from 1996 PDF catalogs (Parts 1-8)
# Usage: python 10_extract_1996.py
# Output: 10_extract_1996.json

# Note: you must install pdfminer, pillow, pdf2image, poppler, tesseract, and pytesseract to run this script 


import requests
import re
import json
import io
from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract
import sys

PDF_URLS = [
	'https://onexi.org/catalog/pdf/01.pdf',
	'https://onexi.org/catalog/pdf/02.pdf',
	'https://onexi.org/catalog/pdf/03.pdf',
	'https://onexi.org/catalog/pdf/04.pdf',
	'https://onexi.org/catalog/pdf/05.pdf',
	'https://onexi.org/catalog/pdf/06.pdf',
	'https://onexi.org/catalog/pdf/07.pdf',
	'https://onexi.org/catalog/pdf/08.pdf',
]
OUTPUT_FILE = '10_extract_1996.json'

def download_pdf(url):
	print(f"Downloading {url}...")
	resp = requests.get(url)
	resp.raise_for_status()
	return resp.content

def extract_courses_from_text(text):
	# Extract course number and title pairs, skip prerequisites
	courses = []
	lines = text.splitlines()
	i = 0
	# Allow department codes with up to three alphanumeric characters (e.g., 21A, 21M, HST, MAS, etc.)
	course_pat = re.compile(r'^((?:[A-Z0-9]{1,3}\.[0-9]{2,4}[A-Z]?J?|[A-Z0-9]{1,3}\.[A-Za-z]{2,4}J?)(?:[,-]\s*(?:[A-Z0-9]{1,3}\.[0-9]{2,4}[A-Z]?J?|[A-Z0-9]{1,3}\.[A-Za-z]{2,4}J?))*)\s+(.+)$')
	# Preprocess lines to remove extra spaces in course numbers (e.g., '2 1 A . 2 1 5' -> '21A.215')
	def normalize_course_number(num):
		# Remove spaces around dots and between letters/numbers
		num = re.sub(r'\s*\.\s*', '.', num)
		num = re.sub(r'\s+', '', num)
		return num
	non_title_pat = re.compile(r'^(Prereq:|\(Same subject as|\(Subject meets with|\-+$)', re.IGNORECASE)
	i = 0
	while i < len(lines):
		line = lines[i].strip()
		match = course_pat.match(line)
		if match:
			number, title = match.groups()
			number = normalize_course_number(number)
			# Collect additional lines for long titles
			j = i + 1
			while j < len(lines):
				next_line = lines[j].strip()
				# Stop at next course, known non-title, or horizontal line
				if course_pat.match(next_line) or non_title_pat.match(next_line) or not next_line:
					break
				title += ' ' + next_line
				j += 1
			if len(number) > 2 and len(title) > 2:
				courses.append({'number': number, 'title': title})
			i = j
		else:
			i += 1
	return courses

def main(start_part=1):
	# If output file exists and resuming, load previous results
	all_courses = []
	if start_part > 1:
		try:
			with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
				all_courses = json.load(f)
			print(f"Loaded {len(all_courses)} courses from previous run.")
		except Exception:
			print("No previous output found or failed to load, starting fresh from part", start_part)
	for idx, url in enumerate(PDF_URLS, 1):
		if idx < start_part:
			continue
		pdf_bytes = download_pdf(url)
		print(f"Converting PDF part {idx} to images...")
		images = convert_from_bytes(pdf_bytes)
		print(f"Performing OCR on {len(images)} pages from part {idx}...")
		for page_num, image in enumerate(images, 1):
			# Skip pages 1, 2, 3 of part 1 (not course data)
			if idx == 1 and page_num in (1, 2, 3):
				print(f"  Skipping page {page_num} of part 1 (not course data)")
				continue
			text = pytesseract.image_to_string(image)
			courses = extract_courses_from_text(text)
			print(f"  Page {page_num}: {len(courses)} courses found.")
			all_courses.extend(courses)
		# Save progress after each part
		with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
			json.dump(all_courses, f, ensure_ascii=False, indent=2)
		print(f"Saved progress: {len(all_courses)} courses to {OUTPUT_FILE}")
	print(f"Finished. Total courses: {len(all_courses)} saved to {OUTPUT_FILE}")

if __name__ == '__main__':
	# Allow optional command-line argument to start at a specific part
	start_part = 1
	if len(sys.argv) > 1:
		try:
			start_part = int(sys.argv[1])
		except Exception:
			print("Invalid argument for start part, using 1.")
	main(start_part)
# -----------------------------------------------
#  10. Catalog 1996
# 
#  Extract course data from the scanned 
#  1996 MIT course catalog. After extracting 
#  the text, create a data model and save the 
#  processed data. This task emphasizes 
#  working with raw, scanned documents 
#  and aims to teach you how to extract 
#  information from non-digitized sources.
# -----------------------------------------------
