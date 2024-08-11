import requests
import streamlit as st

@st.cache_data
def fetch_crowding_data(Naptan, api_key):
    url = f"https://api.tfl.gov.uk/crowding/{Naptan}/Live"
    response = requests.get(url, params = api_key)
    data = response.json()
    return data