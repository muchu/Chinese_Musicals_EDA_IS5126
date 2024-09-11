import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

table_names = ["shows","theatres","citys","musicals","produces"]
datas = { key: pd.read_csv(f"./data/{key}",index_col=0) for key in table_names}
tabs = st.tabs(datas.keys())

# 为每个标签页添加内容
for index,key in enumerate(datas.keys()):
    with tabs[index]:
        st.write(f"head of table **{key}**")
        st.dataframe(datas[key])

        

