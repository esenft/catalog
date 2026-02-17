# -----------------------------------------------
#  2. Data Preparation:
# 
#  Objective: Combine multiple HTML files into 
#  a single document.
# 
#  Tools/Resources: Concatenate HTML text using 
#  python or javascript.
# -----------------------------------------------
import os

# Directory where HTML files are stored (assumed from 01_pull.py output)
HTML_DIR = "catalog_html" # the folder where HTML files are stored
OUTPUT_FILE = "combined.html" # the name of the file where all HTML content will be combined

# Step 1: Gather all HTML files from the HTML directory specified above
# Runs a function to list HTML files 
def get_html_files(directory):
    """Return a list of HTML file paths in the given directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if f.endswith('.html') and os.path.isfile(os.path.join(directory, f))]

# Step 2: Concatenate the contents of all HTML files into a single output file
# Each HTML file is opened, read, and written into the output file with a new line separating them for clarity
def concatenate_html_files(file_list, output_file):
    """Concatenate the contents of HTML files into a single output file."""
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for fname in file_list:
            with open(fname, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n')  # Separate files with a newline

# Main execution block: checks if script is being run directly and then executes the file gathering and concatenation process
if __name__ == "__main__":
    html_files = get_html_files(HTML_DIR)
    if not html_files:
        print(f"No HTML files found in directory '{HTML_DIR}'.")
    else:
        concatenate_html_files(html_files, OUTPUT_FILE)
        print(f"Combined {len(html_files)} HTML files into '{OUTPUT_FILE}'.")

# Note: this file does not modify the HTML content, so the original structure of each file is preserved