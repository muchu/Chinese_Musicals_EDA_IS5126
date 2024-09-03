import psycopg2
import pandas as pd
from INFO import database_schema

conn = psycopg2.connect(
    host ="localhost",
dbname ="postgres",
user = "postgres",
password ="is5126",
port=5433)
cur = conn.cursor()

cur.execute(database_schema)

conn.commit()

cur.close()
conn.close()




