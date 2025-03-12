
import streamlit as st
import pandas as pd
import plotly.express as px
from utils_data import get_data
import folium
import branca
from folium.plugins import Fullscreen
from folium.plugins import Search
from streamlit_folium import st_folium
import streamlit.components.v1 as components



st.fragment()
def get_map():

    # Load data (replace with actual data sources)
    df, airports = get_data()

    selected_continent = st.radio("Válassz kontinenst", ['Európa', 'Ázsia'], horizontal=True)

    if selected_continent == 'Ázsia':
        #asia_cityes = airports[airports['continent'] == 'Asia']['city'].unique()
        # filter df for asia cityes
        df = df[df['varos'].isin(airports[airports['continent'] == 'Asia']['city'].unique())]
    elif selected_continent == 'Európa':
        df = df[df['varos'].isin(airports[airports['continent'] == 'Europe']['city'].unique())]
   

    cheapest_by_repter = df.groupby('repter_id').apply(lambda x: x.nsmallest(1, 'ar')).reset_index(drop=True)

    # join with airports
    cheapest_by_repter = cheapest_by_repter.merge(airports, left_on='repter_id_original', right_on='id', how='left')


    # show table
    st.write("Legolcsóbb repülőjegyek reptér szerint")
    st.write("Az alábbi táblázatban láthatóak a legolcsóbb repülőjegyek reptér szerint")
    cheapest_by_repter = cheapest_by_repter.sort_values(by='ar')



    base_lon = 19.5033
    base_lat =47.1625


    # Using the RdYlGn colormap from matplotlib
    colormap = branca.colormap.LinearColormap(
        vmin=cheapest_by_repter["ar"].quantile(0.0) ,
        vmax=cheapest_by_repter["ar"].quantile(1) ,
        colors = ["green", "red"],
        caption="Ár (Ft)",
    )

    # Az osztások számának és címkéinek formázása
    colormap.caption = "Ár (Ft)"
    colormap.format = "{:.0f}"  # Egész számok formátuma

    # Színskála hozzáadása a térképhez

    m = folium.Map(location=[base_lat, base_lon], zoom_start=4, tiles="Cartodb Positron")


    # show the cheapest flights on map

    for i, row in cheapest_by_repter.iterrows():
        popup_html = f"""
        <div style="width: 300px;">
            <b>{row['repter_id']} - {row['ar']:,.0f} Ft</b><br>
            Ország: {row['orszag']}<br>
            Város: {row['varos']}<br>
            Utazás hossza: {row['napok']} nap<br>
            Indulás napja: {row['indulas']} - {row['indulas_nap']}, {row['indulas_ido']}<br>
            Visszaút napja: {row['vissza']} - {row['vissza_nap']}, {row['vissza_ido']}<br>
            <a href="{row['link']}" target="_blank">Repülj</a>
        </div>
        """

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=7,
            popup=folium.Popup(popup_html, max_width=400),
            color="white",
            fill=True,
            fill_color=colormap(row['ar']),
            fill_opacity=0.9
        ).add_to(m)



    colormap.add_to(m)



    Fullscreen(position="topleft").add_to(m)

    # Display the map
    st_folium(m, height=900,width=1400)

get_map()