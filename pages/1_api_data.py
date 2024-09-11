import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import requests 

st.header("Original shape/schema of the api data")
st.write("\n\n\n\n")
st.write("**Theatre**")
theatre_api = requests.get("http://y.saoju.net/yyj/api/theatre/")
theatre_api_json = theatre_api.json()
st.json(theatre_api_json)

st.write("\n\n\n\n")
st.write("**Musicals**")
musicals_api = requests.get("http://y.saoju.net/yyj/api/musical/")
musicals_api_json = musicals_api.json()
st.json(musicals_api_json)
