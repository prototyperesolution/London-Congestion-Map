import pandas as pd
import requests

def process_active_stops():
    df = pd.read_csv("data/Stops.csv", low_memory = False)
    df = df[(df["ParentLocalityName"] == "London") & (df["Status"] == "active")]
    return df

def return_stops_in_bounds(df, bounds):
    min_lat, min_long = bounds['_southWest']['lat'], bounds['_southWest']['lng']
    max_lat, max_long = bounds['_northEast']['lat'], bounds['_northEast']['lng']
    