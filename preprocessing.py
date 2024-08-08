import pandas as pd
import requests

def process_active_stops():
    df = pd.read_csv("data/Stops.csv", low_memory = False)
    df = df[(df["ParentLocalityName"] == "London") & (df["Status"] == "active")]
    return df

def return_stops_in_bounds(df, bounds):
    