import os
import numpy as np
import pandas as pd
import csv
from math import cos, asin, sqrt
from timeit import default_timer as timer
from pathlib import Path
from datetime import datetime


# ----------------------------------------------------
# ---------------- Inputs: FILES  --------------------
# ----------------------------------------------------

FILE_AIRPORTS  = "/Users/eyana.mallari/Projects-Local/py_airports/Input/world-airports.csv"

FILE_ZIPCODES  = "/Users/eyana.mallari/Projects-Local/py_airports/Input/us_postal_codes.csv"

# -------------------------------------------------------
# ---------------- Inputs: Dataframes -------------------
# -------------------------------------------------------


df_airports = pd.read_csv(FILE_AIRPORTS,encoding = "ISO-8859-1")
columns_to_drop = ['elevation_ft', 'scheduled_service', 'gps_code',
       'home_link', 'wikipedia_link', 'keywords', 'score',
       'last_updated']
df_airports.drop(columns_to_drop, axis=1, inplace=True)

# filter only US
df_airports_filter = df_airports[(df_airports['iso_country']=='US') & (df_airports['type'].isin(['large_airport','medium_airport','small_airport']))]

# Retrieve State Abbreviation
df_airports_filter = df_airports_filter.copy()
df_airports_filter.loc[:,'iso_state'] = df_airports_filter['iso_region'].str.split('-').str[1]


df_zipcodes = pd.read_csv(FILE_ZIPCODES,encoding = "ISO-8859-1")

def getAllStates():
    return df_airports_filter['iso_state'].unique()

def getAirports(state):
    df = df_airports_filter[df_airports_filter['iso_state']==state]
    return df.to_dict('records')

def getZipcodes(state):
    df_filter = df_zipcodes[(df_zipcodes['State Abbreviation']==state)]
    return df_filter.to_dict('records')


# ------------------------------------------
# ----------- Calculation ------------------
# ------------------------------------------

# Function: distance, Purpose: Calculation
# Calculates distance between two points: zipcode lat-lon and airport lat-lon
# Based on Haversine Formula (found in StackOverflow)
# Uses math library
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  #Pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin..


# Function: closest, Purpose: Calculation
# Runs distance function to given airport dataset
# Returns airport data with smallest distance to the given zipcode
def closest(data, zipcode):
    #return min(data, key=lambda p: distance(zipcode['latitude'],zipcode['longitude'],p['latitude'],p['longitude']))
    dl = []
    for p in data:
        ap = {
        'zipcode': zipcode['Zip Code'],
        'country': zipcode['Country'],
        'state': zipcode['State Abbreviation'],
        'state_full': zipcode['State'],
        'county': zipcode['County'],
        'latitude-zip': zipcode['Latitude'],
        'longitude-zip': zipcode['Longitude'],
        'nearest-airport': p['ident'],
        'latitude-air': p['latitude_deg'],
        'longitude-air': p['longitude_deg'],
        'distance': distance(zipcode['Latitude'],zipcode['Longitude'],p['latitude_deg'],p['longitude_deg'])
        }
        dl.append(ap)
    dl_sorted = sorted(dl, key=lambda k: k['distance'])
    return dl_sorted[0]


# ------------------------------------------
# ------- Orchestration & Output -----------
# ------------------------------------------

entries = 0;
i = datetime.now()
timestamp = i.strftime('%Y-%m%d-')
def calculateNearestAirport(state):
    global entries
    try:
        zipcodes = getZipcodes(state)
        dicts = []
        print("Calculating for",state,"with", len(zipcodes), "zipcodes...")
        for zc in zipcodes:
            dicts.append(closest(getAirports(state), zc))


        with open("Output/"+timestamp+state+"_nearest_airport.csv","w") as csv_file:
            dict_writer = csv.DictWriter(csv_file, dicts[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(dicts)
            csv_file.close()

    finally:
        entries = entries + len(zipcodes)
        print("Done calculating for ", len(zipcodes), "zipcodes of", state)



# ------------------------------------------
# -------- Orchestration (Terminal) --------
# ------------------------------------------

states_scope = getAllStates()[:2]

perf_time = []


try:
    start = timer()
    print("Calculating for the following states: ")
    [print (x) for x in states_scope]
    for state in states_scope:

        start_state = timer()
        calculateNearestAirport(state)
        end_state = timer()
        diff = (end_state-start_state)
        time_state={
        'state': state,
        'duration': round(diff/60,3)
        }
        perf_time.append(time_state)

finally:
    end = timer()
    print(round((end - start)/60,3), "minutes")
    print(len(perf_time), "states")
    print(entries, "zipcodes")
    for k in perf_time:
        print(k)
