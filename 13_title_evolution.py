"""
13. Title Evolution

Conduct a word frequency analysis on course titles from 1996 and 2024
and compare the most common terms across both years.
"""

import json
import re
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

FILE_1996 = "10_mit_1996.json"
# Note: update this path if your 2024 data file uses a different name.
FILE_2024 = "11_mit_2026.json"

TOP_N = 20

STOPWORDS = {
	"a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "is",
	"of", "on", "or", "the", "to", "with", "without", "via", "ii", "iii",
	"i", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii",
	"advanced", "introduction", "intro", "seminar", "topics", "selected",
}


def load_titles(path):
	with open(path, encoding="utf-8") as f:
		data = json.load(f)
	return [item.get("title", "") for item in data]


def tokenize_titles(titles):
	tokens = []
	for title in titles:
		words = re.findall(r"[A-Za-z0-9']+", title.lower())
		for word in words:
			if word in STOPWORDS:
				continue
			if len(word) < 2:
				continue
			tokens.append(word)
	return tokens


def top_terms(tokens, n):
	return Counter(tokens).most_common(n)


def build_counts(tokens, vocab):
	counter = Counter(tokens)
	return [counter.get(term, 0) for term in vocab]


def main():
	titles_1996 = load_titles(FILE_1996)
	titles_2024 = load_titles(FILE_2024)

	tokens_1996 = tokenize_titles(titles_1996)
	tokens_2024 = tokenize_titles(titles_2024)

	top_1996 = top_terms(tokens_1996, TOP_N)
	top_2024 = top_terms(tokens_2024, TOP_N)

	terms_1996 = [term for term, _ in top_1996]
	terms_2024 = [term for term, _ in top_2024]
	overlap = set(terms_1996) & set(terms_2024)

	counts_1996 = [count for _, count in top_1996]
	counts_2024 = [count for _, count in top_2024]

	color_1996 = "#4F81BD"
	color_2024 = "#C0504D"
	terms_1996_labels = [f"{term}*" if term in overlap else term for term in terms_1996]
	terms_2024_labels = [f"{term}*" if term in overlap else term for term in terms_2024]

	fig, axes = plt.subplots(1, 2, figsize=(16, 10), sharex=False)

	y_1996 = np.arange(len(terms_1996))
	axes[0].barh(y_1996, counts_1996, color=color_1996)
	axes[0].set_yticks(y_1996)
	axes[0].set_yticklabels(terms_1996_labels)
	axes[0].invert_yaxis()
	axes[0].set_title("Top Terms in 1996")
	axes[0].set_xlabel("Word Frequency")
	axes[0].grid(axis="x", linestyle="--", alpha=0.5)

	y_2024 = np.arange(len(terms_2024))
	axes[1].barh(y_2024, counts_2024, color=color_2024)
	axes[1].set_yticks(y_2024)
	axes[1].set_yticklabels(terms_2024_labels)
	axes[1].invert_yaxis()
	axes[1].set_title("Top Terms in 2024")
	axes[1].set_xlabel("Word Frequency")
	axes[1].grid(axis="x", linestyle="--", alpha=0.5)

	fig.suptitle("Most Common Course Title Terms: 1996 vs 2024", fontsize=16)
	fig.text(0.5, 0.02, "* appears in both years", ha="center", fontsize=11)
	plt.tight_layout(rect=[0, 0.05, 1, 0.95])
	plt.savefig("title_word_frequency_1996_vs_2024.png")
	plt.show()


if __name__ == "__main__":
	main()

# Findings: many of the most common words in 1996 and 2024 were similar
# The top two most common words in each year were the same (just in a different order)
# Older courses use use words like "analysis" and "problems"
# Newer courses use words like "methods" and "history"