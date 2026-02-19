import json
from collections import Counter

with open('10_extract_1996.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total courses: {len(data)}\n")

# Print a few sample courses from the start, middle, and end
print("First 5 courses:")
for course in data[:5]:
    print(course)

print("\nMiddle 5 courses:")
mid = len(data) // 2
for course in data[mid:mid+5]:
    print(course)

print("\nLast 5 courses:")
for course in data[-5:]:
    print(course)

# Check for duplicate course numbers
numbers = [c['number'] for c in data]
dupes = [item for item, count in Counter(numbers).items() if count > 1]
if dupes:
    print(f"\nDuplicate course numbers found: {dupes}")
else:
    print("\nNo duplicate course numbers found.")
