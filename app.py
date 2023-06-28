# -*- coding: utf-8 -*-
"""New Streamlit_Colab_demo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eF1yPS6HddTIZ1P0t02m9L39R74A49BJ

# Streamlit - Building simple web apps/dashboards

- Make sure you have a free, personal `ngrok` token: https://dashboard.ngrok.com/auth
"""


import streamlit as st
from pyngrok import ngrok
import getpass

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import seaborn as sns

# Load some data
df = pd.read_csv("https://drive.google.com/file/d/1zO3kM2gsspH4Wyg5OF1u-n_RFz6He_qE/view?usp=drive_link", sep=",")
df_cont = pd.read_csv("https://drive.google.com/file/d/1YPilsqqlLu27a_ptPTD1458vh5DaG1Wx/view?usp=drive_link", header=0)

df.columns = ["country", "code", "year", "usage"]
df_cont.columns = ["continent", "country"]

#merge continents to the df
df = pd.merge(df, df_cont, on="country", how="inner")
df_cont = df.groupby(["continent", "year"])["usage"].sum().reset_index()



# Add title and header
st.title("Introduction to Streamlit")
st.header("Internet Usage Data Exploration")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.header("This is my dataset:")
    st.dataframe(data=df_cont)
    st.table(data=df_cont)
    st.write(data=df_cont)

data = []
trace = go.Scatter(
        x=df.groupby("year")["usage"].sum().reset_index(name="usage")["year"],
        y=df.groupby("year")["usage"].sum().reset_index(name="usage")["usage"],
        mode='lines',
    )
    # Add the trace object to the data list

data.append(trace)

layout = go.Layout(
    title='Internet Usage by year',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Usage')
)

fig1 = go.Figure(data=data, layout=layout)

st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

## choose the continent to Display

cont = st.selectbox(
    'What continent do you want to see',
    tuple(df_cont["continent"].unique()))

st.write('You selected:', cont)
cont = str(cont)

color_palette = {
    'Asia': 'blue',
    'Africa': 'green',
    'Europe': 'red',
    'North America': 'orange',
    'South America': 'yellow',
    'Oceania': 'pink'
}


data = []
continent_data = df_cont[df_cont['continent'] == cont]
trace = go.Scatter(
        x=continent_data['year'],
        y=continent_data['usage'],
        mode='lines',
        name=cont,
        line=dict(color=color_palette[cont])
    )

data.append(trace)

layout = go.Layout(
    title='Internet Usage by Continent',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Usage')
)

fig2 = go.Figure(data=data, layout=layout)

st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

### plot the country in that continent
country = st.selectbox('What country do you want to see',tuple(df[df["continent"] == cont]["country"].unique()))

country = str(country)

data = []
country_data = df[(df["continent"] == cont) & (df["country"] == country)]
trace = go.Scatter(
        x=country_data['year'],
        y=country_data['usage'],
        name=cont,
        line=dict(color="magenta")
    )

data.append(trace)

layout = go.Layout(
    title='Internet Usage by country',
    xaxis=dict(title='Year'),
    yaxis=dict(title='Usage')
)

fig3 = go.Figure(data=data, layout=layout)
st.plotly_chart(fig3, theme="streamlit", use_container_width=True)

### all countries in continent for different years

year = st.selectbox('What year do you want to see different countries internet usage?',tuple(df["year"].unique()))

year = int(year)

year_data = df[(df["continent"]==cont) & (df["year"] ==year)]
data = []
trace  = go.Bar(
        x= year_data["country"],
        y=year_data['usage'],
        )

data.append(trace)

layout = go.Layout(
    title='Internet Usage by country',
    xaxis=dict(title='country'),
    yaxis=dict(title='Usage')
)

fig4 = go.Figure(data=data, layout=layout)
st.plotly_chart(fig4, theme="streamlit", use_container_width=True)





Commented out IPython magic to ensure Python compatibility.
%%writefile -a streamlit_ex.py


Commented out IPython magic to ensure Python compatibility.
%pycat streamlit_ex.py

