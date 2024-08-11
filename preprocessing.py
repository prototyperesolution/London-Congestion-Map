import requests
import pandas as pd
import streamlit as st
# Function to send GET requests for each tube line and collect the data
@st.cache_data
def collect_stop_points():

    # List of all tube lines in London
    tube_lines = [
        "bakerloo", "central", "circle", "district", "hammersmith-city",
        "jubilee", "metropolitan", "northern", "piccadilly", "victoria", "waterloo-city"
    ]

    line_colours = {
        'bakerloo': '#894e24',  # Brown
        'central': '#dc241f',    # Red
        'circle': '#ffce00',     # Yellow
        'district': '#007229',   # Green
        'hammersmith-city': '#d799af',  # Pink
        'jubilee': '#6a7278',    # Grey
        'metropolitan': '#751056',  # Purple
        'northern': '#000000',   # Black
        'piccadilly': '#003688', # Dark Blue
        'victoria': '#0098d4',   # Light Blue
        'waterloo-city': '#95cdba'  # Turquoise
        }

    # TfL API base URL format
    base_url = "https://api.tfl.gov.uk/Line/{}/StopPoints"

    # Initialize an empty list to store data
    all_stop_points = []

    for line in tube_lines:
        # Construct the full URL for the current line
        url = base_url.format(line)
        
        # Send the GET request to the TfL API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Process the response and extend the list with stop point data
            stop_points = response.json()
            for stop_point in stop_points:
                # Append each stop point to the list
                all_stop_points.append({
                    "line": line,  # Add the tube line as a column
                    "naptanId": stop_point.get('naptanId', None),
                    "commonName": stop_point.get('commonName', None),
                    "lat": stop_point.get('lat', None),
                    "lon": stop_point.get('lon', None),
                    "stationNaptan": stop_point.get('stationNaptan', None),
                    "stopType": stop_point.get('stopType', None),
                    "colour":line_colours[line],
                    "crowdData":0
                })
        else:
            print(f"Failed to retrieve data for {line.capitalize()} line. Status code: {response.status_code}")
        
    return pd.DataFrame(all_stop_points)


def return_stops_in_bounds(df, bounds):
    min_lat, min_long = bounds[0]
    max_lat, max_long = bounds[1]

    stations_in_frame = df[(df["lon"] < max_long) & (min_long < df["lon"]) & (min_lat < df["lat"]) &(df["lat"] < max_lat)]
    return stations_in_frame