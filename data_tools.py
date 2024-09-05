import psycopg2
import pandas as pd

def connect_to_db():
    conn = psycopg2.connect(
    host ="localhost",
    dbname ="postgres",
    user = "postgres",
    password ="is5126",
    port=5433)
    cur = conn.cursor()
    return conn,cur



def get_table_data(cur:psycopg2.connect,table_names) -> dict :
    df_list = {}
    for name in table_names:

        cur.execute(f"""
            SELECT * FROM {name}
            """)
        results = cur.fetchall()
        columns_name = [desc[0] for desc in cur.description]
        df_list[name] = pd.DataFrame(results,columns = columns_name)
    return df_list


def use_sql_query(cur,sql_query:str,params=None):
    cur.execute(sql_query,params)
    results = cur.fetchall()
    columns_name = [desc[0] for desc in cur.description]
        
    return pd.DataFrame(results,columns = columns_name)
