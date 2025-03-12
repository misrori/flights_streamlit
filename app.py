import streamlit as st


st.set_page_config( layout="wide", page_title="Felhok.hu",page_icon="✈️",)

# --- INTRO ---
cheapest_site = st.Page(
    "views/cheapest_flights.py",
    title="Legolcsóbb járatok",
    icon=":material/account_circle:",
    default=True,
)

filter_site = st.Page(
    "views/filter_flights.py",
    title="Járatok szűrése",
    icon=":material/trending_up:",
)




# --- CRYPTO ---

map_site = st.Page(
    "views/map.py",
    title="Térképen a legolcsóbb járatok",
    icon=":material/bar_chart:",
)


pg = st.navigation(
    {
        "Legolcsóbb járatok": [cheapest_site],
        "Járatok szűrése": [filter_site],
        "Térkép": [map_site],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://i.ibb.co/TMFDzvYG/f282897c-3f18-4dbe-b73b-bfaeee581317.png',
    link="https://felhok.hu/",
    size="large")

st.sidebar.markdown("Szeretettel ❤️ by [Goldhandfinance](https://youtube.com/@goldhandfinance)")


# --- RUN NAVIGATION ---
pg.run()

