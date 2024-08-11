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

def main():
    folium_map = create_map()
    st.title("Live map boundaries in London")
    col1, col2 = st.columns([3,1])

    with col2:
        if 'map_bounds' not in st.session_state:
            st.session_state['map_bounds'] = None

        # Add a button to capture and display the map bounds
        if st.button("Show crowding heatmap"):
            #try:
            if st.session_state['map_bounds']:
                bounds = st.session_state['map_bounds']
                curr_stations = preprocessing.return_stops_in_bounds(stops_data, bounds)
                curr_stations = curr_stations.drop_duplicates(subset='commonName', keep='first')
                #50 is an API call limit
                for i in range(0,min(50, len(curr_stations))):
                    curr_crowding = api_calls.fetch_crowding_data(curr_stations.iloc[i,curr_stations.columns.get_loc('naptanId')])
                    st.write(curr_crowding)
                    curr_stations.iloc[i, curr_stations.columns.get_loc('crowdData')] = curr_crowding['percentageOfBaseline']*100
                heat_df = curr_stations.loc[:50,['lat','lon','crowdData']]
                st.write(heat_df)
                st.session_state['heat_data'] = heat_df

            else:
                st.write("Click the button to show the current map bounds.")
            #except:
            #    st.write('Unable to fetch data. Possibly too many API requests \n please wait 1 minute before trying again')                        

    with col1:
        if 'map' not in st.session_state:
            st.session_state['map'] = folium_map
        else:
            folium_map = st.session_state['map']

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
                              icon = folium.DivIcon(html=square_html)).add_to(folium_map)
        
        if 'heat_data' in st.session_state:
            HeatMap(st.session_state['heat_data'], radius = 20).add_to(folium_map)
        map_state = st_folium(folium_map, width=450, height=450)
        st.session_state['map'] = folium_map
        st.session_state['map_bounds'] = map_state['bounds']

    
if __name__ == "__main__":
    main()
