# -----------------------------------------------
#   4. Data Cleaning:
# 
#   Objective: Clean and preprocess the 
#   extracted data for analysis.
# 
#   Tools/Resources: Use Regular Expressions 
#   or string manipulation functions in 
#   your programming language.
# -----------------------------------------------

# Initially, this code was not cleaning anything (0 cleaned rows were being saved)
# This is likely due to a cleaning script that was too aggressive, removing all rows as invalid 
# This was fixed by adjusting the validation logic to allow for non-breaking spaces in course numbers and to be more flexible with credit formats
# After the fix, all 7,913 rows were saved to the cleaning_courses.tsv file

# Imports re library for regular expressions
import re

# Input and output file paths
INPUT_FILE = 'parsed_courses.tsv'
OUTPUT_FILE = 'cleaned_courses.tsv'

# Defining function to clean individual fields by trimming whitespace, removing non-printable charcters, replacing multiple spaces with a single space, and removing trailing punctuation (except periods)
def clean_field(value):
	"""
	Cleans a single field: trims whitespace, removes problematic characters, standardizes format.
	"""
	value = value.strip()
	# Remove non-printable/control characters
	value = re.sub(r'[\x00-\x1F\x7F]', '', value)
	# Replace multiple spaces/tabs with a single space
	value = re.sub(r'[ \t]+', ' ', value)
	# Remove trailing punctuation (except period)
	value = re.sub(r'([,;:])+$', '', value)
	return value

# Defining function to clean each field in a row using the clean_field function
def clean_row(row):
	"""
	Cleans a row (list of fields).
	"""
	return [clean_field(field) for field in row]

# Defining function to check if a row is valid for downstream parsing 
def is_valid_row(row):
	"""
	Checks if a row is valid for downstream parsing.
	"""
	# Must have exactly 4 fields
	if len(row) != 4:
		return False
	# Course number must match pattern (allow non-breaking space)
	if not re.match(r'^[A-Z]{2,4}[\s\xa0]?\d{3,4}[A-Z]?$', row[0]):
		return False
	# Credits must be a number or range (e.g., '1-4', '3', '3.5')
	if not re.match(r'^\d+(\.\d+)?(-\d+(\.\d+)?)?$', row[2]):
		return False
	return True

# Defining function to read input file, clean each row, and validate them
# Collects valid rows for output
def clean_data():
	cleaned_rows = []
	with open(INPUT_FILE, 'r', encoding='utf-8') as f:
		lines = f.readlines()
	header = lines[0].strip().split('\t')
	for line in lines[1:]:
		row = line.strip().split('\t')
		row = clean_row(row)
		if is_valid_row(row):
			cleaned_rows.append(row)
	return header, cleaned_rows

# Writes the cleaned header and rows to output file
def save_cleaned_data(header, rows, out_file):
	with open(out_file, 'w', encoding='utf-8') as f:
		f.write('\t'.join(header) + '\n')
		for row in rows:
			f.write('\t'.join(row) + '\n')

# Run cleaning and saving functions, and prints a confirmation message with the number of cleaned rows saved to the output file
def main():
	header, cleaned_rows = clean_data()
	save_cleaned_data(header, cleaned_rows, OUTPUT_FILE)
	print(f"Cleaned {len(cleaned_rows)} rows saved to {OUTPUT_FILE}")

if __name__ == '__main__':
	main()
