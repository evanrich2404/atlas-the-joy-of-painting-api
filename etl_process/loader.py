from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Now you can user os.getenv to access your variables
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')

def load_data_to_db(filename, table_name):
    conn = psycopg2.connect("dbname=db_name user=db_user password=db_pass")
    cur = conn.cursor()

    df = pd.read_csv(filename)
    for _, row in df.iterrows():
        # Construct an INSERT or UPDATE statement from each row
        # Example: cur.execute(f"INSERT INTO {table_name} VALUES (...)", (row['column1'], row['column2']))
        pass

    conn.commit()
    cur.close()
    conn.close()

# Example function call
load_data_to_db('../transformed_data/transformed_data.csv', 'episodes')