# """## Test run""" """ """

def start_tunnel(port=500):
  # Terminate open tunnels if exist
  ngrok.kill()

  # Setting the authtoken
  # --------------------------------
  # Get your authtoken from https://dashboard.ngrok.com/auth
  NGROK_AUTH_TOKEN = getpass.getpass('Enter the ngrok authtoken: ')
  ngrok.set_auth_token(NGROK_AUTH_TOKEN)
  # --------------------------------

  # Open an HTTP tunnel on port 8501 for http://localhost:8501
  ngrok_tunnel = ngrok.connect(addr=str(port))
  print("Streamlit URL:", ngrok_tunnel.public_url)
  return ngrok_tunnel

start_tunnel(8501)

!streamlit run streamlit_ex.py --logger.level=debug

"""# Mini Project

Below you will find three publicly available datasets which you can use for a small project to showcase your visualization skills.
All of them include some type of geospatial data, so you can for example create choropleth maps, and there are also many other options.
By the end of the day you will complete this project, and (optionally) push your code to GitHub and deploy it as a small web app online to showcase your work to others.

Data Sets
================================

**1. Internet Access Around the Globe**

Do you ever wonder how internet access has changed over the years?
The World Bank provides country-level data on the percentage of the population using the internet from 1960-2020 (though it really only gets interesting in the 90s).
This data works well for choropleth maps of the world, showing which countries have the highest usage percentage and how this has changed.
You can also group the countries by continent or income level and compare the results.

You can get some neat ideas how to visualize this data from [Our World in Data](https://ourworldindata.org/internet) and you can try to combine this dataset with the socio-economic data that we used in the second live coding notebook.

- Data: [Internet Access](https://drive.google.com/file/d/1aWkNwXLI8jmu-cj0OTHM23M19XGKt0e0/view?usp=sharing)
- geoJSON file: [Countries](https://drive.google.com/file/d/1V5GRlto4F1fBO-IUPfqxQf4R39PBirHo/view?usp=sharing)


**2. Clean Energy Sources in Switzerland**

Are you interested in which canton in Switzerland boasts the most clean energy sources?
You can work with a dataset on renewable power plants from the [Open Power System Data](https://open-power-system-data.org/) platform.
It lists the power sources currently operating in each canton, grouped into bioenergy, hydro, solar or wind, along with a few more attributes.

If you want some ideas how this type of data can be visualized, here's an [article](https://www.uvek-gis.admin.ch/BFE/storymaps/EE_Elektrizitaetsproduktionsanlagen/?lang=en) where a somewhat similar dataset was used.

- Data: [Swiss Clean Energy Sources](https://drive.google.com/file/d/1h1wbh7cQPtDSayazQmpG_tuzP9JvASgU/view?usp=sharing>)
- geoJSON file: [Swiss Cantons](https://drive.google.com/file/d/1CZSgdNRB3hrz9kgW49hCJdtdR80_tyhw/view?usp=sharing)


**3. Dogs of Zurich**

Zurich is home to many dogs, all of which have to be registered by their owners.
The city's [Open Data department](https://data.stadt-zuerich.ch/) publishes a dataset of registered dogs every year.
Besides information on the dog's birth year, color, breed and sex, it also includes some features about the owners, like the age group they belong to, their gender and the part of the city that they live in.


So if you've always wanted to know which district has the highest number of dogs, or what breed of dog elderly ladies prefer, this is your chance!
For some ideas how to create fun (yet informative) visualizations with this dataset, have a look at this [newspaper article](https://interaktiv.tagesanzeiger.ch/2017/beliebteste-hunde/).

- Data: [Zurich Dogs](https://drive.google.com/file/d/1PAoIbp1cZrthkuqLSNGcPl_fkkr_YJEK/view?usp=sharing)
- geoJSON file: [Zurich Kreise](https://drive.google.com/file/d/1jS2OxyS7alvJjMYaLH8GGFWcTcjkj37z/view?usp=sharing>)
"""





















