import streamlit as st
import matplotlib.pyplot as plt
from data_tools import use_sql_query,connect_to_db
from sql_query import theatre_number_in_citys
import pandas as pd


#connect to the database
conn,cur = connect_to_db()
if ['cur','conn'] not in st.session_state:
    st.session_state.cur = cur
    st.session_state.conn = conn


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Data Workflow Implementation")
st.write("\n\n\n\n")
st.header("1. Theatre distribution of City")

theatre_data_df = use_sql_query(cur=st.session_state.cur,sql_query=theatre_number_in_citys)
st.dataframe(theatre_data_df)