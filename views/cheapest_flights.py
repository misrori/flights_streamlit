
import streamlit as st
import pandas as pd
import plotly.express as px
from utils_data import get_data
#import folium
#from streamlit_folium import st_folium

# Load data (replace with actual data sources)
df, airports = get_data()


st.fragment()
def cheapest_fligts():
    # top 3 cheapest by every airport id
    st.write("Legolcsóbb repülőjegyek reptér szerint")
    st.write("Az alábbi táblázatban láthatóak a legolcsóbb repülőjegyek reptér szerint")
    cheapest_by_repter = df.groupby('repter_id').apply(lambda x: x.nsmallest(1, 'ar')).reset_index(drop=True)
    cheapest_by_repter = cheapest_by_repter.sort_values(by='ar')

    cheapest_by_repter = cheapest_by_repter[['orszag', 'repter_id', 'napok', 'ar'] + [col for col in cheapest_by_repter.columns if col not in ['orszag', 'repter_id', 'ar', 'napok', 'varos', 'link'] ] + ['varos', 'link'] ]

    # rename all columns
    col_rename_dict = column_descriptions = {
        'varos': 'Városok',
        'orszag': 'Országok',
        'napok': 'Utazás hossza (napok)',
        'ar': 'Ár (Ft)',
        'indulas': 'Indulás dátuma',
        'indulas_nap': 'Indulás napja',
        'indulas_napszak': 'Indulás napszaka',
        'vissza': 'Visszaút dátuma',
        'vissza_nap': 'Visszaút napja',
        'vissza_napszak': 'Visszaút napszaka',
        'atszallas_oda': 'Átszállások száma odaút',
        'atszallas_vissza': 'Átszállások száma visszaút',
        'indulas_ido': 'Indulás órája',
        'vissza_ido': 'Visszaút órája',
        'link': 'Link',
        'repter_id': 'Reptér ID',

    }
    # do not show repter_id_original column
    cheapest_by_repter = cheapest_by_repter[[col for col in cheapest_by_repter.columns if col not in ['repter_id_original']]]

    cheapest_by_repter = cheapest_by_repter.rename(columns=col_rename_dict)
    # start with reptér id than rest of the columns
    

    st.data_editor(
        cheapest_by_repter,
        column_config={
            "Link": st.column_config.LinkColumn(
                "Link",
                help="The top trending Streamlit apps",
                display_text="Repülj",
            )
        },
        hide_index=True,
    )

cheapest_fligts()