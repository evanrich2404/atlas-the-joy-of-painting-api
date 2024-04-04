import pandas as pd
import os


def transform_subject_matter(input_filename, output_filename):
    # Read the CSV file
    df = pd.read_csv(input_filename)

    # Split the 'subjects' column into a list of subjects
    df['subjects'] = df['subjects'].str.split('; ')

    # Explode the DataFrame to have a separate row for each subject
    exploded_df = df.explode('subjects')

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    # Save the exploded DataFrame to a new CSV file
    exploded_df.to_csv(output_filename, index=False)


input_filename = '../preprocessed_data/preprocessed_subjects.csv'
output_filename = '../transformed_data/transformed_subjects.csv'
transform_subject_matter(input_filename, output_filename)
