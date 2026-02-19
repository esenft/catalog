# -----------------------------------------------
#  8. Export a Clean Formatted Dataset
#  of the Entire University Catalog:
# 
#  Export a Clean Formatted Dataset of 
#  the Entire University Catalog: The 
#  dataset you would have liked when you 
#  started. Prepare and export a clean, 
#  well-formatted dataset encompassing 
#  the entire university catalog. This 
#  dataset should be in a form that is 
#  readily usable for analysis and 
#  visualization, reflecting the cleaned 
#  and consolidated data you've worked 
#  with throughout the project. Document 
#  the structure of your dataset, including 
#  a description of columns, data types, and 
#  any assumptions or decisions made during 
#  the data preparation process.
# -----------------------------------------------

# 8. Export Cleaned University Catalog Dataset
#
# This script exports the cleaned, well-formatted dataset of the entire university catalog.
# It uses the output from 04_clean.py (cleaned_courses.tsv), which includes all information (number, title, credits, description).
# The export is written as a CSV file for easy use in analysis and visualization.

import csv

INPUT_FILE = 'cleaned_courses.tsv'
EXPORT_FILE = 'catalog_export.csv'

def export_cleaned_catalog():
	with open(INPUT_FILE, 'r', encoding='utf-8') as fin, open(EXPORT_FILE, 'w', encoding='utf-8', newline='') as fout:
		reader = (line.rstrip('\n').split('\t') for line in fin)
		writer = csv.writer(fout)
		for row in reader:
			writer.writerow(row)
	print(f"Exported cleaned catalog to {EXPORT_FILE}")

if __name__ == '__main__':
	export_cleaned_catalog()

