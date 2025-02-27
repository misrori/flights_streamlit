import streamlit as st


st.set_page_config( layout="wide", page_title="Felhok",page_icon="✈️",)


# --- INTRO ---
cheapest_site = st.Page(
    "views/cheapest_flights.py",
    title="Cheapest flights",
    icon=":material/account_circle:",
    default=True,
)

filter_site = st.Page(
    "views/filter_flights.py",
    title="Filter flights",
    icon=":material/trending_up:",
)




# --- CRYPTO ---

map_site = st.Page(
    "views/map.py",
    title="Térkép legolcsóbb repülések",
    icon=":material/bar_chart:",
)


pg = st.navigation(
    {
        "Cheapest flights": [cheapest_site],
        "Filter flights": [filter_site],
        "Map": [map_site],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://i.ibb.co/Pgw52bM/Screenshot-from-2024-12-26-09-41-17-removebg-preview.png',
    link="https://goldhandfinance.streamlit.app/",
    size="large")

st.sidebar.markdown("Made with ❤️ by [Goldhandfinance](https://youtube.com/@goldhandfinance)")


# --- RUN NAVIGATION ---
pg.run()

