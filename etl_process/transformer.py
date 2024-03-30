import pandas as pd

def transform_data(input_file):
    # Load data
    df = pd.read_csv(input_file)

    # Perform transformation operations
    # Example: df['new_column'] = df['existing_column'].apply(transformation_logic)

    # Save transformed data
    df.to_csv('transformed_data.csv', index=False)

# Example function call
transform_data('preprocessed_data.csv')
