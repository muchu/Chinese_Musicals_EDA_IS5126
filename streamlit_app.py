import streamlit as st
import matplotlib.pyplot as plt
from data_tools import use_sql_query,connect_to_db,get_table_data
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
st.header("2. Originality of Musical")
# get data
musicals = get_table_data(cur=st.session_state.cur,table_names= ["musicals"] )["musicals"]

musicals["premiere_date"] = pd.to_datetime(musicals["premiere_date"])
musicals["year"] = musicals["premiere_date"].dt.year
musicals = musicals[musicals["year"] > 2017]

year_musical_df = pd.DataFrame(musicals.groupby("year").agg({
    'musical_id': 'count',
    'is_original': 'sum',
}))
year_musical_df["imitation_musical_number"] = year_musical_df["musical_id"] - year_musical_df["is_original"]
year_musical_df["original_musical_ratio"] = year_musical_df["is_original"] / year_musical_df["musical_id"]
year_musical_df.reset_index(inplace=True)

fig_musical_originality = go.Figure()

fig_musical_originality.add_trace(go.Bar(
    x=year_musical_df["year"],
    y=year_musical_df["musical_id"],
    name="Total Musical",
    marker=dict(color="#E91E63"),
    yaxis="y2"

))
fig_musical_originality.add_trace(go.Scatter(
    x=year_musical_df["year"],
    y=year_musical_df["original_musical_ratio"],
    name="original ratio",
    mode='lines+markers',
    marker=dict(color="#466b82"),
    yaxis="y"
))

fig_musical_originality.update_layout(
    title="Musical Originality by Year",
    yaxis=dict(title="Original Ratio",side="right",overlaying="y2",range=[0,1]),
    yaxis2=dict(title="Total Musical",side="left"),
    legend=dict(x=1.1, y=1),
    autosize=True,
    xaxis=dict(title="Year"),
)

st.plotly_chart(fig_musical_originality)

musical_2022 = musicals[(musicals["year"] == 2022) & (musicals["is_original"] == 0)]
musical_2023 = musicals[(musicals["year"] == 2023) & (musicals["is_original"] == 0)]
musical_2024 = musicals[(musicals["year"] == 2024) & (musicals["is_original"] == 0)]
county_name = {
    "Broadway":["百老汇"],
    "American":["美国"],
    "Korea":["韩国","韩","韩方"],
    "Thailand":["泰国"],
    "Russia":["俄罗斯"],
    "France":["法国"],
    "Japan":["日本"],
    "Other":["其他"]
}

for key, value in county_name.items():
    musical_2022["info_country"] = musical_2022["info"].apply(lambda x: key if any(v in x for v in value) else musical_2022.loc[musical_2022["info"] == x, "info_country"].iloc[0] if "info_country" in musical_2022.columns else x)
    musical_2023["info_country"] = musical_2023["info"].apply(lambda x: key if any(v in x for v in value) else musical_2023.loc[musical_2023["info"] == x, "info_country"].iloc[0] if "info_country" in musical_2023.columns else x)
    musical_2024["info_country"] = musical_2024["info"].apply(lambda x: key if any(v in x for v in value) else musical_2024.loc[musical_2024["info"] == x, "info_country"].iloc[0] if "info_country" in musical_2024.columns else x)
musical_2022["info_country"] = musical_2022["info_country"].apply(lambda x: x if x in county_name.keys() else "Other")
musical_2023["info_country"] = musical_2023["info_country"].apply(lambda x: x if x in county_name.keys() else "Other")
musical_2024["info_country"] = musical_2024["info_country"].apply(lambda x: x if x in county_name.keys() else "Other")

# pie chart to describe the proportion of imitation musicals by country
# subplot

fig_musical_imitation_country = make_subplots(rows=1, cols=3, subplot_titles=["2022", "2023", "2024"], specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]])
#change color, do not use likely color  
colors = ["#FFA15A", "#FFB470", "#FFC49C", "#FFD6AA", "#FFE6CC", "#FFF2E0"]
fig_musical_imitation_country.add_trace(go.Pie(
    labels=musical_2022["info_country"].value_counts().index,
    values=musical_2022["info_country"].value_counts().values,
    name="2022",
    marker=dict(colors=colors)
), row=1, col=1)

fig_musical_imitation_country.add_trace(go.Pie(
    labels=musical_2023["info_country"].value_counts().index,
    values=musical_2023["info_country"].value_counts().values,
    name="2023",
    marker=dict(colors=colors)
), row=1, col=2)

fig_musical_imitation_country.add_trace(go.Pie(
    labels=musical_2024["info_country"].value_counts().index,
    values=musical_2024["info_country"].value_counts().values,
    name="2024",
    marker=dict(colors=colors)
), row=1, col=3)

fig_musical_imitation_country.update_layout(

    title="Imitation Musical by Country",
    legend=dict(x=1.1, y=1),
    autosize=True
)

st.plotly_chart(fig_musical_imitation_country)

#####Fig3
st.header("3. Trending of performances in Shanghai and Beijing")



#get data
monthly_shows = use_sql_query(cur=st.session_state.cur,sql_query=get_monthly_number_of_shows_by_city)
monthly_shows["datetime"] = pd.to_datetime(monthly_shows["year"].astype(str) + "-" + monthly_shows["month"].astype(str), format='%Y-%m')
monthly_shows = monthly_shows[(monthly_shows["datetime"] < "2024-09-01")]


shanghai = monthly_shows[monthly_shows["city"] == "上海"]
shanghai_2023 = shanghai.sort_values(by=['datetime'])
shanghai["monthly_ratio"] = (shanghai["total_shows"] - shanghai["total_shows"].shift(1))*100 / shanghai["total_shows"].shift(1)



beijing = monthly_shows[monthly_shows["city"] == "北京"]
beijing_2023 = beijing.sort_values(by=['datetime'])
beijing["monthly_ratio"] =( beijing["total_shows"] - beijing["total_shows"].shift(1))*100 / beijing["total_shows"].shift(1)


fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=shanghai["datetime"],
    y=shanghai["total_shows"],
    name="Shanghai",
    yaxis="y"
))
fig3.add_trace(go.Bar(
    x=beijing["datetime"],
    y=beijing["total_shows"],
    name="Beijing",
    yaxis="y"
))


fig3.add_trace(go.Scatter(
    x=shanghai["datetime"],
    y=shanghai["monthly_ratio"],
    mode='lines+markers',
    name="Shanghai Ratio",
    yaxis="y2"
))
fig3.add_trace(go.Scatter(
    x=beijing["datetime"],
    y=beijing["monthly_ratio"],
    mode='lines+markers',
    name="Beijing Ratio",
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


####### artists

last_month_shows = use_sql_query(cur=st.session_state.cur,sql_query=musical_list_by_date_range,params=("2024-08-01","2024-09-01"))
casts = " ".join(last_month_shows["casts"].astype(str))
cast_list = casts.split(" ")
st.write(pd.Series(cast_list).value_counts())