import streamlit as st
import matplotlib.pyplot as plt
from data_tools import get_table_data
from sql_query import *
import pandas as pd

table_names = ["shows","theatres","citys","musicals","produces"]
datas = get_table_data(cur=st.session_state.cur,table_names=table_names)
tabs = st.tabs(datas.keys())
print(tabs)
# 为每个标签页添加内容
for index,key in enumerate(datas.keys()):
    with tabs[index]:
        st.write(f"### head of table **{key}**")
        st.dataframe(datas[key].head(10))

        st.write("### Data NaN information")
        st.write(datas[key].isnull().sum())

