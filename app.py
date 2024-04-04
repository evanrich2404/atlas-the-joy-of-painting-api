from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve database connection details from environment variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')


app = Flask(__name__)

# Database URI
DATABASE_URI = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

engine = create_engine(DATABASE_URI)

@app.route('/')
def home():
    return "Welcome to The Joy of Painting API!"

@app.route('/episodes', methods=['GET'])
def get_episodes():
    month = request.args.getlist('month')
    subjects = request.args.getlist('subject')
    colors = request.args.getlist('color')
    match_all_filters = request.args.get('match_all', 'false').lower() == 'true'

    # Start building your SQL query based on the filters received
    # This is a basic starting point. You'll need to adjust it based on your database schema
    query = """
    SELECT DISTINCT episodes.id, episodes.painting_title, episodes.broadcast_date
    FROM episodes
    LEFT JOIN episodes_subjects ON episodes.id = episodes_subjects.episode_id
    LEFT JOIN subjects ON episodes_subjects.subject_id = subjects.id
    LEFT JOIN episodes_colors ON episodes.id = episodes_colors.episode_id
    LEFT JOIN colors ON episodes_colors.color_id = colors.id
    WHERE 1=1
    """

    # Add conditions based on the filters
    if month:
        query += " AND EXTRACT(MONTH FROM episodes.broadcast_date) IN ({})".format(','.join(month))
    if subjects:
        query += " AND subjects.name IN ({})".format(','.join([f"'{subject}'" for subject in subjects]))
    if colors:
        query += " AND colors.name IN ({})".format(','.join([f"'{color}'" for color in colors]))

    print("Final SQL Query:", query)

    # Execute the query and fetch results
    with engine.connect() as conn:
        episodes = pd.read_sql(query, conn)

    # Convert the DataFrame to JSON
    return jsonify(episodes.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
