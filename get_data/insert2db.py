import pandas as pd
from INFO import fieids_url
import psycopg2


data_dict = {}
for key in fieids_url.keys():
    data_dict[key] = pd.read_csv(f"../data/{key}")

try:
    conn = psycopg2.connect(
        host ="localhost",
    dbname ="postgres",
    user = "postgres",
    password ="is5126",
    port=5433)
    cur = conn.cursor()
except psycopg2.Error as e:
    print(f"An error occurred: {e}")
    conn.rollback()  # Rollback in case of error




for key in data_dict.keys():
    try:
        num_columns = len(data_dict[key].columns)
        placeholders = ', '.join(['%s'] * num_columns)
        # Define the SQL insert query with placeholders for the data
        insert_query = f"INSERT INTO {key} VALUES ({placeholders})"
    
    
        # Iterate over DataFrame rows as namedtuples (use index=False to avoid including the index)
        for row in data_dict[key].itertuples(index=False, name=None):
            cur.execute(insert_query, row)
    
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully")
    
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback in case of error
    
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()