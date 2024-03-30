import psycopg2
import csv
import re
from datetime import datetime

# Database connection parameters
conn = psycopg2.connect("dbname=joy_of_painting user=root password=root")
cur = conn.cursor()

# Preprocess and normalize titles
def preprocess_title(title):
    title = re.sub(r'\bMt\.\b', 'Mount', title, flags=re.IGNORECASE)
    return title.title()

# Insert data from the master list
def insert_master_list(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Assuming preprocess_title() is defined and implemented
            painting_title = preprocess_title(row['painting_title'])
            # Insert episode data along with season and episode numbers

# Insert data from other datasets, matching on painting_title
def insert_additional_data(filename):
    # Implementation depends on the dataset structure
    return

# Parse and insert episode dates with special handling for inconsistencies
def insert_episode_dates(filename):
    pattern = re.compile(r'"([^"]+)" \(([^)]+)\)(?: (Special guest|Footage with)?(.*))?')
    with open(filename, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                title, air_date_str, note_type, note = match.groups()
                title = preprocess_title(title)
                air_date = datetime.strptime(air_date_str, '%B %d, %Y').date()
                # Insert or update the database record for this episode

# Call the functions to process and insert data
insert_master_list('./data_sets/The Joy Of Painiting - Colors Used')
insert_additional_data('./data_sets/The Joy Of Painiting - Subject Matter')
insert_episode_dates('./data_sets/The Joy Of Painting - Episode Dates')

# Commit changes and close the database connection
conn.commit()
cur.close()
conn.close()
