import pandas as pd
import plotly.express as px
import streamlit as st


def translate_day(day):
    day_translation = {
        "Monday": "Hétfő", "Tuesday": "Kedd", "Wednesday": "Szerda",
        "Thursday": "Csütörtök", "Friday": "Péntek", "Saturday": "Szombat", "Sunday": "Vasárnap"
    }
    return day_translation.get(day, day)

# Caching the Tw object to optimize performance
@st.cache_data(ttl=60*60*2)
def get_data():
    df = pd.read_csv('https://raw.githubusercontent.com/misrori/flights/main/csv_data/last_prices.csv')
    #df = pd.read_csv('last_prices.csv')

    
    # Load data (replace with actual data sources)
    airports = pd.read_csv('https://raw.githubusercontent.com/misrori/flights/main/csv_data/airportrs.csv')
    #airports = pd.read_csv('airportrs.csv')

    #df['link'] = df['link'].apply(create_link)
    df['indulas_nap'] = df['indulas_nap'].apply(translate_day)
    df['vissza_nap'] = df['vissza_nap'].apply(translate_day)
    df['repter_id_original'] = df['repter_id']
    df['repter_id'] = df['varos'] + " - " + df['repter_id']
    df['link'] = [x.split('"')[0] for x in df['link']]


    return df, airports


