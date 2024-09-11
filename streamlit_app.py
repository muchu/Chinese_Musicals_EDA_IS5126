import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots  import make_subplots




st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.write("# Data Workflow Implementation")
st.write("\n\n\n\n")



##########Fig1
st.header("1. Uneven Distribution of Theaters")
st.write("The number of theaters is heavily skewed towards Shanghai, which has approximately three times more theaters than most other cities, highlighting Shanghai as a central hub for musical theater. For most other cities, such as Beijing, Shenzhen, and Chengdu, the number of theaters and performances seems to be relatively more balanced, but still far below Shanghai’s levels.")
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
theatre_data_df = pd.read_csv("./data/theatres",index_col=0)
musical_perform_df = pd.read_csv("./data/shows",index_col=0)
citys = pd.read_csv("./data/citys",index_col=0)
theatre_data_df = theatre_data_df.merge(citys,left_on="fields.city",right_on="pk",how="left")
theatre_data_df = theatre_data_df.groupby("fields.name_y").size().reset_index(name="numberoftheatre")
theatre_data_df.sort_values(by="numberoftheatre",ascending=False,inplace=True)
theatre_data_df = theatre_data_df.head(10)
musical_perform_df = musical_perform_df.groupby("city").size().reset_index(name="count")

#join 2 df
fig_data1 = pd.merge(theatre_data_df,musical_perform_df,left_on = "fields.name_y",right_on = "city",how="left")
fig_data1["city_en"] = fig_data1["fields.name_y"].map(location_dict)

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
    title="Number of Theatres and Performances in Different Cities",
    
    
)
st.plotly_chart(fig)

#########Fig 2
st.header("2.More new musicals, more original script")
st.write("The number of new musicals produced annually has been steadily increasing. Alongside this growth, there has been a notable rise in the proportion of original musicals. This could suggest a growing emphasis on creativity and original storytelling in the musical industry. The sustained growth in original musicals might indicate a healthy and vibrant future for the musical theater industry. ")
# get data
musicals = pd.read_csv("./data/musicals")

musicals["premiere_date"] = pd.to_datetime(musicals["fields.premiere_date"])
musicals["year"] = musicals["premiere_date"].dt.year
musicals = musicals[musicals["year"] > 2017]
# add "musical_id" using index of musicals
musicals["musical_id"] = musicals.index
year_musical_df = pd.DataFrame(musicals.groupby("year").agg({
    
    'musical_id': 'count',
    'fields.is_original': 'sum',
}))


year_musical_df["imitation_musical_number"] = year_musical_df["musical_id"] - year_musical_df["fields.is_original"]
year_musical_df["original_musical_ratio"] = year_musical_df["fields.is_original"] / year_musical_df["musical_id"]
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
st.write("**Most of imitational musical comes from Korea**")
st.write("\n Most newly produced musicals are adapted from Korean scripts. In contrast to the decline in Broadway productions, this suggests that Chinese audiences may prefer the storytelling, expression, and musical style of Asian productions.")
musical_2022 = musicals[(musicals["year"] == 2022) & (musicals["fields.is_original"] == 0)]
musical_2023 = musicals[(musicals["year"] == 2023) & (musicals["fields.is_original"] == 0)]
musical_2024 = musicals[(musicals["year"] == 2024) & (musicals["fields.is_original"] == 0)]
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
    musical_2022["info_country"] = musical_2022["fields.info"].apply(lambda x: key if any(v in x for v in value) else musical_2022.loc[musical_2022["fields.info"] == x, "info_country"].iloc[0] if "info_country" in musical_2022.columns else x)
    musical_2023["info_country"] = musical_2023["fields.info"].apply(lambda x: key if any(v in x for v in value) else musical_2023.loc[musical_2023["fields.info"] == x, "info_country"].iloc[0] if "info_country" in musical_2023.columns else x)
    musical_2024["info_country"] = musical_2024["fields.info"].apply(lambda x: key if any(v in x for v in value) else musical_2024.loc[musical_2024["fields.info"] == x, "info_country"].iloc[0] if "info_country" in musical_2024.columns else x)
