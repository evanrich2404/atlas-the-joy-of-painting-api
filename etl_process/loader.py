import psycopg2
import pandas as pd

def load_data_to_db(filename, table_name):
    conn = psycopg2.connect("dbname=bobdabase user=root password=root")
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
load_data_to_db('transformed_data.csv', 'episodes')
