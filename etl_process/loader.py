from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# Retrieve database connection details from environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

# Database URI
DATABASE_URI = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

engine = create_engine(DATABASE_URI)

def load_episodes(filename):
    df = pd.read_csv(filename)
    with engine.begin() as conn:
        for index, row in df.iterrows():
            conn.execute(
                text("INSERT INTO episodes(painting_title, broadcast_date) VALUES (:painting_title, :broadcast_date) ON CONFLICT (painting_title) DO NOTHING;"),
                {"painting_title": row['painting_title'], "broadcast_date": row['broadcast_date']}
            )

def load_colors(filename):
    df = pd.read_csv(filename).drop_duplicates(subset=['color_name', 'color_hex'])
    with engine.begin() as conn:
        for index, row in df.iterrows():
            conn.execute(
                text("INSERT INTO colors (name, hex_code) VALUES (:name, :hex_code) ON CONFLICT (hex_code) DO NOTHING;"),
                {"name": row['color_name'], "hex_code": row['color_hex']}
            )

def load_subjects(filename):
    df = pd.read_csv(filename).drop_duplicates(subset=['subjects'])
    with engine.begin() as conn:
        for subject in df['subjects']:
            conn.execute(
                text("INSERT INTO subjects (name) VALUES (:name) ON CONFLICT (name) DO NOTHING;"),
                {"name": subject}
            )

def refresh_episodes_df():
    return pd.read_sql("SELECT id, painting_title FROM episodes", engine)

def link_episodes_to_subjects_and_colors(episodes_filename, subjects_filename, colors_filename):
    episodes_df = refresh_episodes_df()  # Ensure this function refreshes episodes_df from the database
    subjects_df = pd.read_csv(subjects_filename).dropna(subset=['subjects'])
    colors_df = pd.read_csv(colors_filename)

    with engine.begin() as conn:
        for index, row in subjects_df.iterrows():
            episode_id = episodes_df.loc[episodes_df['painting_title'] == row['painting_title'], 'id'].values
            if episode_id.size > 0:
                episode_id = int(episode_id[0])  # Ensure episode_id is an integer
                subject_result = conn.execute(text("SELECT id FROM subjects WHERE name = :name"), {"name": row['subjects']})
                subject_id_list = [r[0] for r in subject_result]
                if subject_id_list:
                    subject_id = int(subject_id_list[0])  # Ensure subject_id is an integer
                    conn.execute(text("INSERT INTO episodes_subjects (episode_id, subject_id) VALUES (:episode_id, :subject_id) ON CONFLICT DO NOTHING;"), {"episode_id": episode_id, "subject_id": subject_id})
                else:
                    print(f"Subject '{row['subjects']}' not found.")
            else:
                print(f"Episode title '{row['painting_title']}' not found in episodes.")

        episodes_df = refresh_episodes_df()  # Re-fetch episodes_df after loading episodes to ensure it's up-to-date

        for index, row in colors_df.iterrows():
            episode_id = episodes_df.loc[episodes_df['painting_title'] == row['painting_title'], 'id'].values
            if episode_id.size > 0:
                episode_id = int(episode_id[0])  # Ensure episode_id is an integer
                color_result = conn.execute(text("SELECT id FROM colors WHERE name = :name AND hex_code = :hex_code"), {"name": row['color_name'], "hex_code": row['color_hex']})
                color_id_list = [r[0] for r in color_result]
                if color_id_list:
                    color_id = int(color_id_list[0])  # Ensure color_id is an integer
                    conn.execute(text("INSERT INTO episodes_colors (episode_id, color_id) VALUES (:episode_id, :color_id) ON CONFLICT DO NOTHING;"), {"episode_id": episode_id, "color_id": color_id})
                else:
                    print(f"Color '{row['color_name']}' not found.")
            else:
                print(f"Episode title '{row['painting_title']}' not found in episodes.")



if __name__ == "__main__":
    dates = '../transformed_data/transformed_dates.csv'
    subjects = '../transformed_data/transformed_subjects.csv'
    colors = '../transformed_data/transformed_colors.csv'

    load_episodes(dates)
    load_colors(colors)
    load_subjects(subjects)
    link_episodes_to_subjects_and_colors(dates, subjects, colors)
