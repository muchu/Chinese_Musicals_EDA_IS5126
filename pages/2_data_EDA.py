import streamlit as st
import matplotlib.pyplot as plt
from data_tools import get_table_data
from sql_query import *
import pandas as pd

table_names = ["shows","theatres","citys","musicals","produces"]
datas = { key: pd.read_csv(f"./data/{key}") for key in table_names}
tabs = st.tabs(datas.keys())

# 为每个标签页添加内容
for index,key in enumerate(datas.keys()):
    with tabs[index]:
        st.write(f"head of table **{key}**")
        st.dataframe(datas[key].head(10))
        
        st.write(f"Data info")
        st.write(datas[key].info())

        st.write("Data NaN information")
        st.write(datas[key].isnull().sum())
        

