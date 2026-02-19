# -----------------------------------------------
#  9. Data pipeline:
# 
#  Write a program that automates the 
#  sequential execution of previously created 
#  script files, ensuring that each script 
#  runs to completion before the next begins. 
#  This program aims to streamline the 
#  generation of outputs from all your 
#  previous files, consolidating the 
#  results into one sequence.
# -----------------------------------------------

# Pipeline to automate sequential execution of scripts 01-08
import subprocess
import sys
import os

SCRIPTS = [
	'01_pull.py',
	'02_combine.py',
	'03_parse.py',
	'04_clean.py',
	'05_extract.py',
	'06_frequency.py',
	'07_visualization.py',
	'08_export.py',
]

# Add in indicators to show progress 
def run_script(script):
	print(f"Starting {script}...")
	try:
		result = subprocess.run([sys.executable, script], check=True, capture_output=True, text=True)
		print(result.stdout)
		print(f"{script} completed.\n")
	except subprocess.CalledProcessError as e:
		print(f"Error running {script}:")
		print(e.stdout)
		print(e.stderr)
		print(f"Pipeline stopped at {script} due to error.")
		sys.exit(1)

def main():
	for script in SCRIPTS:
		if not os.path.exists(script):
			print(f"Script {script} not found. Skipping.")
			continue
		run_script(script)
	print("Pipeline completed successfully. All outputs generated.")

if __name__ == '__main__':
	main()


