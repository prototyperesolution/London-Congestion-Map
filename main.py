import streamlit as st
import requests
import pandas as pd
import folium
from folium.plugins import HeatMap
import preprocessing
from streamlit_folium import st_folium
import math

STAMEN_TONER_ATTRIBUTION = (
    'Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
    'under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. '
    'Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, '
    'under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.'
)

def fetch_crowding_data(Naptan):
    url = f"https://api.tfl.gov.uk/crowding/{Naptan}/Live"
    response = requests.get(url)
    data = response.json()
    return data

def create_map():
    # Center the map on London
    london_coords = [51.5074, -0.1278]
    m = folium.Map(location=london_coords, zoom_start=100, 
                   tiles="CartoDB Positron", attr="Stamen Terrain")
    
    return m


            

def main():
    st.title("Live map boundaries in London")
    stops_data = preprocessing.process_active_stops()
    col1, col2 = st.columns([3,1])
    with col1:
        folium_map = create_map()
        for index, stop in stops_data.iterrows():
            if math.isnan(stop['Latitude']) or math.isnan(stop['Longitude']):
                st.write(stop)
            else:
                folium.Marker(location = [stop['Latitude'], stop['Longitude']],
                              popup = stop['CommonName']).add_to(folium_map)
        map_state = st_folium(folium_map, width=700, height=500)
       
    with col2:
        if 'map_bounds' not in st.session_state:
            st.session_state['map_bounds'] = None

        # Add a button to capture and display the map bounds
        if st.button("Show Count of Current Stations"):
            if map_state and 'bounds' in map_state:
                st.session_state['map_bounds'] = map_state['bounds']

        # Display the map bounds when the button is clicked
        if st.session_state['map_bounds']:
            bounds = st.session_state['map_bounds']
            curr_stations = preprocessing.return_stops_in_bounds(stops_data, bounds)
            st.write(len(curr_stations))
        else:
            st.write("Click the button to show the current map bounds.")
                              
if __name__ == "__main__":
    main()
