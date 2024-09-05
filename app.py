import streamlit as st
import matplotlib.pyplot as plt
from data_tools import use_sql_query,connect_to_db
from sql_query import *
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots  import make_subplots


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



##########Fig1
st.header("1. Theatre distribution of City")

location_dict = {
    "上海":"Shanghai",
    "北京":"Beijing",
    "深圳":"Shenzhen",
    "南京":"Nanjing",
    "成都":"Chengdu",
    "杭州":"Hangzhou",
    "广州":"Guangzhou",
    "苏州":"Suzhou",
    "西安":"Xian",
    "武汉":"Wuhan"
}

# get data
theatre_data_df = use_sql_query(cur=st.session_state.cur,sql_query=theatre_number_in_citys).head(10)
musical_perform_df = use_sql_query(cur=st.session_state.cur,sql_query=musical_perform_by_date_range,params=("2023-01-01","2024-12-31"))

#join 2 df
fig_data1 = pd.merge(theatre_data_df,musical_perform_df,left_on = "city_name",right_on = "city",how="left")
fig_data1["city_en"] = fig_data1["city_name"].map(location_dict)

# plot
fig = go.Figure()
fig.add_trace(go.Bar(
    x=fig_data1['city_en'],
    y=fig_data1['numberoftheatre'],
    marker=dict(color="#466b82"),
    name="Number of Theatres"
))
fig.add_trace(go.Scatter(
    x=fig_data1['city_en'],
    y=fig_data1['count'],
    mode='lines+markers',
    line=dict(color='#E91E63', width=2),
    marker=dict(size=8),
    yaxis='y2',
    name="Number of Performance"
))
fig.update_layout(
    yaxis2=dict(
        title='Number of Performances',
        overlaying='y',
        side='right'
    ),
    yaxis=dict(title='Number of Theatres'),
    xaxis=dict(title='City name'),
    legend=dict(x=1.1, y=1),
        autosize=True,
)
st.plotly_chart(fig)

#########Fig 2
st.header("2. 音乐剧创作性质")
# get data
musical_original_df_2023 = use_sql_query(cur=st.session_state.cur, sql_query= original_musical_persentage_by_date_range,params=("2023-01-01","2023-12-31"))
musical_original_df_2024 = use_sql_query(cur=st.session_state.cur, sql_query= original_musical_persentage_by_date_range,params=("2024-01-01","2024-12-31"))
st.dataframe(musical_original_df_2023)
fig = make_subplots(rows=1, cols=2,specs=[[{'type':'domain'}, {'type':'domain'}]],subplot_titles=("2023", "2024"))
fig.add_trace(
    go.Pie(name="Number of Theatres",labels=musical_original_df_2023["is_original"],values=musical_original_df_2023["count"]),
    row=1, col=1
)
fig.add_trace(
    go.Pie(name="Number of Theatres",labels=musical_original_df_2024["is_original"],values=musical_original_df_2024["count"]),
    row=1, col=2
)
# 更新布局
fig.update_layout(
    title_text="Musical Creation Nature Comparison: 2023 vs 2024",
    height=600,
    width=1000,
    legend_title="Original Status"
)

# 显示图表
st.plotly_chart(fig)

#####Fig3
st.header("3. 不同城市表演月份分布")

month_date_list_2023 = {

    "January": ("2023-01-01", "2023-01-31"),
    "February": ("2023-02-01", "2023-02-28"),
    "March": ("2023-03-01", "2023-03-31"),
    "April": ("2023-04-01", "2023-04-30"),
    "May": ("2023-05-01", "2023-05-31"),
    "June": ("2023-06-01", "2023-06-30"),
    "July": ("2023-07-01", "2023-07-31"),
    "August": ("2023-08-01", "2023-08-31"),
    "September": ("2023-09-01", "2023-09-30"),
    "October": ("2023-10-01", "2023-10-31"),
    "November": ("2023-11-01", "2023-11-30"),
    "December": ("2023-12-01", "2023-12-31")
}


#get data
monthly_shows = use_sql_query(cur=st.session_state.cur,sql_query=get_monthly_number_of_shows_by_city)

shanghai_2023 = monthly_shows[(monthly_shows["city"] == "上海") & (monthly_shows["year"] == 2023)]
shanghai_2023_total = shanghai_2023["total_shows"].sum()
shanghai_2023["monthly_ratio"] = shanghai_2023["total_shows"] / shanghai_2023_total

beijing_2023 = monthly_shows[(monthly_shows["city"] == "北京") & (monthly_shows["year"] == 2023)]
beijing_2023_total = beijing_2023["total_shows"].sum()
beijing_2023["monthly_ratio"] = beijing_2023["total_shows"] / beijing_2023_total

chengdu_2023 = monthly_shows[(monthly_shows["city"] == "成都") & (monthly_shows["year"] == 2023)]
chengdu_2023_total = chengdu_2023["total_shows"].sum()
chengdu_2023["monthly_ratio"] = chengdu_2023["total_shows"] / chengdu_2023_total
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=shanghai_2023["month"],
    y=shanghai_2023["total_shows"],
    name="Shanghai",
    yaxis="y"
))
fig3.add_trace(go.Bar(
    x=beijing_2023["month"],
    y=beijing_2023["total_shows"],
    name="Beijing",
    yaxis="y"
))
fig3.add_trace(go.Bar(
    x=chengdu_2023["month"],
    y=chengdu_2023["total_shows"],
    name="Chengdu",
    yaxis="y"
))

fig3.add_trace(go.Scatter(
    x=shanghai_2023["month"],
    y=shanghai_2023["monthly_ratio"],
    mode='lines+markers',
    name="Shanghai Ratio",
    yaxis="y2"
))
fig3.add_trace(go.Scatter(
    x=beijing_2023["month"],
    y=beijing_2023["monthly_ratio"],
    mode='lines+markers',
    name="Beijing Ratio",
    yaxis="y2"
))
fig3.add_trace(go.Scatter(
    x=chengdu_2023["month"],
    y=chengdu_2023["monthly_ratio"],
    mode='lines+markers',
    name="Chengdu Ratio",
    yaxis="y2"
))

fig3.update_layout(
    title="Monthly Distribution of Performances in Different Cities (2023)",
    xaxis_title="Month",
    yaxis_title="Total Shows",
    yaxis2=dict(title="Monthly Ratio", overlaying="y", side="right"),
    legend_title="City",
    barmode="group"
)

st.plotly_chart(fig3)