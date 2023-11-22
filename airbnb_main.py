import pandas as pd
import numpy as np
import certifi
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from pymongo.mongo_client import MongoClient
from streamlit_option_menu import option_menu


st.set_page_config(page_title= "Airbnb Data Visualization | By Gokul Ram",
                   layout = "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard has been created by *Gokul Ram*!"""})

st.markdown("<h1 style='text-align: center; color: red;'>Airbnb Data Visualization</h1>", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore"], 
                            icons=["house","graph-up-arrow","bar-chart-line"],
                            menu_icon= "menu-button-wide",
                            default_index=0,
                            orientation = "horizontal",
                            styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                    "nav-link-selected": {"background-color": "#FF5A5F"}}
                            )


# Mongo DB connection

uri = "mongodb://gokulram:subline@ac-hwa9ikn-shard-00-00.cpc3ie7.mongodb.net:27017,ac-hwa9ikn-shard-00-01.cpc3ie7.mongodb.net:27017,ac-hwa9ikn-shard-00-02.cpc3ie7.mongodb.net:27017/?ssl=true&replicaSet=atlas-of54d2-shard-0&authSource=admin&retryWrites=true&w=majority&appName=AtlasApp"
# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client.sample_airbnb    #database fetched
records = db.listingsAndReviews


df = pd.read_csv('airbnb_data.csv')

if selected == "Home":

    home_col1, home_col2 = st.columns(2,gap= 'medium')

    with home_col1:

        st.markdown("#   ")
        st.markdown("## :blue[Domain] : Travel Industry, Property Management ")
        st.markdown("#   ")
        st.markdown("## :blue[Packages Used] : Python, Pandas, Mongo DB, Plotly, Seaborn, Streamlit ")
        st.markdown("#   ")
        st.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, \
            develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, \
            and location-based trends. ")

    with home_col2:
        
           st.image("airbnb.png")


if selected == "Overview":
    st.write('## :orange[OVERVIEW OF THE AIRBNB DATA]')
    tab1,tab2 = st.tabs(["SOURCE DATA", "INSIGHTS"])
    
    # SOURCE DATA TAB
    with tab1:
        col1,col2 = st.columns(2)
        
        # DATAFRAME FORMAT
        if st.button("View Airbnb Dataframe"):
            st.write(df)

    # INSIGHTS TAB
    with tab2:
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.sidebar.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

        # User input into query
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

        col1, col2 = st.columns([6,4])

        with col1:

             # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name= "Listings").sort_values(by= 'Listings',ascending= False)[:10]
            fig = px.bar(df1,
                         title = 'Top 10 Property Types',
                         x = 'Listings',
                         y = 'Property_type',
                         orientation = 'h',
                         color = 'Property_type',
                         color_continuous_scale = px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width = True)

              # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name= "Listings").sort_values(by= 'Listings', ascending= False)[:10]
            fig = px.bar(df2,
                         title = 'Top 10 Hosts with highest number of listings',
                         x = 'Listings',
                         y = 'Host_name',
                         orientation = 'h',
                         color = 'Host_name',
                         color_continuous_scale = px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width = True) 
        
        with col2:

            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name= "counts")
            fig = px.pie(df1,
                         title = 'Total Listings in each Room_types',
                         names = 'Room_type',
                         values = 'counts',
                         color_discrete_sequence = px.colors.sequential.Viridis
                        )
            fig.update_traces(textposition = 'outside', textinfo = 'value+label')
            st.plotly_chart(fig,use_container_width=True)


            df3 = df.query(query).groupby(["Country"]).size().reset_index(name= "counts")
            fig = px.pie(df3,
                         title = 'Total Listings in each country',
                         names = 'Country',
                         values = 'counts',
                         color_discrete_sequence = px.colors.sequential.Blugrn_r
                        )
            fig.update_traces(textposition = 'outside', textinfo='value+label')
            st.plotly_chart(fig,use_container_width = True)


            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
        country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
        fig = px.choropleth(country_df,
                            title = 'Total Listings Geo map',
                            locations = 'Country',
                            locationmode = 'country names',
                            color = 'Total_Listings',
                            color_continuous_scale = px.colors.sequential.Viridis
                            )
        st.plotly_chart(fig,use_container_width=True)

# EXPLORE TAB

if selected == "Explore":
    st.write('## :orange[EXPLORATION OF AIRBNB DATA]')

    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.sidebar.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

    # User input into query
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

    #for title
    cols1, cols2, cols3 = st.columns(3)

    with cols2:
        st.markdown("<h3 style='text-align: center; color: grey;'>Price Analysis</h3>", unsafe_allow_html=True)

    price_col1, price_col2 = st.columns([5,5])

    with price_col1:

        price_df = df.query(query).groupby('Room_type', as_index = False)['Price'].mean().sort_values(by= 'Price')

        # Average price by room type

        fig = px.bar(data_frame = price_df,
                     x = 'Room_type',
                     y = 'Price',
                     color = 'Price',
                     title = 'Avg Price for each Room type'
                    )
        st.plotly_chart(fig, use_container_width = True)

    with price_col2:
        
        # Average price in countries geo plot
        country_df = df.query(query).groupby('Country', as_index = False)['Price'].mean()

        fig = px.scatter_geo(data_frame = country_df,
                                       locations = 'Country',
                                       color = 'Price', 
                                       hover_data = ['Price'],
                                       locationmode = 'country names',
                                       size = 'Price',
                                       title = 'Avg Price in each Country',
                                       color_continuous_scale = 'agsunset'
                            )
        st.plotly_chart(fig, use_container_width = True)

    #for title
    cols1, cols2, cols3 = st.columns(3)

    with cols2:
        st.markdown("<h3 style='text-align: center; color: grey;'>Availability Analysis</h3>", unsafe_allow_html=True)

    avail_col1, avail_col2 = st.columns([5,5])

    with avail_col1:

        # Availability by room type
        avail_df = df.query(query).groupby('Availability', as_index = False)['Price'].mean().sort_values(by= 'Price')

        fig = px.box(data_frame = df.query(query),
                     x = 'Room_type',
                     y = 'Availability',
                     color = 'Room_type',
                     title = 'Availability by Room_type'
                    )
        st.plotly_chart(fig, use_container_width = True)

    with avail_col2:

        # Average price in countries geo plot
        country_df = df.query(query).groupby('Country', as_index = False)['Availability'].mean()
        country_df.Availability = country_df.Availability.astype(int)

        fig = px.scatter_geo(data_frame = country_df,
                             locations = 'Country',
                             color = 'Availability', 
                             hover_data = ['Availability'],
                             locationmode = 'country names',
                             size = 'Availability',
                             title = 'Avg Availability in each Country',
                             color_continuous_scale = 'agsunset'
                             )
        st.plotly_chart(fig, use_container_width = True)
        
