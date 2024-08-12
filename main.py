import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
import preprocessing
from streamlit_folium import st_folium
import api_calls

stops_data = preprocessing.collect_stop_points()

@st.cache_data
def create_map():
    # Center the map on London
    london_coords = [51.5074, -0.1278]
    m = folium.Map(location=london_coords, zoom_start=10, 
                   tiles="CartoDB Positron", attr="CartoDB Positron")
    
    return m

folium_map = create_map()
        
def main():
    st.title("Live tube crowding in London")
    #print(stops_data['crowdData'].head())
    for index, stop in stops_data.iterrows():
            popup_html = f"""<div style="text-align: center;">
                    <div style="font-family: 'Courier New', Courier, monospace; color: blue; font-size: 10px;">
                        {stop['commonName']}
                        \n
                        Current proportion of normal crowding: {stop['crowdData']}
                    </div>"""
            square_html = f"""
                    <div style="width: 5px; height: 5px; background-color: {stop['colour']}; margin: 0 auto;"></div>
                </div>
                """
            folium.Marker(location = [stop['lat'], stop['lon']],
                              popup = folium.Popup(popup_html, max_width=200),
                              icon = folium.DivIcon(html=square_html)).add_to(folium_map)

    heat_df = stops_data[['lat','lon','crowdData']]
    HeatMap(heat_df, 
                    min_opacity=0.4,
                    blur = 18
                        ).add_to(folium.FeatureGroup(name='Heat Map').add_to(folium_map))
    folium.LayerControl().add_to(folium_map)
    map_state = st_folium(folium_map, width=700, height=700)
        
    
if __name__ == "__main__":
    main()
