import pandas as pd
import math

def process_active_stops():
    df = pd.read_csv("data/Stops.csv", low_memory = False)
    df = df.dropna(subset=['Latitude', 'Longitude', 'NaptanCode'])
    df = df[(df["ParentLocalityName"] == "London") & (df["Status"] == "active") &
            (df["ATCOCode"].str.startswith("9"))]
    return df

def return_stops_in_bounds(df, bounds):
    min_lat, min_long = bounds['_southWest']['lat'], bounds['_southWest']['lng']
    max_lat, max_long = bounds['_northEast']['lat'], bounds['_northEast']['lng']

    stations_in_frame = df[(df["Longitude"] < max_long) & (min_long < df["Longitude"]) & (min_lat < df["Latitude"]) &(df["Latitude"] < max_lat)]
    return stations_in_frame