musical_2022["info_country"] = musical_2022["info_country"].apply(lambda x: x if x in county_name.keys() else "Other")
musical_2023["info_country"] = musical_2023["info_country"].apply(lambda x: x if x in county_name.keys() else "Other")
musical_2024["info_country"] = musical_2024["info_country"].apply(lambda x: x if x in county_name.keys() else "Other")

# pie chart to describe the proportion of imitation musicals by country
# subplot

fig_musical_imitation_country = make_subplots(rows=1, cols=3, subplot_titles=["2022", "2023", "2024"], specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]])

colors = ['#FFA07A', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1', '#FFF2E0',"#FFD6AA"]
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
st.header("3. Steadily performed in shanghai, other cities come seasonal")

st.write("Compared to other cities, shanghai has a relatively steady number of shows perform(excluding the shrink in Feb for Chinese New Year). Shenzhen indicates a relatively seasonal trend.")

#get data
monthly_shows = pd.read_csv("./data/shows",index_col=0)
monthly_shows["datetime"] = pd.to_datetime(monthly_shows["date"])
monthly_shows["year"] = monthly_shows["datetime"].dt.year
monthly_shows["month"] = monthly_shows["datetime"].dt.month
monthly_shows = monthly_shows[(monthly_shows["datetime"] < "2024-09-01")]


shanghai = monthly_shows[monthly_shows["city"] == "上海"]
shanghai_2023 = shanghai.groupby(["year","month"]).size().reset_index(name="total_shows")
shanghai_2023["datetime"] = pd.to_datetime(shanghai_2023["year"].astype(str) + "-" + shanghai_2023["month"].astype(str), format='%Y-%m')
shanghai_2023 = shanghai_2023.sort_values(by=['datetime'])
shanghai_2023["monthly_ratio"] = (shanghai_2023["total_shows"] - shanghai_2023["total_shows"].shift(1))*100 / shanghai_2023["total_shows"].shift(1)



beijing = monthly_shows[monthly_shows["city"] == "深圳"]
beijing_2023 = beijing.groupby(["year","month"]).size().reset_index(name="total_shows")
beijing_2023["datetime"] = pd.to_datetime(beijing_2023["year"].astype(str) + "-" + beijing_2023["month"].astype(str), format='%Y-%m')
beijing_2023 = beijing_2023.sort_values(by=['datetime'])
beijing_2023["monthly_ratio"] =( beijing_2023["total_shows"] - beijing_2023["total_shows"].shift(1))*100 / beijing_2023["total_shows"].shift(1)


fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=shanghai_2023["datetime"],
    y=shanghai_2023["total_shows"],
    name="Shanghai",
    yaxis="y"
))
fig3.add_trace(go.Bar(
    x=beijing_2023["datetime"],
    y=beijing_2023["total_shows"],
    name="Shenzhen",
    yaxis="y"
))


fig3.add_trace(go.Scatter(
    x=shanghai_2023["datetime"],
    y=shanghai_2023["monthly_ratio"],
    mode='lines+markers',
    name="Shanghai Ratio",
    yaxis="y2"
))
fig3.add_trace(go.Scatter(
    x=beijing_2023["datetime"],
    y=beijing_2023["monthly_ratio"],
    mode='lines+markers',
    name="Shenzhen Ratio",
    yaxis="y2"
))


fig3.update_layout(
    title="Monthly Distribution of Performances in Different Cities (2023-01-01 --- 2024-09-01)",
    xaxis_title="Month",
    yaxis_title="Total Shows",
    yaxis2=dict(title="Monthly Ratio", overlaying="y", side="right",range=[-500,800]),
    legend_title="City",
    barmode="group",
    
)

st.plotly_chart(fig3)