"""
15. Curriculum Breadth

Compare topic breadth in 1996 vs 2024 catalogs to assess interdisciplinarity
vs specialization using department diversity and cross-listing signals.
"""

import json
import math
import re

import matplotlib.pyplot as plt

FILE_1996 = "10_mit_1996.json"
FILE_2024 = "11_mit_2026.json"
OUTPUT_JSON = "curriculum_breadth_summary.json"
OUTPUT_PNG = "curriculum_breadth_summary.png"


def load_courses(path):
	with open(path, encoding="utf-8") as f:
		return json.load(f)


def dept_from_number(number):
	match = re.match(r"^([A-Z0-9]{1,3})\.", number)
	return match.group(1) if match else None


def is_cross_listed(number):
	# Heuristic: joint subjects often use J or list multiple numbers with commas/dashes.
	return ("J" in number) or ("," in number) or ("-" in number)


def shannon_entropy(counts):
	total = sum(counts)
	if total == 0:
		return 0.0
	entropy = 0.0
	for count in counts:
		p = count / total
		if p > 0:
			entropy -= p * math.log(p)
	return entropy


def summarize(courses):
	dept_counts = {}
	interdisciplinary = 0
	for item in courses:
		number = item.get("number", "")
		dept = dept_from_number(number)
		if dept:
			dept_counts[dept] = dept_counts.get(dept, 0) + 1
		if number and is_cross_listed(number):
			interdisciplinary += 1

	total = len(courses)
	unique_depts = len(dept_counts)
	entropy = shannon_entropy(list(dept_counts.values()))
	interdisciplinary_pct = (interdisciplinary / total) * 100 if total else 0

	return {
		"total_courses": total,
		"unique_departments": unique_depts,
		"dept_entropy": entropy,
		"interdisciplinary_count": interdisciplinary,
		"interdisciplinary_pct": interdisciplinary_pct,
		"dept_counts": dept_counts,
	}


def main():
	courses_1996 = load_courses(FILE_1996)
	courses_2024 = load_courses(FILE_2024)

	summary_1996 = summarize(courses_1996)
	summary_2024 = summarize(courses_2024)

	result = {
		"1996": summary_1996,
		"2024": summary_2024,
	}

	with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
		json.dump(result, f, ensure_ascii=False, indent=2)

	create_visual(summary_1996, summary_2024)

	print("Saved summary to", OUTPUT_JSON)
	print("Saved visual to", OUTPUT_PNG)


def create_visual(summary_1996, summary_2024):
	fig, axes = plt.subplots(1, 2, figsize=(14, 6))

	# Unique Departments
	vals_depts = [summary_1996["unique_departments"], summary_2024["unique_departments"]]
	axes[0].bar(["1996", "2024"], vals_depts, color=["#4F81BD", "#C0504D"])
	axes[0].set_title("Unique Departments")
	axes[0].set_ylabel("Count")
	axes[0].grid(axis="y", linestyle="--", alpha=0.4)
	for i, v in enumerate(vals_depts):
		axes[0].text(i, v + 1, str(v), ha="center", fontweight="bold")

	# Joint Courses
	vals_joint = [summary_1996["interdisciplinary_count"], summary_2024["interdisciplinary_count"]]
	axes[1].bar(["1996", "2024"], vals_joint, color=["#4F81BD", "#C0504D"])
	axes[1].set_title("Joint Courses")
	axes[1].set_ylabel("Count")
	axes[1].grid(axis="y", linestyle="--", alpha=0.4)
	for i, v in enumerate(vals_joint):
		axes[1].text(i, v + 2, str(v), ha="center", fontweight="bold")

	fig.suptitle("Curriculum Breadth: 1996 vs 2024", fontsize=14)

	plt.tight_layout()
	plt.savefig(OUTPUT_PNG, dpi=200)
	plt.close(fig)


if __name__ == "__main__":
	main()


# Discoveries: the two measures I focused on for the cirriculum breadth were the number of unique departments and the number of joint courses
# There are more unique departments in 2024 than in 1996, which suggests that the curriculum has become more specialized
# However, there are more joint courses in 2024, which suggests that the curriculum has become more interdisciplinary with topics covering different departments.
# Overall, with the increased number of courses in 2024, I would conclude that the cirriculum has become more specialized.