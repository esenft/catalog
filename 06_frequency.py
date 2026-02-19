# -----------------------------------------------
#  6. Word Frequency Analysis:
# 
#  Objective: Perform a word frequency count 
#  on the course titles.
# 
#  Tools/Resources: You can use a “map reduce” 
#  style word counting approach.
# -----------------------------------------------

# Word Frequency Analysis on course_titles.txt using MapReduce approach
import string
from collections import Counter

# Define a set of common English stopwords
STOPWORDS = set([
	'the', 'and', 'in', 'of', 'to', 'a', 'for', 'on', 'with', 'at', 'by', 'an', 'be', 'is', 'as', 'from', 'that',
	'this', 'it', 'are', 'or', 'was', 'but', 'not', 'which', 'into', 'can', 'has', 'have', 'will', 'its', 'if', 'their',
	'also', 'we', 'our', 'they', 'you', 'all', 'more', 'than', 'one', 'about', 'so', 'do', 'no', 'may', 'such', 'these',
	'out', 'up', 'use', 'used', 'using', 'each', 'other', 'new', 'some', 'most', 'any', 'who', 'what', 'when', 'where',
	'how', 'why', 'been', 'being', 'through', 'over', 'under', 'between', 'both', 'after', 'before', 'during', 'while',
	'per', 'upon', 'within', 'without', 'like', 'just', 'should', 'could', 'would', 'very', 'much', 'many', 'them', 'he', 'she', 'his', 'her', 'i', 'me', 'my', 'your', 'yours', 'ours', 'theirs', 'him', 'hers', 'itself', 'themselves', 'ourselves', 'yourself', 'yourselves'
])

# Define a function to preprocess the text
def preprocess(text):
	# Lowercase, remove punctuation, split into words, remove stopwords
	text = text.lower() # convert all words to lowercase so capitalizaiton doesn't affect the count
	text = text.translate(str.maketrans('', '', string.punctuation))
	words = text.split()
	# Exclude stopwords and words that are purely numeric
	# I added this in because there was "1" and "2" being counted as common words in course titles
	return [word for word in words if word not in STOPWORDS and not word.isdigit()]

# Employ a MapReduce style approach to count word frequencies
def map_words(lines):
	# Map step: emit (word, 1) for each word
	for line in lines:
		for word in preprocess(line):
			yield (word, 1)

# Aggregate the counts for each word
def reduce_word_counts(pairs):
	# Reduce step: aggregate counts for each word
	counter = Counter()
	for word, count in pairs:
		counter[word] += count
	return counter

def main():
	with open('course_titles.txt', 'r', encoding='utf-8') as f:
		lines = f.readlines()
	# Map
	mapped = list(map_words(lines))
	# Reduce
	word_counts = reduce_word_counts(mapped)
	# Print top 20 most common words
	for word, count in word_counts.most_common(20):
		print(f'{word}: {count}')

if __name__ == '__main__':
	main()


