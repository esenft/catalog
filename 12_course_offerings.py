# -----------------------------------------------
#  12. Course Offerings Over Time
# 
#  After extracting the course data from 
#  both the 1996 and present catalogs, 
#  analyze the number of courses offered 
#  in various departments. Are there any 
#  departments that have significantly 
#  expanded or reduced their course offerings? 
#  If so, identify them and discuss possible 
#  reasons for these changes.
# -----------------------------------------------

# To run code, must install matplotlib library

import json
import re
import matplotlib.pyplot as plt
import numpy as np

# Load course data
with open('10_mit_1996.json', encoding='utf-8') as f:
    data_1996 = json.load(f)
with open('11_mit_2026.json', encoding='utf-8') as f:
    data_2026 = json.load(f)

# Extract department from course number (1-3 letters/numbers before period)
def get_dept(course_number):
    m = re.match(r'^([A-Z0-9]{1,3})\.', course_number)
    return m.group(1) if m else None

# Count courses per department for each year
def count_courses(data):
    dept_counts = {}
    for course in data:
        dept = get_dept(course['number'])
        if dept:
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
    return dept_counts

counts_1996 = count_courses(data_1996)
counts_2026 = count_courses(data_2026)

# Union of all departments
all_depts = sorted(set(counts_1996) | set(counts_2026))

vals_1996 = [counts_1996.get(dept, 0) for dept in all_depts]
vals_2026 = [counts_2026.get(dept, 0) for dept in all_depts]

x = np.arange(len(all_depts)) * 2  # Increase spacing between bars
width = 0.7

fig, ax = plt.subplots(figsize=(22, 10))

# Horizontal grouped bar chart
bar_1996 = ax.bar(x - width/2, vals_1996, width, color='#4F81BD', label='1996')
bar_2026 = ax.bar(x + width/2, vals_2026, width, color='#C0504D', label='2026')

ax.set_ylabel('Number of Courses', fontsize=16)
ax.set_xlabel('Department', fontsize=16)
ax.set_title('Course Offerings by Department: 1996 vs 2026', fontsize=20, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(all_depts, rotation=45, ha='right', fontsize=14)
ax.legend(fontsize=14)

# Add grid and value labels
ax.grid(axis='y', linestyle='--', alpha=0.7)
for i, (v96, v26) in enumerate(zip(vals_1996, vals_2026)):
    if v96 > 0:
        ax.text(x[i] - width/2, v96 + 2, str(v96), ha='center', color='#4F81BD', fontsize=12, fontweight='bold')
    if v26 > 0:
        ax.text(x[i] + width/2, v26 + 2, str(v26), ha='center', color='#C0504D', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('course_offerings_comparison.png')
plt.show()
