import streamlit as st
import matplotlib.pyplot as plt
from data_tools import use_sql_query,connect_to_db
from sql_query import theatre_number_in_citys
import pandas as pd

st.write("# this is the page about api data")
st.write("# Data Workflow Implementation")
st.write("\n\n\n\n")
st.header("1. Theatre distribution of City")

theatre_data_df = use_sql_query(cur=st.session_state.cur,sql_query=theatre_number_in_citys)
st.dataframe(theatre_data_df)