import csv
import re
import os


# Preprocess and normalize titles
def preprocess_title(title):
    # Explicitly handle different scenarios for "Mt." to "Mount" conversion
    # 1. "Mt." at the start of a title
    title = re.sub(r'^Mt\.\s+', 'Mount ', title, flags=re.IGNORECASE)
    # 2. "Mt." in the middle or end, ensuring it's not part of "Mountain"
    title = re.sub(r'\s+Mt\.\s*', ' Mount ', title, flags=re.IGNORECASE)
    # 3. "Mt." followed by punctuation (e.g., at the end of a sentence/title)
    title = re.sub(r'\s+Mt\.\b', ' Mount', title, flags=re.IGNORECASE)
    return title.title()


def preprocess_episode_dates(input_filename, output_filename):
    pattern = re.compile(r'"([^"]+)" \(([^)]+)\)')
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(input_filename, 'r', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['painting_title', 'broadcast_date'])

        for line in infile:
            match = pattern.match(line)
            if match:
                title, date = match.groups()
                title = preprocess_title(title)
                writer.writerow([title, date])


def preprocess_subject_matter(input_filename, output_filename):
    # Extract title and subjects,
    # preparing for the `subjects` table and `episodes_subjects`
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(input_filename, newline='', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['painting_title',
                                                     'subjects'])
        writer.writeheader()

        for row in reader:
            painting_title = preprocess_title(row['TITLE'].strip('"'))
            # Skip EPISODE and TITLE, start from the 3rd column
            subjects = [subject for subject in reader.fieldnames[2:]
                        if row[subject] == '1']
            writer.writerow({
                'painting_title': painting_title,
                # Join subjects with a semicolon (separator)
                'subjects': '; '.join(subjects)
            })


def preprocess_colors_used(input_filename, output_filename):
    # Extract painting titles, color names, and hex codes
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(input_filename, newline='', encoding='utf-8') as infile, \
         open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['painting_title',
                                                     'colors', 'color_hex'])
        writer.writeheader()

        for row in reader:
            row['painting_title'] = preprocess_title(row['painting_title'])
            writer.writerow({
                'painting_title': row['painting_title'],
                'colors': row.get('colors', ''),
                'color_hex': row.get('color_hex', '')
            })


# Colors Used Processing
input_filename = (
    '../data_sets/'
    'The Joy Of Painiting - Colors Used'
)
output_filename = (
    '../preprocessed_data/preprocessed_colors.csv'
)
preprocess_colors_used(input_filename, output_filename)

# Subject Matter
input_filename = (
    '../data_sets/'
    'The Joy Of Painiting - Subject Matter'
)
output_filename = (
    '../preprocessed_data/preprocessed_subjects.csv'
)
preprocess_subject_matter(input_filename, output_filename)

# Episode Dates
input_filename = (
    '../data_sets/'
    'The Joy Of Painting - Episode Dates'
)
output_filename = (
    '../preprocessed_data/preprocessed_dates.csv'
)
preprocess_episode_dates(input_filename, output_filename)
