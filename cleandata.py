import os
import numpy as np
import pandas as pd
import csv
from math import cos, asin, sqrt
from timeit import default_timer as timer
from pathlib import Path
from datetime import datetime


# ------------------------------------------
# ----------- Inputs  -------------
# ------------------------------------------

FILE_AIRPORTS  = "/Users/eyana.mallari/Projects-Local/py_airports/Input/world-airports.csv"

FILE_ZIPCODES  = "/Users/eyana.mallari/Projects-Local/py_airports/Input/us_postal_codes.csv"


def cleanAirportData():
    df = pd.read_csv(FILE_AIRPORTS,encoding = "ISO-8859-1")

    print(df.columns)
    df_filter = df[(df['iso_country']=='US') & (df['type'].isin(['large_airport','medium_airport','small_airport']))]

    df_filter['iso_state'] = df_filter['iso_region'].str.split('-').str[1]
    #print(df_filter.sample(10))
    [print(x) for x in df_filter['type'].unique()]
    [print(x) for x in df_filter['iso_country'].unique()]
    [print(x) for x in df_filter['iso_state'].unique()]

    #return df_filter

def cleanZipcodesData():
    df = pd.read_csv(FILE_ZIPCODES,encoding = "ISO-8859-1")
    print(df.columns)

cleanZipcodesData()
