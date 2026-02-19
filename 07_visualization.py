# -----------------------------------------------
#  7. Data Visualization:
#  Objective: Visualize the word frequencies
#  using a visualization library.
# 
#  Tools/Resources: Examples of visualization 
#  libraries D3, Plotly, and Chart.JS.
#     D3, https://d3js.org/
#     Plotly, https://plotly.com/
#     Chart.JS, https://www.chartjs.org/
#     Google Charts, https://developers.google.com/chart/
# -----------------------------------------------

# Visualization of Word Frequencies using Google Charts
import json

def load_word_frequencies(filename):
	"""
	Loads the word frequency data from 06_frequency.py output.
	Here, we expect a file 'word_frequencies.json' with {"word": count, ...} format.
	Returns all words sorted by frequency (descending).
	"""
	with open(filename, 'r', encoding='utf-8') as f:
		data = json.load(f)
	sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
	return sorted_items[:20]

# I chose to use Google Charts since it is easy to use and is slightly interactive
# I also decided to use a stacked bar chart since it clearly shows a comparison of the frequencies
# I was considering doing a word cloud with different sized words to show the frequencies, but this was not supported with Google Charts so I went with a simple representation.
def generate_google_bar_chart_html(word_counts, output_html):
		"""
		Generates an HTML file with a Google Charts bar chart for word frequencies.
		"""
		# Prepare data rows for Google Charts
		data_rows = ",\n        ".join([
				f"['{word}', {count}]" for word, count in word_counts
		])
		data_rows = ",\n        ".join([
				f"['{word}', {count}]" for word, count in word_counts
		])
		html = f"""
<html>
	<head>
		<script type=\"text/javascript\" src=\"https://www.gstatic.com/charts/loader.js\"></script>
		<script type=\"text/javascript\">
			google.charts.load('current', {{packages:['corechart']}});
			google.charts.setOnLoadCallback(drawChart);
			function drawChart() {{
				var data = google.visualization.arrayToDataTable([
					['Word', 'Frequency'],
					{data_rows}
				]);
				var options = {{
					title: 'Top Word Frequencies in Course Titles',
					legend: {{ position: 'none' }},
					chartArea: {{width: '70%'}},
					hAxis: {{ minValue: 0 }},
					bar: {{ groupWidth: '90%' }},
					vAxis: {{
						textStyle: {{ fontSize: 14 }},
						slantedText: false,
						showTextEvery: 1
					}}
				}};
				var chart = new google.visualization.BarChart(document.getElementById('barchart'));
				chart.draw(data, options);
			}}
		</script>
	</head>
	<body>
		<div id=\"barchart\" style=\"width: 900px; height: 600px;\"></div>
	</body>
</html>
"""
		with open(output_html, 'w', encoding='utf-8') as f:
				f.write(html)

def main():
		# You must first export the word frequency data to a JSON file from 06_frequency.py
		# For demonstration, expects 'word_frequencies.json' in the same directory
		word_counts = load_word_frequencies('word_frequencies.json')
		generate_google_bar_chart_html(word_counts, 'word_frequencies_chart.html')
		print('Bar chart saved to word_frequencies_chart.html')

if __name__ == '__main__':
		main()

