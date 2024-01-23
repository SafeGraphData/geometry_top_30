import streamlit as st
from read_data import read_from_gsheets
import altair as alt
from datetime import datetime, timedelta
import pandas as pd
import streamlit.components.v1 as components
import plotly.express as px

st.set_page_config(
    page_title="Geometry Summary Statistics - Top 30",
    layout="wide"
)

#### Top 30 Geometry ####
top_30_geometry_df = (
    read_from_gsheets("Countries")
    .assign(**{
        "Total POI with Parking Lots": lambda df: df["Total POI with Parking Lots"].astype(int),
        "POI with polygons": lambda df: df["POI with polygons"].str.replace(",", "").astype(int),
        "Point-only POI": lambda df: df["Point-only POI"].str.replace(",", "").astype(int),
        "Polygon coverage": lambda df: ((df["Polygon coverage"].str.replace(",", "").astype(float)) * 100).astype(float)
    })
    .query('iso_country_code != "US"')
    .rename(columns={"iso_country_code": "Country Code", "country": "Country"})
    [["Country Code", "Country", "Total POI with Parking Lots", "POI with polygons", "Point-only POI", "Polygon coverage"]]
    .head(30)
)

top_30_df_geometry_styled = (
    top_30_geometry_df.style
    .apply(lambda x: ['background-color: #D7E8ED' if i%2==0 else '' for i in range(len(x))], axis=0)
    .format({
       "Total POI with Parking Lots": "{:,.0f}",
        "POI with polygons": "{:,.0f}",
        "Point-only POI": "{:,.0f}",
        "Polygon coverage": "{:.01f}%"
    })
)

st.write("POI Counts - Top 30 Countries Outside the US")
st.dataframe(top_30_df_geometry_styled, use_container_width=True, hide_index=True)


hide_streamlit_style = """
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


css = '''
<style>
section.main > div:has(~ footer ) {
    padding-bottom: 0px;
}

[data-testid="ScrollToBottomContainer"] {
    overflow: hidden;
}
</style>
'''

st.markdown(css, unsafe_allow_html=True)
