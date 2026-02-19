"""
14. New and Discontinued Subjects

Identify subjects offered in 1996 but not in 2024, and new subjects in 2024
that were not offered in 1996.
"""

import json
import math

import matplotlib.pyplot as plt

FILE_1996 = "10_mit_1996.json"
FILE_2024 = "11_mit_2026.json"
OUTPUT_FILE = "subjects_new_and_discontinued.json"
OUTPUT_PNG = "subjects_new_and_discontinued.png"
MAX_TITLES = 15


def load_subjects(path):
	with open(path, encoding="utf-8") as f:
		data = json.load(f)
	return [
		{"number": item.get("number"), "title": item.get("title")}
		for item in data
		if item.get("number") and item.get("title")
	]


def unique_titles_by_number(subjects, other_numbers):
	unique = [item for item in subjects if item["number"] not in other_numbers]
	unique.sort(key=lambda item: item["number"])
	return unique


def main():
	data_1996 = load_subjects(FILE_1996)
	data_2024 = load_subjects(FILE_2024)

	numbers_1996 = {item["number"] for item in data_1996}
	numbers_2024 = {item["number"] for item in data_2024}

	discontinued = unique_titles_by_number(data_1996, numbers_2024)
	new_subjects = unique_titles_by_number(data_2024, numbers_1996)

	discontinued_titles = [item["title"] for item in discontinued]
	new_subjects_titles = [item["title"] for item in new_subjects]

	visual_discontinued = discontinued_titles[:MAX_TITLES]
	visual_new = new_subjects_titles[:MAX_TITLES]

	result = {
		"1996_only": discontinued,
		"2024_only": new_subjects,
		"counts": {
			"1996_only": len(discontinued),
			"2024_only": len(new_subjects),
		},
		"visualized_titles": {
			"1996_only": visual_discontinued,
			"2024_only": visual_new,
		},
	}

	with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
		json.dump(result, f, ensure_ascii=False, indent=2)

	create_visual(visual_discontinued, visual_new, len(discontinued), len(new_subjects))

	print(f"1996 only: {len(discontinued)}")
	print(f"2024 only: {len(new_subjects)}")
	print(f"Saved results to {OUTPUT_FILE}")
	print(f"Saved visual to {OUTPUT_PNG}")


def create_visual(discontinued_titles, new_titles, discontinued_total, new_total):
	fig, axes = plt.subplots(1, 2, figsize=(16, 10))

	build_list_panel(
		axes[0],
		discontinued_titles,
		f"1996 Only (Top {MAX_TITLES})",
	)
	build_list_panel(
		axes[1],
		new_titles,
		f"2024 Only (Top {MAX_TITLES})",
	)

	fig.suptitle("Courses Present in Only One Year", fontsize=16)
	fig.text(
		0.5,
		0.02,
		f"Discontinued from 1996: {discontinued_total} | New in 2024: {new_total}",
		ha="center",
		fontsize=11,
	)
	plt.tight_layout(rect=[0, 0.05, 1, 0.95])
	plt.savefig(OUTPUT_PNG, dpi=200)
	plt.close(fig)


def build_list_panel(ax, items, title):
	ax.axis("off")
	ax.set_title(title, fontsize=12)

	if not items:
		ax.text(0.5, 0.5, "None", ha="center", va="center", fontsize=12)
		return

	max_rows = 40
	columns = max(1, math.ceil(len(items) / max_rows))
	columns = min(columns, 4)
	rows = math.ceil(len(items) / columns)

	font_size = 9 if rows <= 40 else 7

	col_width = 1.0 / columns
	for col in range(columns):
		start = col * rows
		end = min(start + rows, len(items))
		col_items = items[start:end]
		text = "\n".join(col_items)
		x = col * col_width + 0.02
		ax.text(x, 0.98, text, ha="left", va="top", fontsize=font_size, family="monospace")


if __name__ == "__main__":
	main()

# I noticed that topics that may have been "discontinued" may just have different names.
# For example, "Fluid Mechanics" is listed as discontinued, but there is a course called
# "Thermal-Fluids Engineering" which may cover similar material. 
# More courses have been added than were discontinued (2,164 discontinued and 4,877 added)
# This shows that the course offerings are increasing over time