import csv
import re

# Preprocess and normalize titles
def preprocess_title(title):
    title = re.sub(r'\bMt\.\b', 'Mount', title, flags=re.IGNORECASE)
    return title.title()

def extract_data(filename):
    # Extract and preprocess data from filename
    # Save to an intermediate file
    pass

# Example function call
extract_data('./data_sets/The Joy Of Painiting - Colors Used')
