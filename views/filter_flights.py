import streamlit as st
import pandas as pd
from utils_data import get_data
import plotly.express as px
from datetime import datetime

df, airports = get_data()

st.fragment()
def filter_flights():

    st.sidebar.header("Filter Options")
    

    # Ensure date columns are in datetime format
    df['indulas'] = pd.to_datetime(df['indulas'])
    df['vissza'] = pd.to_datetime(df['vissza'])

    # Define column descriptions in Hungarian (excluding 'repter_id' and 'link' as per your original request)


    # Create three columns for filter layout
    col1, col2, col3 = st.columns(3)

    # Column 1: General Trip Details
    with col1:
        st.subheader("Utazás részletei")
        
        # Country filter checkbox
        enable_orszag = st.checkbox("Ország szűrő")
        if enable_orszag:
            selected_orszag = st.multiselect(
                "Országok",
                sorted(df['orszag'].unique()),
                default=None
            )
        else:
            selected_orszag = sorted(df['orszag'].unique())  # Default to all countries

        # City filter checkbox
        enable_varos = st.checkbox("Város szűrő")
        if enable_varos:
            selected_varos = st.multiselect(
                "Városok",
                sorted(df['varos'].unique()),
                default=None
            )
        else:
            selected_varos = sorted(df['varos'].unique())  # Default to all cities
        

        # Duration filter checkbox
        enable_napok = st.checkbox("Utazás hossza szűrő")
        if enable_napok:
            min_napok = int(df['napok'].min())
            max_napok = int(df['napok'].max())
            selected_napok = st.slider(
                "Utazás hossza (napok)",
                min_napok,
                max_napok,
                (min_napok, max_napok), step=1,
            )
        else:
            selected_napok = (int(df['napok'].min()), int(df['napok'].max()))  # Default to full range
        
        # Price filter checkbox
        enable_ar = st.checkbox("Ár szűrő")
        if enable_ar:
            min_ar = int(df['ar'].min())
            max_ar = int(df['ar'].max())
            selected_ar = st.slider(
                "Ár (Ft)",
                min_ar,
                max_ar,
                (min_ar, max_ar), step=1000,
            )
        else:
            selected_ar = (int(df['ar'].min()), int(df['ar'].max()))  # Default to full range

        # date range 
        try:
            enable_date_range = st.checkbox("Dátumtartomány szűrő")
            if enable_date_range:
                min_indulas = df['indulas'].min()
                max_indulas = df['vissza'].max()
                selected_date_range = st.date_input(
                    "Dátumtartomány",
                    value=(min_indulas, max_indulas),
                    min_value=min_indulas,
                    max_value=max_indulas
                )
        # Convert datetime.date to pandas.Timestamp for comparison
                min_date_for_filter = pd.Timestamp(selected_date_range[0])
                max_date_for_filter = pd.Timestamp(selected_date_range[1])
            else:
                min_date_for_filter = pd.Timestamp(df['indulas'].min())
                max_date_for_filter = pd.Timestamp(df['vissza'].max())

        except Exception as e:
            st.warning("Válaszd ki a dátumtartományt")  




    # Column 2: Departure Details
    with col2:
        st.subheader("Indulás részletei")
        # indulasi nap ja with multiseelct
        enable_indulas = st.checkbox("Indulás napja szűrő")
        if enable_indulas:
            selected_indulas_nap = st.multiselect(
                "Indulás napja",
                df['indulas_nap'].unique(),
                default=None

            )
        else:
            selected_indulas_nap = df['indulas_nap'].unique()

        # indulási napszak
        enable_indulas_napszak = st.checkbox("Indulás napszak szűrő")
        if enable_indulas_napszak:
            selected_indulas_napszak = st.multiselect(
                "Indulás napszak",
                sorted(df['indulas_napszak'].unique()),
                default=sorted(df['indulas_napszak'].unique())
            )
        else:
            selected_indulas_napszak = sorted(df['indulas_napszak'].unique())


    # Column 3: Return Details
    with col3:
        st.subheader("Visszaút részletei")

        # visszaút napja
        enable_vissza = st.checkbox("Visszaút napja szűrő")
        if enable_vissza:
            selected_vissza = st.multiselect(
                "Visszaút napja",
                df['vissza_nap'].unique(),
                default=None

            )
        else:
            selected_vissza = df['vissza_nap'].unique()
        
        # visszaút napszak
        enable_vissza_napszak = st.checkbox("Visszaút napszak szűrő")
        if enable_vissza_napszak:
            selected_vissza_napszak = st.multiselect(
                "Visszaút napszak",
                sorted(df['vissza_napszak'].unique()),
                default=sorted(df['vissza_napszak'].unique())
            )
        else:
            selected_vissza_napszak = sorted(df['vissza_napszak'].unique())


    # Build the filtering mask


    mask = pd.Series(True, index=df.index)

    # Apply the filters
    mask = mask & df['orszag'].isin(selected_orszag)
    mask = mask & df['varos'].isin(selected_varos)
    mask = mask & df['napok'].between(selected_napok[0], selected_napok[1])
    mask = mask & df['ar'].between(selected_ar[0], selected_ar[1])
    mask = mask & (df['indulas'] >= min_date_for_filter)
    mask = mask & (df['vissza'] <= max_date_for_filter)

    mask = mask & df['indulas_nap'].isin(selected_indulas_nap)
    mask = mask & df['indulas_napszak'].isin(selected_indulas_napszak)
    mask = mask & df['vissza_nap'].isin(selected_vissza)
    mask = mask & df['vissza_napszak'].isin(selected_vissza_napszak)






    # Apply the mask to filter the dataframe
    filtered_df = df[mask]


    # Check if filtered data is empty
    if filtered_df.empty:
        st.warning("Nincs találat a megadott szűrőkkel.")
    else:
        # Display the filtered results

        filtered_df = filtered_df[['orszag', 'repter_id', 'napok', 'ar'] + [col for col in filtered_df.columns if col not in ['orszag', 'repter_id', 'ar', 'napok', 'varos', 'link'] ] + ['varos', 'link'] ]

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
        filtered_df = filtered_df[[col for col in filtered_df.columns if col not in ['repter_id_original']]]

        filtered_df = filtered_df.rename(columns=col_rename_dict)
        # start with reptér id than rest of the columns

        st.write(f"{len(filtered_df)} repülőjárat megjelenítése:")
        st.data_editor(
            filtered_df,
            column_config={
                "Link": st.column_config.LinkColumn(
                    "Link",
                    help="The top trending Streamlit apps",
                    display_text="Repülj",
                )
            },
            hide_index=True,
        )

        # Add a download button for the filtered data
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Szűrt adatok letöltése CSV-ként",
            data=csv,
            file_name="szurt_repulojaratok.csv",
            mime="text/csv"
        )

filter_flights()