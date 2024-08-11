import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
import preprocessing
from streamlit_folium import st_folium
import api_calls

crowding_api_key = '9c484d65d3664a708a65bb3954d0450f'
stops_data = preprocessing.collect_stop_points()

@st.cache_data
def create_map():
    # Center the map on London
    london_coords = [51.5074, -0.1278]
    m = folium.Map(location=london_coords, zoom_start=10, 
                   tiles="CartoDB Positron", attr="CartoDB Positron")
    
    return m

def get_curr_map_bounds(map_state):
    try:
        return [[map_state['bounds']['_southWest']['lat'],
            map_state['bounds']['_southWest']['lng']],
            [map_state['bounds']['_northEast']['lat'],
            map_state['bounds']['_northEast']['lng']]]
    except:
        return None

folium_map = create_map()

@st.cache_data
def place_stations(_map, stops_data):
    for index, stop in stops_data.iterrows():
            popup_html = f"""<div style="text-align: center;">
                    <div style="font-family: 'Courier New', Courier, monospace; color: blue; font-size: 10px;">
                        {stop['commonName']}
                    </div>"""
            square_html = f"""
                    <div style="width: 5px; height: 5px; background-color: {stop['colour']}; margin: 0 auto;"></div>
                </div>
                """
            folium.Marker(location = [stop['lat'], stop['lon']],
                              popup = folium.Popup(popup_html, max_width=200),
                              icon = folium.DivIcon(html=square_html)).add_to(_map)


@st.cache_data
def place_heatmap(_map, stops_data):
    for i in range(0,len(stops_data)):
                    curr_crowding = api_calls.fetch_crowding_data(stops_data.iloc[i,stops_data.columns.get_loc('naptanId')], crowding_api_key)
                    try:
                        stops_data.iloc[i, stops_data.columns.get_loc('crowdData')] = curr_crowding['percentageOfBaseline'].astype('int64')*100
                    except:
                        stops_data.iloc[i, stops_data.columns.get_loc('crowdData')] = 0
    heat_df = stops_data[['lat','lon','crowdData']]
    HeatMap(heat_df, 
                    min_opacity=0.4,
                    blur = 18
                        ).add_to(folium.FeatureGroup(name='Heat Map').add_to(_map))
    folium.LayerControl().add_to(_map)
            
def main():
    st.title("Live map boundaries in London")
    col1, col2 = st.columns([3,1])

    with col2:
        pass
    with col1:
        try:
            place_stations(folium_map,stops_data)
            place_heatmap(folium_map,stops_data)
        except:
             st.write('too many API requests, wait a minute')
        map_state = st_folium(folium_map, width=450, height=450)
        
    
if __name__ == "__main__":
    main()
