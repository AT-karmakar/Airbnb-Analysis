# streamlit run c:/Users/Akash/Desktop/pROJECT_Airbnb/Airbnb_Main_Streamlit.py

import pymongo
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image


#✈️
# page configuration
icon = Image.open(r"C:\Users\Akash\Desktop\pROJECT_Airbnb\airbnb-logo (1).png")
st.set_page_config(page_title= "Airbnb Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Aakash.K*!
                                        """}
                  )


title_styles = """
<style>    
    .title-text {
        font-family: Courier New, monospace; 
        color: red; 
        font-size: 64px; 
        text-align: center;        
    }
</style>
"""
st.markdown(title_styles, unsafe_allow_html=True)

# Display the customized title
st.markdown("<p class='title-text'>Airbnb Analysis</p>", unsafe_allow_html=True)


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#dedbd9"},
                                   "nav-link-selected": {"background-color": "#f04107"}}
                          )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
connection_string = "mongodb+srv://aakashkarmakar927:GuviAK@cluster0.rbcsqfl.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(connection_string)
db = client.sample_airbnb
col = db.listingsAndReviews

# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')

# HOME PAGE
if selected == "Home":
    
    img1= Image.open(r"C:\Users\Akash\Desktop\pROJECT_Airbnb\1589701567385.png")
    img2= Image.open(r"C:\Users\Akash\Desktop\pROJECT_Airbnb\timeline-airbnb.png")
    st.image(img1)
    st.markdown("""
    <p style='font-size:25px;font-family: Lucida Console'>Airbnb, Inc. is an American San Francisco-based company operating an online marketplace for short- and long-term homestays and experiences.
    The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia.</p>
    """, unsafe_allow_html=True)
    st.markdown("[Click here to visit Airbnb's website](https://www.airbnb.co.in/)")


    col1,col2 = st.columns(2,gap= 'small')
    col1.markdown("### :red[Overview:]")
    col1.markdown("""<p style='font-size: 25px; font-family: Palatino;''> This project delves into Airbnb data analysis using MongoDB Atlas, emphasizing data cleaning, interactive visualizations, and a Streamlit web app. Objectives include establishing MongoDB connectivity, ensuring data accuracy through cleaning, developing interactive maps for Airbnb exploration, analyzing pricing and availability trends. Key focus areas encompass MongoDB integration, data accuracy, interactive exploration, and consolidated insights.</p>
    """, unsafe_allow_html=True)
    col1.markdown("#### :red[Domain] => Travel Industry, Property Management and Tourism")
    col2.image(img2)
    st.markdown(
        """
        <div style='text-align: center; font-style: italic; font-size: 18px; color: gray; margin-top: 20px;'>
            Tecchnologies used: Python, Pandas, Plotly, Streamlit, MongoDB atlas.
        </div>
        """,
        unsafe_allow_html=True
        )

# OVERVIEW PAGE
if selected == "Overview":
    st.markdown("## Overview of the Airbnb data")

    tab1,tab2,tab3 = st.tabs(["$\huge  RAW DATA $","$ __________ $", "$\huge INSIGHTS $"])
    
    # RAW DATA TAB
    with tab1:
        col1,col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(col.find_one())
        if col2.button("Click to view Dataframe"):
            col1.write(col.find_one())
            col2.write(df)

    # INSIGHTS TAB
    with tab3:
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        proprety = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price(Currency)',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {proprety} & Price >= {price[0]} & Price <= {price[1]}'
        
        col1,col2 = st.columns(2,gap='medium')
        
        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='Property_type',
                         y='Listings',
                         orientation='v',
                         color='Listings',
                         color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig,use_container_width=True) 
        
            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Listings',
                         y='Host_name',
                         orientation='h',
                         color='Host_name',
                         color_continuous_scale=px.colors.sequential.Inferno)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df3 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")                      
            fig = px.pie(
                df3,
                names='Room_type',
                values='counts',
                title='Total Listings Proportion in each Room Type',
                color='Room_type',  # Color by room type
                color_discrete_sequence=px.colors.diverging.Portland,
                hole=0.4,
            )
            st.plotly_chart(fig, use_container_width=True)
            
            
            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
            st.plotly_chart(fig,use_container_width=True)

    # EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore the Airbnb data")
    
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    proprety = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price(Currency)',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # uner input convert
    query = f'Country in {country} & Room_type in {room} & Property_type in {proprety} & Price >= {price[0]} & Price <= {price[1]}'
    
    st.markdown("## Price Analysis")

    col1,col2 = st.columns(2,gap='medium')    
    with col1:
        #average price
        price_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=price_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        st.markdown("## Availability Analysis")

        # room abailabilty
        fig1 = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig1,use_container_width=True)

    with col2:
        
        # avg prive in country
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        custom_colors = ['blue', 'green', 'yellow', 'orange', 'red', 'violet','maroon']
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale=custom_colors
                            )
        col2.plotly_chart(fig,use_container_width=True)

        st.markdown("#   ")
        st.markdown("#   ")

        # average availabilty in countries
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig1 = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )        
        col2.plotly_chart(fig1,use_container_width=True)

    st.markdown(
        """
        <div style='text-align: center; font-style: italic; font-size: 18px; color: gray; margin-top: 20px;'>
            Thank You for Viewing!
        </div>
        """,
        unsafe_allow_html=True
        )

            
        
