import requests
import streamlit as st

@st.cache_data
def fetch_crowding_data(Naptan):
    url = f"https://api.tfl.gov.uk/crowding/{Naptan}/Live"
    response = requests.get(url)
    data = response.json()
    return data

print(fetch_crowding_data(0))